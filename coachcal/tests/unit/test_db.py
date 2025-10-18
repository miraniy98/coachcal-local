from src.tools import db

def test_db_init_and_plan_roundtrip(tmp_path, monkeypatch):
    # point DB to a temp file
    test_db = tmp_path / "coach_state.db"
    monkeypatch.setattr(db, "DB_URL", f"sqlite:///{test_db}")
    # re-init engine with new URL
    from sqlmodel import create_engine
    db._engine = create_engine(db.DB_URL, echo=False)

    db.init_db()
    with db.session() as s:
        # upsert & get plan
        p = db.upsert_plan(s, "2025-08-23", 2150, 160, 60, 240, "Push Day")
        got = db.get_plan(s, "2025-08-23")
        assert got is not None
        assert got.kcal_target == 2150
        assert got.protein_g == 160

        # add meals
        db.add_meals(s, "2025-08-23", [
            {"item":"tofu (100g)", "grams":200, "kcal":170, "protein_g":20, "carbs_g":4, "fat_g":10}
        ])
        meals = db.get_meals(s, "2025-08-23")
        assert len(meals) == 1
        assert meals[0].kcal == 170

        # weight & workout
        w = db.upsert_weight(s, "2025-08-23", 94.6, 94.8)
        assert w.ewma_kg == 94.8
        wk = db.upsert_workout(s, "2025-08-23", "Push", 1, 45, 10, 7.5)
        assert wk.completed == 1

        # config
        db.set_config(s, "activity_factor", "1.35")
        assert db.get_config(s, "activity_factor") == "1.35"
