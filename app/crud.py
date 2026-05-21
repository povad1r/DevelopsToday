from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, services, schemas


async def create_project(db: Session, project: schemas.ProjectCreate) -> models.Project:
    if len(project.places) > 10:
        raise HTTPException(status_code=400, detail="A project cannot have more than 10 places")

    external_ids = []
    for place in project.places:
        external_ids.append(place.external_id)

    if len(external_ids) != len(set(external_ids)):
        raise HTTPException(status_code=400, detail="Duplicate places in external ids")

    for id in external_ids:
        exists = await services.verify_place_exists(id)
        if not exists:
            raise HTTPException(status_code=400, detail=f"Place {id} not found in external API")

    db_project = models.Project(name=project.name,
                                description=project.description,
                                start_date=project.start_date)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    for place in project.places:
        db_place = models.Place(project_id=db_project.id,
                                external_id=place.external_id,
                                notes=place.notes)
        db.add(db_place)
    db.commit()
    db.refresh(db_project)

    return db_project

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def update_project(db: Session, project_id: int, project_update: schemas.ProjectUpdate):
    db_project = get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)

    return db_project

def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    for place in db_project.places:
        if place.is_visited:
            raise HTTPException(status_code=400, detail=f"Project {project_id} cannot be deleted, as at least one place is marked as visited")

    db.delete(db_project)
    db.commit()

    return db_project

async def add_place_to_project(db: Session, project_id: int, place: schemas.PlaceCreate):
    db_project = get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    if len(db_project.places) > 10:
        raise HTTPException(status_code=400, detail="A project cannot have more than 10 places")

    for p in db_project.places:
        if p.external_id == place.external_id:
            raise HTTPException(status_code=400, detail=f"Place {p.external_id} already in the project")

    if not await services.verify_place_exists(place.external_id):
        raise HTTPException(status_code=400, detail=f"Place {place.external_id} not found in API")

    db_place = models.Place(project_id=db_project.id,
                            external_id=place.external_id,
                            notes=place.notes)

    db.add(db_place)
    db.commit()
    db.refresh(db_place)

    return db_place

def get_place(db: Session, place_id: int):
    return db.query(models.Place).filter(models.Place.id == place_id).first()

def update_place(db: Session, place_id: int, place: schemas.PlaceUpdate):
    db_place = get_place(db, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")

    update_data = place.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_place, key, value)

    db.commit()
    db.refresh(db_place)

    return db_place