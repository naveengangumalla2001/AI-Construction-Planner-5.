import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import inspect
import requests
from rag.qa import generate_answer
from rag.document_loader import load_documents
from rag.chunking import chunk_documents
from rag.embeddings import embedding_model, create_embeddings
from rag.retriever import retrieve_documents


from datetime import date, timedelta

from graph.workflow import construction_workflow
from planning.material_estimator import estimate_materials
from planning.timeline import estimate_timeline
from planning.budget_optimizer import optimize_budget, generate_scenarios
from planning.floor_planner import create_floor_plan
from planning.visualization import create_3d_building

from reports.pdf_generator import generate_project_report


API_URL = "http://127.0.0.1:8000/analyze"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Construction Planner",
    page_icon="🏗️",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🏗️ AI-Powered Smart Construction Planning System")

st.write(
    """
    This application provides preliminary construction planning,
    cost estimation, material estimation, timeline estimation,
    conceptual 2D floor planning and conceptual 3D visualization.
    """
)

st.info(
    "⚠️ This system provides preliminary estimates for planning and "
    "demonstration purposes. Final architectural, structural, electrical, "
    "plumbing and construction decisions must be validated by qualified professionals."
)


# ============================================================
# LOAD ML MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load("models/construction_cost_model.pkl")

# ============================================================
# RAG KNOWLEDGE BASE
# ============================================================

@st.cache_resource
def load_rag_knowledge_base():

    documents = load_documents()

    chunks = chunk_documents(documents)

    embeddings = create_embeddings(chunks)

    return chunks, embeddings

try:
    model = load_model()
except Exception as e:
    st.error(f"❌ Model could not be loaded: {e}")
    st.stop()


# ============================================================
# HELPER FUNCTION
# ============================================================

def call_function_safely(func, kwargs):
    """
    Calls a function using only the keyword arguments
    accepted by that function.

    This prevents errors such as:
    - unexpected keyword argument 'parking'
    - missing arguments caused by different function versions
    """

    try:
        signature = inspect.signature(func)
        parameters = signature.parameters

        # If function accepts **kwargs, send everything
        accepts_kwargs = any(
            param.kind == inspect.Parameter.VAR_KEYWORD
            for param in parameters.values()
        )

        if accepts_kwargs:
            return func(**kwargs)

        # Send only parameters accepted by the function
        filtered_kwargs = {
            key: value
            for key, value in kwargs.items()
            if key in parameters
        }

        return func(**filtered_kwargs)

    except Exception:
        # If introspection fails, try normal call
        return func(**kwargs)


# ============================================================
# PROJECT INPUT SECTION
# ============================================================

st.header("📋 Project Requirements")

col1, col2, col3 = st.columns(3)

with col1:

    project_name = st.text_input(
        "Project Name",
        value="My Construction Project"
    )

    location = st.selectbox(
        "Location",
        [
            "Hyderabad",
            "Bengaluru",
            "Chennai",
            "Pune",
            "Mumbai",
            "Delhi",
            "Kochi"
        ]
    )

    plot_area = st.number_input(
        "Plot Area (sqft)",
        min_value=300.0,
        max_value=100000.0,
        value=1500.0,
        step=50.0
    )

    builtup_area = st.number_input(
        "Built-up Area (sqft)",
        min_value=300.0,
        max_value=100000.0,
        value=1200.0,
        step=50.0
    )


with col2:

    floors = st.number_input(
        "Number of Floors",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )

    bedrooms = st.number_input(
        "Number of Bedrooms",
        min_value=1,
        max_value=20,
        value=3,
        step=1
    )

    bathrooms = st.number_input(
        "Number of Bathrooms",
        min_value=1,
        max_value=20,
        value=2,
        step=1
    )

    construction_quality = st.selectbox(
        "Construction Quality",
        [
            "Economy",
            "Standard",
            "Premium"
        ]
    )


with col3:

    material_quality = st.selectbox(
        "Material Quality",
        [
            "Basic",
            "Standard",
            "Premium"
        ]
    )

    parking = st.selectbox(
        "Parking",
        [
            "No",
            "Yes"
        ]
    )

    budget = st.number_input(
        "Project Budget (₹)",
        min_value=100000.0,
        max_value=100000000.0,
        value=2500000.0,
        step=100000.0
    )

    start_date = st.date_input(
        "Project Start Date",
        value=date.today()
    )


