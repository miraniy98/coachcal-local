from __future__ import annotations
from typing import Optional, Dict

# ----- BMR / TDEE -----

def bmr_msj(sex: str, weight_kg: float, height_cm: float, age: int) -> float:
    sex = sex.lower().strip()
    if sex.startswith("m"):
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

def tdee(bmr: float, activity_factor: float) -> float:
    return bmr * activity_factor

# ----- Macros -----

def macros_from_kcal(kcal: int, protein_g_target: int, fat_g_floor: int) -> Dict[str, int]:
    kcal_from_pro = protein_g_target * 4
    kcal_from_fat = max(fat_g_floor * 9, int(0.25 * kcal))  # ensure ≥25% kcal from fat
    carb_kcal = max(0, kcal - kcal_from_pro - kcal_from_fat)
    return dict(
        protein_g=int(protein_g_target),
        fat_g=int(round(kcal_from_fat / 9)),
        carbs_g=int(round(carb_kcal / 4)),
    )

# ----- EWMA -----

def ewma(prev: Optional[float], x: float, alpha: float = 0.25) -> float:
    return x if prev is None else alpha * x + (1 - alpha) * prev

# ----- Totals from items -----

def kcal_totals(items: list[dict]) -> Dict[str, int]:
    kcal = int(round(sum(i.get("kcal", 0.0) for i in items)))
    p = int(round(sum(i.get("protein_g", 0.0) for i in items)))
    c = int(round(sum(i.get("carbs_g", 0.0) for i in items)))
    f = int(round(sum(i.get("fat_g", 0.0) for i in items)))
    return {"kcal": kcal, "protein_g": p, "carbs_g": c, "fat_g": f}
