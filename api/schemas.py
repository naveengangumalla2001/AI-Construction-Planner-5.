from pydantic import BaseModel


class ConstructionRequest(BaseModel):
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