from src.tools.energy import bmr_msj, tdee, macros_from_kcal, ewma, kcal_totals

def test_bmr_tdee_macros():
    bmr = bmr_msj("male", weight_kg=95, height_cm=177, age=27)
    assert 1800 <= bmr <= 2200  # loose bounds

    maintenance = tdee(bmr, 1.35)
    assert maintenance > bmr

    macros = macros_from_kcal(2150, protein_g_target=160, fat_g_floor=60)
    assert macros["protein_g"] == 160
    assert macros["fat_g"] >= 60
    assert macros["carbs_g"] >= 0

def test_ewma_and_totals():
    e = ewma(None, 95.0, alpha=0.25)
    assert e == 95.0
    e2 = ewma(e, 94.6, alpha=0.25)
    assert round(e2, 2) <= 94.9

    totals = kcal_totals([
        {"kcal": 170, "protein_g": 20, "carbs_g": 4, "fat_g": 10},
        {"kcal": 100, "protein_g": 3,  "carbs_g": 17, "fat_g": 2},
    ])
    assert totals["kcal"] == 270
    assert totals["protein_g"] == 23
