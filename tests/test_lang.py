from language.lang import t

def test_translation_uk():
    assert t("clean", "uk") == "Очищення та оптимізація"

def test_translation_en():
    assert t("clean", "en") == "Cleaning & Optimization"