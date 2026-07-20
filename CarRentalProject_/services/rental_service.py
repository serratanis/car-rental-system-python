# services/rental_service.py
from datetime import datetime
from services.json_service import verileri_yukle, verileri_kaydet, CARS_FILE


def araci_sistemden_sil(plaka):
    araclar = verileri_yukle(CARS_FILE)
    # Seçilen plaka dışındaki araçları filtreleyerek yeni listeyi kaydet
    yeni_liste = [a for a in araclar if a["plaka"] != plaka]
    verileri_kaydet(CARS_FILE, yeni_liste)


def araci_iade_al(plaka):
    araclar = verileri_yukle(CARS_FILE)
    for arac in araclar:
        if arac["plaka"] == plaka and arac.get("durum") == "kirada":
            # İade işlemi: Aracı geçmişe kaydet
            gecmis = arac.get("gecmis", [])
            gecmis.append({
                "musteri": arac.get("kiralayan"),
                "baslangic": arac.get("baslangic"),
                "bitis": arac.get("bitis"),
                "iade_tarihi": datetime.now().strftime("%d.%m.%Y")
            })
            arac["gecmis"] = gecmis

            # Aracın durumunu sıfırla
            arac["durum"] = "müsait"
            arac["kiralayan"] = ""
            for key in ["baslangic", "bitis", "gun"]:
                arac.pop(key, None)
            break

    verileri_kaydet(CARS_FILE, araclar)


def araci_kirala(plaka, musteri, bas_tarih, bit_tarih):
    # Tarih formatlarını hesapla (Gün sayısını bul)
    bas = datetime.strptime(bas_tarih, "%d.%m.%Y")
    bit = datetime.strptime(bit_tarih, "%d.%m.%Y")
    gun_sayisi = (bit - bas).days + 1

    araclar = verileri_yukle(CARS_FILE)
    for arac in araclar:
        if arac["plaka"] == plaka:
            gunluk_ucret = int(arac.get("ucret", 0))
            toplam_fiyat = gun_sayisi * gunluk_ucret

            # Aracı kiraya ver
            arac["durum"] = "kirada"
            arac["kiralayan"] = musteri
            arac["baslangic"] = bas_tarih
            arac["bitis"] = bit_tarih
            arac["gun"] = gun_sayisi
            # Eski toplam ücretin üzerine ekle (Aracın toplam cirosu)
            arac["toplam_ucret"] = arac.get("toplam_ucret", 0) + toplam_fiyat
            break

    verileri_kaydet(CARS_FILE, araclar)

    # services/rental_service.py (Dosyanın sonuna eklenecek)

    def yeni_arac_ekle(plaka, marka, ucret):
        araclar = verileri_yukle(CARS_FILE)

        # Plakanın sistemde zaten olup olmadığını kontrol et
        for arac in araclar:
            if arac["plaka"] == plaka.upper().strip():
                return False, "Bu plakaya sahip bir araç zaten sistemde kayıtlı!"

        yeni_arac = {
            "plaka": plaka.upper().strip(),
            "marka": marka.strip(),
            "ucret": str(ucret),
            "durum": "müsait",
            "toplam_ucret": 0,
            "kiralayan": "",
            "gecmis": []
        }

        araclar.append(yeni_arac)
        verileri_kaydet(CARS_FILE, araclar)
        return True, "Araç sisteme başarıyla eklendi!"