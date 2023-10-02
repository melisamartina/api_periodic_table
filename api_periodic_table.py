from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, or_
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional

app = FastAPI()

engine = create_engine("sqlite:///./periodic_table.db")
try:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    SessionLocal()
    print("Conexión exitosa a la base de datos")
except Exception as e:
    raise ("Error al conectarse a la base de datos:", e)

Base = declarative_base()

class PeriodicElement(Base):
    __tablename__ = "periodic_elements"

    id = Column(Integer, primary_key=True, index=True)
    element_name = Column(String(255))
    element_symbol = Column(String(10))
    atomic_number = Column(Integer)
    atomic_mass_avg = Column(Float)
    description = Column(Text)

Base.metadata.create_all(bind=engine)

class PeriodicElementCreate(BaseModel):
    element_name: Optional[str] = None
    element_symbol: Optional[str] = None
    atomic_number: int
    atomic_mass_avg: Optional[float] = None
    description: Optional[str] = None

@app.get("/periodic_elements")
def get_periodic_elements():
    db = SessionLocal()
    elements = db.query(PeriodicElement).all()
    return elements

@app.post("/periodic_elements")
def create_periodic_element(element: PeriodicElementCreate):
    db = SessionLocal()
    existing_element = db.query(PeriodicElement).filter_by(atomic_number=element.atomic_number).first()
    if existing_element:
        raise HTTPException(status_code=400, detail="Ya existe un elemento con ese número atómico")
    new_element = PeriodicElement(
        element_name=element.element_name,
        element_symbol=element.element_symbol,
        atomic_number=element.atomic_number,
        atomic_mass_avg=element.atomic_mass_avg,
        description=element.description
    )
    db.add(new_element)
    db.commit()
    db.refresh(new_element)
    return new_element

@app.delete("/periodic_elements/{atomic_number}")
def delete_periodic_element(atomic_number: int):
    db = SessionLocal()
    element = db.query(PeriodicElement).filter_by(atomic_number=atomic_number).first()
    if not element:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    db.delete(element)
    db.commit()

    return {"mensaje": "Elemento eliminado correctamente"}

@app.put("/periodic_elements/{atomic_number}")
def update_periodic_element(atomic_number: int, element: PeriodicElementCreate):
    db = SessionLocal()
    existing_element = db.query(PeriodicElement).filter_by(atomic_number=atomic_number).first()
    if not existing_element:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    if element.element_name: 
        existing_element.element_name = element.element_name
    if element.element_symbol:
        existing_element.element_symbol = element.element_symbol
    if element.atomic_number:
        existing_element.atomic_number = element.atomic_number
    if element.atomic_mass_avg:
        existing_element.atomic_mass_avg = element.atomic_mass_avg
    if element.description:
        existing_element.description = element.description
    db.commit()
    db.refresh(existing_element)
    
    return existing_element

@app.get("/periodic_elements/{query}")
def get_periodic_element(query: str):
    db = SessionLocal()
    element = db.query(PeriodicElement).filter(
        or_(
            PeriodicElement.atomic_number == query,
            PeriodicElement.element_name == query,
            PeriodicElement.element_symbol == query
        )
    ).first()

    if not element:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    return element