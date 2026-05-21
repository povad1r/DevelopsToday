from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from typing import List
import secrets

from . import models, schemas, crud
from .database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title='Travel Company API')
security = HTTPBasic()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "login")
    correct_password = secrets.compare_digest(credentials.password, "supersecret0000")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
@app.post("/projects", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return await crud.create_project(db=db, project=project)

@app.get("/projects", response_model=List[schemas.Project])
def get_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_projects(db=db, skip=skip, limit=limit)

@app.get("/projects/{project_id}", response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project_update: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    db_project = crud.update_project(db=db, project_id=project_id, project_update=project_update)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db), username: str = Depends(verify_credentials)):
    db_project = crud.delete_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return None

@app.post("/projects/{project_id}/places", response_model=schemas.Place, status_code=status.HTTP_201_CREATED)
async def add_place(project_id: int, place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    return await crud.add_place_to_project(db=db, project_id=project_id, place=place)

@app.get("/places/{place_id}", response_model=schemas.Place)
def read_place(place_id: int, db: Session = Depends(get_db)):
    db_place = crud.get_place(db, place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return db_place

@app.put("/places/{place_id}", response_model=schemas.Place)
def update_place(place_id: int, place_update: schemas.PlaceUpdate, db: Session = Depends(get_db)):
    db_place = crud.update_place(db=db, place_id=place_id, place_update=place_update)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return db_place
