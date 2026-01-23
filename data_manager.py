import json

class DataManager:
    @staticmethod
    def verileri_yukle():
        try:
            with open("veriler.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []

    @staticmethod
    def verileri_kaydet(veriler):
        with open("veriler.json", "w", encoding="utf-8") as f:
            json.dump(veriler, f, ensure_ascii=False, indent=4)

    @staticmethod
    def kullanicilari_yukle():
        try:
            with open("kullanicilar.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}

    @staticmethod
    def kullanici_kaydet(veriler):
        with open("kullanicilar.json", "w", encoding="utf-8") as f:
            json.dump(veriler, f, ensure_ascii=False, indent=4)