# ============================================================
# VALIDATION
# ============================================================

if builtup_area > plot_area:

    st.warning(
        "⚠️ Built-up area is greater than plot area. "
        "Please verify the project dimensions."
    )


# ============================================================
# GENERATE BUTTON
# ============================================================

generate_button = st.button(
    "🚀 Generate Complete Construction Plan",
    type="primary",
    width="stretch"
)


# ============================================================
# MAIN PROJECT PIPELINE
# ============================================================

if generate_button:

    # ========================================================
    # MULTI-AGENT WORKFLOW (via FastAPI backend)
    # ========================================================

    project_input = {
        "project_name": project_name,
        "location": location,
        "plot_area": plot_area,
        "builtup_area": builtup_area,
        "floors": floors,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "construction_quality": construction_quality,
        "material_quality": material_quality,
        "parking": parking,
        "budget": budget
    }

    try:

        with st.spinner(
            "🤖 Running AI Construction Planning Agents..."
        ):

            response = requests.post(
                API_URL,
                json=project_input,
                timeout=120
            )

            response.raise_for_status()

            workflow_result = response.json()

        # Generate visualization objects locally for Streamlit display
        workflow_result["floor_plan"] = call_function_safely(
            create_floor_plan,
            {
                "plot_area": plot_area,
                "builtup_area": builtup_area,
                "floors": floors,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "parking": parking
            }
        )

        workflow_result["visualization"] = call_function_safely(
            create_3d_building,
            {
                "plot_area": plot_area,
                "builtup_area": builtup_area,
                "floors": floors,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "parking": parking
            }
        )

        st.success(
            "✅ LangGraph Multi-Agent Workflow Completed"
        )

        # Store workflow results
        workflow_predicted_cost = workflow_result.get(
            "predicted_cost"
        )

        workflow_materials = workflow_result.get(
            "material_estimate"
        )

        workflow_timeline = workflow_result.get(
            "timeline"
        )

        workflow_floor_plan = workflow_result.get(
            "floor_plan"
        )

        workflow_visualization = workflow_result.get(
            "visualization"
        )

        workflow_budget_status = workflow_result.get(
            "budget_status"
        )

        workflow_optimization = workflow_result.get(
            "optimization_result"
        )

    except Exception as e:

        st.error(
            f"❌ LangGraph workflow failed: {e}"
        )

        st.stop()


    # ========================================================
    # CONSTRUCTION PLANNING RESULTS
    # ========================================================

    st.divider()

    st.header("🏗️ Construction Planning Results")

    # --------------------------------------------------------
    # 1. MACHINE LEARNING COST PREDICTION
    # --------------------------------------------------------

    st.subheader("💰 Construction Cost Estimation")

    # Important:
    # These are exactly the features used during model training.

    new_project = pd.DataFrame(
        [
            {
                "plot_area_sqft": plot_area,
                "builtup_area_sqft": builtup_area,
                "floors": floors,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "location": location,
                "construction_quality": construction_quality,
                "material_quality": material_quality,
                "parking": parking
            }
        ]
    )

    try:

        predicted_cost = float(
            workflow_result["predicted_cost"]
        )

        # Indicative cost split
        material_cost = predicted_cost * 0.60
        labour_cost = predicted_cost * 0.30
        other_cost = predicted_cost * 0.10

        # Display metrics
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Estimated Total Cost",
                f"₹{predicted_cost:,.0f}"
            )

        with c2:
            st.metric(
                "Material Cost",
                f"₹{material_cost:,.0f}"
            )

        with c3:
            st.metric(
                "Labour Cost",
                f"₹{labour_cost:,.0f}"
            )

        with c4:
            st.metric(
                "Other Cost",
                f"₹{other_cost:,.0f}"
            )

        # ----------------------------------------------------
        # COST BREAKDOWN
        # ----------------------------------------------------

        st.subheader("📊 Cost Breakdown")

        cost_data = pd.DataFrame(
            {
                "Category": [
                    "Material",
                    "Labour",
                    "Other"
                ],
                "Cost": [
                    material_cost,
                    labour_cost,
                    other_cost
                ]
            }
        )

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:

            fig_pie = px.pie(
                cost_data,
                names="Category",
                values="Cost",
                title="Construction Cost Distribution"
            )

            st.plotly_chart(
                fig_pie,
                width="stretch"
            )

        with col_chart2:

            st.dataframe(
                cost_data.style.format(
                    {"Cost": "₹{:,.0f}"}
                ),
                width="stretch"
            )

    except Exception as e:

        st.error(
            f"❌ Cost prediction failed: {e}"
        )

        st.stop()


    # ========================================================
    # 2. BUDGET OPTIMIZATION
    # ========================================================

    st.divider()

    st.subheader("💰 Budget Optimization")

    budget_difference = budget - predicted_cost

    st.markdown("---")

    st.subheader("🤖 AI Budget Scenario Optimization")

    st.write(
        "The system evaluates alternative project configurations "
        "using the trained ML cost prediction model."
    )

    scenario_results = generate_scenarios(
        model=model,
        budget=budget,
        plot_area=plot_area,
        builtup_area=builtup_area,
        floors=floors,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        location=location,
        construction_quality=construction_quality,
        material_quality=material_quality,
        parking=parking
    )

    scenario_df = pd.DataFrame(scenario_results)

    st.dataframe(
        scenario_df,
        width="stretch"
    )

    # Find scenarios that are within budget
    feasible_scenarios = [
        scenario
        for scenario in scenario_results
        if scenario["Estimated Cost"] <= budget
    ]

    if feasible_scenarios:

        # Select the option with the smallest change from the original
        # project; ties are broken by the highest estimated cost that
        # still remains within budget.
        recommended = min(
            feasible_scenarios,
            key=lambda x: (
                x["Change Score"],
                -x["Estimated Cost"]
            )
        )

        st.success("🏆 Recommended Budget-Friendly Option")

        st.write(
            f"**Scenario:** {recommended['Scenario']}"
        )

        st.write(
            f"**Estimated Cost:** "
            f"₹{recommended['Estimated Cost']:,.0f}"
        )

        st.write(
            f"**Remaining Budget:** "
            f"₹{recommended['Budget Difference']:,.0f}"
        )

    else:

        st.warning(
            "⚠️ None of the generated scenarios fit within the "
            "current budget."
        )

    optimization_result = optimize_budget(
        budget=budget,
        predicted_cost=predicted_cost,
        construction_quality=construction_quality,
        material_quality=material_quality,
        builtup_area=builtup_area,
        floors=floors,
        parking=parking
    )

    budget_utilization = (predicted_cost / budget) * 100

    if budget_difference >= 0:

        st.success("✅ Project is within the planned budget.")

        b1, b2, b3 = st.columns(3)

        with b1:
            st.metric(
                "Client Budget",
                f"₹{budget:,.0f}"
            )

        with b2:
            st.metric(
                "Estimated Cost",
                f"₹{predicted_cost:,.0f}"
            )

        with b3:
            st.metric(
                "Remaining Budget",
                f"₹{budget_difference:,.0f}"
            )

    else:

        extra_amount = abs(budget_difference)

        st.warning("⚠️ Project is over the planned budget.")

        b1, b2, b3 = st.columns(3)

        with b1:
            st.metric(
                "Client Budget",
                f"₹{budget:,.0f}"
            )

        with b2:
            st.metric(
                "Estimated Cost",
                f"₹{predicted_cost:,.0f}"
            )

        with b3:
            st.metric(
                "Additional Budget Required",
                f"₹{extra_amount:,.0f}"
            )

    st.write(
        f"**Budget Utilization:** {budget_utilization:.1f}%"
    )

    if predicted_cost > budget:

        st.write("### 💡 Preliminary Optimization Suggestions")

        suggestions = []

        if construction_quality == "Premium":
            suggestions.append(
                "Consider reviewing construction quality from Premium to Standard."
            )

        if material_quality == "Premium":
            suggestions.append(
                "Consider reviewing material quality from Premium to Standard."
            )

        if builtup_area > 1000:
            suggestions.append(
                "Consider reducing the built-up area if project requirements allow."
            )

        if floors > 1:
            suggestions.append(
                "Consider reviewing the number of floors and overall space requirements."
            )

        if parking == "Yes":
            suggestions.append(
                "Review the parking requirement and available space."
            )

        if suggestions:

            for suggestion in suggestions:
                st.write(f"• {suggestion}")

        else:

            st.write(
                "Review project requirements and construction specifications "
                "with a qualified professional."
            )

    else:

        st.info(
            "The current project estimate is within the specified budget. "
            "The remaining amount can be considered for contingency or "
            "future requirement upgrades."
        )

    st.caption(
        "Budget optimization suggestions are preliminary planning suggestions "
        "and should be validated with qualified construction professionals."
    )


    # ========================================================
    # 3. MATERIAL ESTIMATION
    # ========================================================

    st.divider()

    st.subheader("🧱 Estimated Construction Materials")

    try:

        material_kwargs = {
            "builtup_area": builtup_area,
            "plot_area": plot_area,
            "floors": floors,
            "construction_quality": construction_quality,
            "material_quality": material_quality
        }

        materials = workflow_result["material_estimate"]

        if isinstance(materials, pd.DataFrame):

            st.dataframe(
                materials,
                width="stretch"
            )

        elif isinstance(materials, dict):

            material_df = pd.DataFrame(
                list(materials.items()),
                columns=["Material", "Estimated Quantity"]
            )

            st.dataframe(
                material_df,
                width="stretch"
            )

        else:

            st.write(materials)

    except Exception as e:

        materials = {}

        st.warning(
            f"⚠️ Material estimation could not be generated: {e}"
        )


    # ========================================================
    # 4. CONSTRUCTION TIMELINE
    # ========================================================

    st.divider()

    st.subheader("📅 Construction Timeline")

    try:

        timeline_kwargs = {
            "builtup_area": builtup_area,
            "floors": floors,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "construction_quality": construction_quality
        }

        timeline = workflow_result["timeline"]

        # ----------------------------------------------
        # Convert timeline into dataframe if dictionary
        # ----------------------------------------------

        if isinstance(timeline, dict):

            timeline_df = pd.DataFrame(
                list(timeline.items()),
                columns=[
                    "Construction Phase",
                    "Estimated Days"
                ]
            )

            st.dataframe(
                timeline_df,
                width="stretch"
            )

            # Calculate total duration
            numeric_values = []

            for value in timeline.values():

                try:
                    numeric_values.append(int(value))

                except (ValueError, TypeError):
                    pass

            if "Total" in timeline:
                total_days = int(timeline["Total"])
            else:
                total_days = 240

        elif isinstance(timeline, pd.DataFrame):

            st.dataframe(
                timeline,
                width="stretch"
            )

            total_days = 240

        else:

            st.write(timeline)
            total_days = 240

    except Exception as e:

        st.warning(
            f"⚠️ Timeline estimation could not be generated: {e}"
        )

        timeline = {}
        total_days = 240


    # ========================================================
    # 5. COMPLETION DATE
    # ========================================================

    estimated_completion_date = (
        start_date + timedelta(days=int(total_days))
    )

    st.success(
        f"🏗️ Estimated Construction Duration: "
        f"{int(total_days)} days"
    )

    st.info(
        f"📅 Estimated Completion Date: "
        f"{estimated_completion_date.strftime('%d-%m-%Y')}"
    )

    st.caption(
        "Completion date is an estimate and may vary due to weather, "
        "material availability, labour availability and site conditions."
    )


    # ========================================================
    # 6. 2D FLOOR PLAN
    # ========================================================

    st.divider()

    st.subheader("🏠 Conceptual 2D Floor Plan")

    st.write(
        "Interactive conceptual floor plan based on the project requirements."
    )

    try:

        floor_plan = workflow_result["floor_plan"]

        if floor_plan is not None:

            st.plotly_chart(
                floor_plan,
                width="stretch"
            )

        else:

            st.warning(
                "⚠️ Floor plan was not generated."
            )

    except Exception as e:

        st.error(
            f"❌ 2D floor plan could not be generated: {e}"
        )

    st.info(
        "⚠️ This is a conceptual floor plan for preliminary planning only. "
        "Final architectural drawings must be prepared and approved by qualified professionals."
    )


    # ========================================================
    # 7. 3D BUILDING VISUALIZATION
    # ========================================================

    st.subheader("🏠 3D Building Visualization")

    try:

        visualization = workflow_result["visualization"]

        if visualization is not None:

            st.plotly_chart(
                visualization,
                width="stretch"
            )

            st.info(
                "⚠️ The 3D model is a conceptual visualization "
                "for planning purposes and is not an architectural "
                "or structural drawing."
            )

        else:

            st.warning(
                "⚠️ 3D visualization was not generated."
            )

    except Exception as e:

        st.error(
            f"❌ 3D visualization could not be displayed: {e}"
        )


    # ========================================================
    # 8. PROJECT DETAILS
    # ========================================================

    st.divider()

    with st.expander("📋 View Project Input Details"):

        project_details = pd.DataFrame(
            {
                "Parameter": [
                    "Project Name",
                    "Location",
                    "Plot Area",
                    "Built-up Area",
                    "Floors",
                    "Bedrooms",
                    "Bathrooms",
                    "Construction Quality",
                    "Material Quality",
                    "Parking",
                    "Project Budget",
                    "Start Date",
                    "Estimated Completion"
                ],
                "Value": [
                    str(project_name),
                    str(location),
                    f"{plot_area:,.0f} sqft",
                    f"{builtup_area:,.0f} sqft",
                    str(floors),
                    str(bedrooms),
                    str(bathrooms),
                    str(construction_quality),
                    str(material_quality),
                    str(parking),
                    f"₹{budget:,.0f}",
                    start_date.strftime("%d-%m-%Y"),
                    estimated_completion_date.strftime("%d-%m-%Y")
                ]
            }
        )

        st.dataframe(
            project_details,
            width="stretch",
            hide_index=True
        )


    # ========================================================
    # 9. PDF PROJECT REPORT
    # ========================================================

    st.divider()

    st.subheader("📄 Project Report")

    st.write(
        "Generate a downloadable PDF containing project details, "
        "cost estimation, materials and construction timeline."
    )

    try:

        pdf_file = generate_project_report(
            project_name=project_name,
            location=location,
            plot_area=plot_area,
            builtup_area=builtup_area,
            floors=floors,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            construction_quality=construction_quality,
            material_quality=material_quality,
            parking=parking,
            predicted_cost=predicted_cost,
            material_cost=material_cost,
            labour_cost=labour_cost,
            other_cost=other_cost,
            materials=materials,
            timeline=timeline,
            start_date=start_date,
            completion_date=estimated_completion_date,
            budget_optimization=optimization_result
        )

        safe_project_name = (
            project_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        st.download_button(
            label="📄 Download Construction Project Report",
            data=pdf_file,
            file_name=f"{safe_project_name}_Construction_Report.pdf",
            mime="application/pdf",
            width="stretch"
        )

    except Exception as e:

        st.error(
            f"❌ PDF report could not be generated: {e}"
        )


# ========================================================
# 🤖 CONSTRUCTION KNOWLEDGE ASSISTANT
# ========================================================

st.divider()

st.subheader("🤖 Construction Knowledge Assistant")

st.write(
    "Ask questions about residential construction, "
    "construction stages, cost factors, and safety."
)

user_question = st.text_input(
    "Ask a construction-related question:",
    placeholder="Example: What are the major stages of construction?"
)

if st.button("🔍 Ask Construction Assistant"):

    if not user_question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching construction knowledge..."):

            chunks, embeddings = load_rag_knowledge_base()

            query_embedding = embedding_model.encode(
                user_question
            )

            retrieved_chunks = retrieve_documents(
                query_embedding=query_embedding,
                embeddings=embeddings,
                chunks=chunks,
                top_k=3
            )

            answer = generate_answer(
                question=user_question,
                retrieved_chunks=retrieved_chunks
            )

        st.markdown("### 💡 Answer")

        st.write(answer)

        with st.expander("📚 Retrieved Knowledge"):

            for i, chunk in enumerate(
                retrieved_chunks,
                start=1
            ):

                st.markdown(
                    f"**Source {i}:** "
                    f"{chunk['source']}"
                )

                st.write(chunk["content"])

                st.write(
                    f"Similarity distance: "
                    f"{chunk['distance']:.4f}"
                )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "⚠️ Cost, material quantities, floor planning, 3D visualization "
    "and timeline are preliminary estimates for planning and demonstration "
    "purposes only. Final construction decisions must be validated by "
    "qualified architects, structural engineers and construction professionals."
)