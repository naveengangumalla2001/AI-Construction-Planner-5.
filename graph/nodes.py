import joblib
import pandas as pd
from planning.material_estimator import estimate_materials
from planning.timeline import estimate_timeline
from planning.floor_planner import create_floor_plan
from planning.visualization import create_3d_building
from planning.budget_optimizer import generate_scenarios


def requirement_agent(state):
    """
    Requirement Agent
    Validates and prepares the client project requirements.
    """

    print("Requirement Agent: Processing project requirements...")

    return {
        "project_name": state["project_name"],
        "location": state["location"],
        "plot_area": state["plot_area"],
        "builtup_area": state["builtup_area"],
        "floors": state["floors"],
        "bedrooms": state["bedrooms"],
        "bathrooms": state["bathrooms"],
        "construction_quality": state["construction_quality"],
        "material_quality": state["material_quality"],
        "parking": state["parking"],
        "budget": state["budget"],
    }


def cost_agent(state):
    print("Cost Agent: Estimating construction cost...")

    model = joblib.load("models/construction_cost_model.pkl")

    input_data = {
        "plot_area_sqft": state["plot_area"],
        "builtup_area_sqft": state["builtup_area"],
        "floors": state["floors"],
        "bedrooms": state["bedrooms"],
        "bathrooms": state["bathrooms"],
        "location": state["location"],
        "construction_quality": state["construction_quality"],
        "material_quality": state["material_quality"],
        "parking": state["parking"]
    }

    input_df = pd.DataFrame([input_data])

    predicted_cost = float(model.predict(input_df)[0])

    print(f"Predicted Construction Cost: ₹{predicted_cost:,.0f}")

    return {
        "predicted_cost": predicted_cost
    }


def material_agent(state):
    """
    Material Agent
    Estimates construction materials.
    """

    print("Material Agent: Estimating construction materials...")

    materials = estimate_materials(
        state["builtup_area"],
        state["construction_quality"]
    )

    return {
        "material_estimate": materials
    }


def timeline_agent(state):
    print("Timeline Agent: Estimating construction timeline...")

    timeline = estimate_timeline(
        state["floors"],
        state["builtup_area"],
        state["construction_quality"]
    )

    return {
        "timeline": timeline
    }


def planning_agent(state):
    print("Planning Agent: Creating conceptual floor plan...")

    floor_plan = create_floor_plan(
        plot_area=state["plot_area"],
        builtup_area=state["builtup_area"],
        bedrooms=state["bedrooms"],
        bathrooms=state["bathrooms"],
        parking=state["parking"]
    )

    return {"floor_plan": floor_plan}


def visualization_agent(state):
    """
    Visualization Agent
    Generates conceptual 3D building visualization.
    """

    print("Visualization Agent: Creating 3D building...")

    visualization = create_3d_building(
        plot_area=state["plot_area"],
        builtup_area=state["builtup_area"],
        floors=state["floors"],
        bedrooms=state["bedrooms"],
        bathrooms=state["bathrooms"],
        parking=state["parking"]
    )

    return {
        "visualization": visualization
    }


def budget_agent(state):
    print("Budget Agent: Optimizing project budget...")

    model = joblib.load("models/construction_cost_model.pkl")

    budget = state["budget"]
    predicted_cost = state["predicted_cost"]

    scenarios = generate_scenarios(
        model=model,
        budget=budget,
        plot_area=state["plot_area"],
        builtup_area=state["builtup_area"],
        floors=state["floors"],
        bedrooms=state["bedrooms"],
        bathrooms=state["bathrooms"],
        location=state["location"],
        construction_quality=state["construction_quality"],
        material_quality=state["material_quality"],
        parking=state["parking"]
    )

    feasible_scenarios = [
        scenario
        for scenario in scenarios
        if scenario["Estimated Cost"] <= budget
    ]

    if predicted_cost <= budget:
        status = "Within Budget"

    else:
        status = "Over Budget"

    if feasible_scenarios:
        recommended = min(
            feasible_scenarios,
            key=lambda x: (
                x["Change Score"],
                -x["Estimated Cost"]
            )
        )

    else:
        recommended = None

    return {
        "budget_status": status,
        "optimization_result": {
            "scenarios": scenarios,
            "recommended": recommended
        }
    }


def report_agent(state):
    print("Report Agent: Preparing final project report...")

    optimization = state.get("optimization_result", {})

    recommended = optimization.get("recommended")

    return {
        "report": {
            "project_name": state.get("project_name"),
            "location": state.get("location"),
            "plot_area": state.get("plot_area"),
            "builtup_area": state.get("builtup_area"),
            "floors": state.get("floors"),
            "bedrooms": state.get("bedrooms"),
            "bathrooms": state.get("bathrooms"),
            "construction_quality": state.get("construction_quality"),
            "material_quality": state.get("material_quality"),
            "parking": state.get("parking"),
            "budget": state.get("budget"),

            "predicted_cost": state.get("predicted_cost"),

            "budget_status": state.get("budget_status"),

            "material_estimate": state.get(
                "material_estimate"
            ),

            "timeline": state.get(
                "timeline"
            ),

            "budget_optimization": optimization,

            "recommended_scenario": recommended,

            "floor_plan_generated": (
                state.get("floor_plan") is not None
            ),

            "visualization_generated": (
                state.get("visualization") is not None
            )
        }
    }

    return {
        "report": report
    }