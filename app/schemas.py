from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

class PlaceBase(BaseModel):
    external_id: int
    notes: Optional[str] = None

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(PlaceBase):
    notes: Optional[str] = None
    is_visited: Optional[bool] = None

class Place(PlaceBase):
    id: int
    project_id: int
    is_visited: bool

    model_config = ConfigDict(from_attributes=True)


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None

class ProjectCreate(ProjectBase):
    places: Optional[List[PlaceCreate]] = []

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None

class Project(ProjectBase):
    id: int
    is_completed: bool
    places: List[Place] = []

    model_config = ConfigDict(from_attributes=True)