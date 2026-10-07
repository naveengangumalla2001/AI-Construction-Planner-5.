from fastapi import FastAPI
from api.schemas import ConstructionRequest

from graph.workflow import construction_workflow
from planning.material_estimator import estimate_materials
from planning.timeline import estimate_timeline
from planning.floor_planner import create_floor_plan
from planning.visualization import create_3d_building

# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="AI Construction Planner API",
    description="AI-powered construction planning, cost estimation and visualization API",
    version="1.0.0"
)


# ============================================================
# Home API
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Construction Planner API is running"
    }


# ============================================================
# Complete Project Analysis
# ============================================================

@app.post("/analyze")
def analyze_project(request: ConstructionRequest):

    project_input = {
        "project_name": request.project_name,
        "location": request.location,
        "plot_area": request.plot_area,
        "builtup_area": request.builtup_area,
        "floors": request.floors,
        "bedrooms": request.bedrooms,
        "bathrooms": request.bathrooms,
        "construction_quality": request.construction_quality,
        "material_quality": request.material_quality,
        "parking": request.parking,
        "budget": request.budget
    }

    # Run LangGraph workflow
    result = construction_workflow.invoke(project_input)

    return {
        "project_name": request.project_name,
        "predicted_cost": result.get("predicted_cost"),
        "material_estimate": result.get("material_estimate"),
        "timeline": result.get("timeline"),
        "budget_status": result.get("budget_status"),
        "optimization_result": result.get("optimization_result"),
        "floor_plan_generated": result.get("floor_plan") is not None,
        "visualization_generated": result.get("visualization") is not None
    }


# ============================================================
# Cost Estimation API
# ============================================================

@app.post("/estimate-cost")
def estimate_cost(request: ConstructionRequest):

    project_input = {
        "project_name": request.project_name,
        "location": request.location,
        "plot_area": request.plot_area,
        "builtup_area": request.builtup_area,
        "floors": request.floors,
        "bedrooms": request.bedrooms,
        "bathrooms": request.bathrooms,
        "construction_quality": request.construction_quality,
        "material_quality": request.material_quality,
        "parking": request.parking,
        "budget": request.budget
    }

    # Run LangGraph workflow
    result = construction_workflow.invoke(project_input)

    return {
        "project_name": request.project_name,
        "predicted_cost": result.get("predicted_cost")
    }


# ============================================================
# Material Estimation API
# ============================================================

@app.post("/estimate-materials")
def estimate_materials_api(request: ConstructionRequest):

    materials = estimate_materials(
        builtup_area=request.builtup_area,
        construction_quality=request.construction_quality
    )

    return {
        "project_name": request.project_name,
        "builtup_area": request.builtup_area,
        "construction_quality": request.construction_quality,
        "material_estimate": materials
    }

# ============================================================
# Timeline Estimation API
# ============================================================

@app.post("/estimate-timeline")
def estimate_timeline_api(request: ConstructionRequest):

    timeline = estimate_timeline(
        floors=request.floors,
        builtup_area=request.builtup_area,
        construction_quality=request.construction_quality
    )

    return {
        "project_name": request.project_name,
        "builtup_area": request.builtup_area,
        "floors": request.floors,
        "construction_quality": request.construction_quality,
        "timeline": timeline
    }

# ============================================================
# 2D Floor Plan API
# ============================================================

@app.post("/generate-floor-plan")
def generate_floor_plan_api(request: ConstructionRequest):

    floor_plan = create_floor_plan(
        plot_area=request.plot_area,
        builtup_area=request.builtup_area,
        bedrooms=request.bedrooms,
        bathrooms=request.bathrooms,
        parking=request.parking
    )

    # Convert Plotly figure into JSON
    floor_plan_json = floor_plan.to_json()

    return {
        "project_name": request.project_name,
        "plot_area": request.plot_area,
        "builtup_area": request.builtup_area,
        "floors": request.floors,
        "bedrooms": request.bedrooms,
        "bathrooms": request.bathrooms,
        "parking": request.parking,
        "floor_plan": floor_plan_json
    }

# ============================================================
# 3D Building Visualization API
# ============================================================

@app.post("/generate-3d")
def generate_3d_api(request: ConstructionRequest):

    visualization = create_3d_building(
        plot_area=request.plot_area,
        builtup_area=request.builtup_area,
        floors=request.floors,
        bedrooms=request.bedrooms,
        bathrooms=request.bathrooms,
        parking=request.parking
    )

    # Convert Plotly 3D figure into JSON
    visualization_json = visualization.to_json()

    return {
        "project_name": request.project_name,
        "plot_area": request.plot_area,
        "builtup_area": request.builtup_area,
        "floors": request.floors,
        "bedrooms": request.bedrooms,
        "bathrooms": request.bathrooms,
        "parking": request.parking,
        "visualization": visualization_json
    }