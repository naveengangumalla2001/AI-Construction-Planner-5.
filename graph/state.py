from typing import TypedDict, Any


class ConstructionState(TypedDict, total=False):

    # Client requirements
    project_name: str
    location: str
    plot_area: float
    builtup_area: float
    floors: int
    bedrooms: int
    bathrooms: int
    construction_quality: str
    material_quality: str
    parking: str
    budget: float

    # Generated results
    predicted_cost: float
    material_estimate: Any
    timeline: Any
    floor_plan: Any
    visualization: Any

    # Budget optimization
    budget_status: str
    optimization_result: Any

    # Final output
    report: Any