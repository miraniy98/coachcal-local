from __future__ import annotations
from typing import Optional, Iterable
from datetime import date
from sqlmodel import SQLModel, Field, create_engine, Session, select

DB_URL = "sqlite:///coachcal/data/coach_state.db"
_engine = create_engine(DB_URL, echo=False)

# ---------- Models ----------

class Weight(SQLModel, table=True):
    dt: str = Field(primary_key=True)  # YYYY-MM-DD
    weight_kg: float
    ewma_kg: Optional[float] = None

class Meal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dt: str
    item: str
    grams: float
    kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float

class Workout(SQLModel, table=True):
    dt: str = Field(primary_key=True)
    template: str
    completed: int  # 0/1
    minutes: int
    sets: int
    rpe: float

class Plan(SQLModel, table=True):
    dt: str = Field(primary_key=True)
    kcal_target: int
    protein_g: int
    fat_g: int
    carbs_g: int
    workout_plan: str
    notes: str = ""

class Config(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str

# ---------- Lifecycle ----------

def init_db() -> None:
    SQLModel.metadata.create_all(_engine)

def session() -> Session:
    return Session(_engine)

# ---------- CRUD Utilities ----------

def upsert_plan(s: Session, dt: str, kcal: int, p: int, f: int, c: int, workout_plan: str, notes: str = "") -> Plan:
    plan = s.get(Plan, dt)
    if plan is None:
        plan = Plan(dt=dt, kcal_target=kcal, protein_g=p, fat_g=f, carbs_g=c, workout_plan=workout_plan, notes=notes)
        s.add(plan)
    else:
        plan.kcal_target, plan.protein_g, plan.fat_g, plan.carbs_g = kcal, p, f, c
        plan.workout_plan, plan.notes = workout_plan, notes
    s.commit()
    return plan

def get_plan(s: Session, dt: str) -> Optional[Plan]:
    return s.get(Plan, dt)

def add_meals(s: Session, dt: str, meals: Iterable[dict]) -> None:
    rows = [Meal(dt=dt, **m) for m in meals]
    s.add_all(rows)
    s.commit()

def get_meals(s: Session, dt: str) -> list[Meal]:
    return list(s.exec(select(Meal).where(Meal.dt == dt)))

def upsert_weight(s: Session, dt: str, weight_kg: float, ewma_kg: Optional[float]) -> Weight:
    w = s.get(Weight, dt)
    if w is None:
        w = Weight(dt=dt, weight_kg=weight_kg, ewma_kg=ewma_kg)
        s.add(w)
    else:
        w.weight_kg, w.ewma_kg = weight_kg, ewma_kg
    s.commit()
    return w

def upsert_workout(s: Session, dt: str, template: str, completed: int, minutes: int, sets: int, rpe: float) -> Workout:
    w = s.get(Workout, dt)
    if w is None:
        w = Workout(dt=dt, template=template, completed=completed, minutes=minutes, sets=sets, rpe=rpe)
        s.add(w)
    else:
        w.template, w.completed, w.minutes, w.sets, w.rpe = template, completed, minutes, sets, rpe
    s.commit()
    return w

def set_config(s: Session, key: str, value: str) -> None:
    c = s.get(Config, key)
    if c is None:
        s.add(Config(key=key, value=value))
    else:
        c.value = value
    s.commit()

def get_config(s: Session, key: str, default: Optional[str] = None) -> Optional[str]:
    c = s.get(Config, key)
    return c.value if c else default
