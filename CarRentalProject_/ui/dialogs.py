# ui/dialogs.py
import customtkinter as ctk
from tkinter import messagebox
import datetime
from theme import COLORS, FONT, SIZE
from services.json_service import verileri_yukle, verileri_kaydet, CARS_FILE
import os
import shutil
from tkinter import filedialog

class AracDetayDialog(ctk.CTkToplevel):
    def __init__(self, parent, arac, rol, on_update_callback):
        super().__init__(parent)
        self.parent = parent
        self.arac = arac
        self.rol = rol
        self.on_update_callback = on_update_callback

        self.title(f"Araç Detayı - {self.arac.get('plaka')}")
        self.geometry("450x650")
        self.configure(fg_color=COLORS["background"])

        self.transient(parent)
        self.grab_set()

        self.arayuz_olustur()

    def arayuz_olustur(self):
        # Ana çerçeveyi burada tanımlıyoruz
        main_frame = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=SIZE["radius"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="📄 Araç Detayları", font=FONT["title"], text_color=COLORS["text"]).pack(
            pady=(20, 15))

        # Bilgiler listesi
        bilgiler = [
            ("Plaka", self.arac.get("plaka", "Bilinmiyor")),
            ("Marka", self.arac.get("marka", "Bilinmiyor")),
            ("Günlük Ücret", f"{self.arac.get('ucret', 0)} TL"),
            ("Durum", self.arac.get("durum", "müsait").capitalize()),
            ("Toplam Gelir", f"{self.arac.get('toplam_ucret', 0):,.0f} TL")
        ]

        for baslik, deger in bilgiler:
            satir = ctk.CTkFrame(main_frame, fg_color="transparent")
            satir.pack(fill="x", padx=30, pady=5)
            ctk.CTkLabel(satir, text=f"{baslik}:", font=FONT["normal"], text_color=COLORS["subtext"]).pack(side="left")

            renk = COLORS["success"] if deger == "Müsait" else COLORS["danger"] if deger == "Kirada" else COLORS["text"]
            ctk.CTkLabel(satir, text=deger, font=FONT["normal"], text_color=renk).pack(side="right")

        ctk.CTkFrame(main_frame, height=2, fg_color=COLORS["border"]).pack(fill="x", padx=20, pady=15)

        # --- DURUMA GÖRE İŞLEM ---
        if self.arac.get("durum") == "müsait":
            ctk.CTkLabel(main_frame, text="Müşteri Adı:", font=FONT["normal"], text_color=COLORS["text"]).pack(
                anchor="w", padx=30)
            self.ent_musteri = ctk.CTkEntry(main_frame, font=FONT["normal"], height=SIZE["entry_height"])
            self.ent_musteri.pack(fill="x", padx=30, pady=(0, 10))

            ctk.CTkLabel(main_frame, text="Başlangıç Tarihi (GG.AA.YYYY):", font=FONT["normal"],
                         text_color=COLORS["text"]).pack(anchor="w", padx=30)
            self.ent_tarih = ctk.CTkEntry(main_frame, font=FONT["normal"], height=SIZE["entry_height"])
            self.ent_tarih.insert(0, datetime.date.today().strftime("%d.%m.%Y"))
            self.ent_tarih.pack(fill="x", padx=30, pady=(0, 10))

            ctk.CTkLabel(main_frame, text="Kiralama Süresi (Gün):", font=FONT["normal"],
                         text_color=COLORS["text"]).pack(anchor="w", padx=30)
            self.ent_gun = ctk.CTkEntry(main_frame, font=FONT["normal"], height=SIZE["entry_height"])
            self.ent_gun.pack(fill="x", padx=30, pady=(0, 20))

            ctk.CTkButton(main_frame, text="Aracı Kirala", font=FONT["button"], height=SIZE["button_height"],
                          fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], command=self.kirala).pack(
                fill="x", padx=30, pady=(0, 10))
        else:
            ctk.CTkLabel(main_frame, text=f"Mevcut Kiralayan: {self.arac.get('kiralayan')}", font=FONT["normal"],
                         text_color=COLORS["danger"]).pack(pady=5)
            ctk.CTkLabel(main_frame, text=f"Kira Tarihi: {self.arac.get('baslangic')} - {self.arac.get('bitis')}",
                         font=FONT["normal"], text_color=COLORS["subtext"]).pack(pady=(0, 20))

            ctk.CTkButton(main_frame, text="Aracı İade Al", font=FONT["button"], height=SIZE["button_height"],
                          fg_color=COLORS["warning"], hover_color="#D97706", text_color=COLORS["text"],
                          command=self.iade_al).pack(fill="x", padx=30, pady=(0, 10))

        if self.rol == "admin":
            ctk.CTkButton(main_frame, text="🗑️ Aracı Sistemden Sil", font=FONT["button"], height=SIZE["button_height"],
                          fg_color="transparent", text_color=COLORS["danger"], border_width=1,
                          border_color=COLORS["danger"],
                          hover_color="#FEE2E2", command=self.araci_sil).pack(fill="x", padx=30, pady=(10, 10))

    def kirala(self):
        musteri = self.ent_musteri.get().strip()
        tarih_str = self.ent_tarih.get().strip()
        gun_str = self.ent_gun.get().strip()

        if not musteri or not tarih_str or not gun_str:
            return messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")

        try:
            baslangic = datetime.datetime.strptime(tarih_str, "%d.%m.%Y").date()
            gun = int(gun_str)
            bitis = baslangic + datetime.timedelta(days=gun)
        except:
            return messagebox.showerror("Hata", "Tarih formatı hatalı (GG.AA.YYYY) veya gün sayısı geçersiz!")

        toplam_ucret = gun * int(self.arac.get("ucret", 0))

        if messagebox.askyesno("Kiralama Onayı", f"Toplam Ücret: {toplam_ucret} TL. Onaylıyor musunuz?"):
            araclar = verileri_yukle(CARS_FILE)
            for a in araclar:
                if a["plaka"] == self.arac["plaka"]:
                    a["durum"] = "kirada"
                    a["kiralayan"] = musteri
                    a["baslangic"] = baslangic.strftime("%d.%m.%Y")
                    a["bitis"] = bitis.strftime("%d.%m.%Y")
                    a["toplam_ucret"] = a.get("toplam_ucret", 0) + toplam_ucret
                    a.setdefault("gecmis", []).append(f"{baslangic.strftime('%d.%m.%Y')} - {musteri} ({gun} gün)")
                    break
            verileri_kaydet(CARS_FILE, araclar)
            self.on_update_callback()
            self.destroy()

    def iade_al(self):
        if messagebox.askyesno("İade Onayı", "Aracı teslim alıyorsunuz?"):
            araclar = verileri_yukle(CARS_FILE)
            for a in araclar:
                if a["plaka"] == self.arac["plaka"]:
                    a["durum"] = "müsait"
                    a["kiralayan"] = ""
                    a["baslangic"] = ""
                    a["bitis"] = ""
                    break
            verileri_kaydet(CARS_FILE, araclar)
            self.on_update_callback()
            self.destroy()

    def araci_sil(self):
        if self.arac.get("durum") == "kirada":
            return messagebox.showerror("Hata", "Kirada olan araç silinemez.")
        if messagebox.askyesno("Silme", "Emin misiniz?"):
            araclar = verileri_yukle(CARS_FILE)
            araclar = [a for a in araclar if a["plaka"] != self.arac["plaka"]]
            verileri_kaydet(CARS_FILE, araclar)
            self.on_update_callback()
            self.destroy()


class AracEkleDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_update_callback):
        super().__init__(parent)
        self.parent = parent
        self.on_update_callback = on_update_callback

        self.title("Yeni Araç Ekle")
        self.geometry("400x550")
        self.configure(fg_color=COLORS["background"])

        self.transient(parent)
        self.grab_set()

        self.secilen_gorsel_yolu = None
        self.arayuz_olustur()

    def arayuz_olustur(self):
        main_frame = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="✚ Yeni Araç Bilgileri", font=FONT["title"]).pack(pady=(20, 20))

        # Giriş Alanları
        self.ent_plaka = ctk.CTkEntry(main_frame, placeholder_text="Plaka (Örn: 34 ABC 01)", height=40)
        self.ent_plaka.pack(fill="x", padx=20, pady=10)

        self.ent_marka = ctk.CTkEntry(main_frame, placeholder_text="Marka ve Model (Örn: Renault Clio)", height=40)
        self.ent_marka.pack(fill="x", padx=20, pady=10)

        self.ent_ucret = ctk.CTkEntry(main_frame, placeholder_text="Günlük Ücret (TL)", height=40)
        self.ent_ucret.pack(fill="x", padx=20, pady=10)

        # Görsel Seçici Butonu
        self.btn_gorsel = ctk.CTkButton(main_frame, text="📷 Bilgisayardan Görsel Seç",
                                        fg_color="transparent", border_width=1, text_color=COLORS["text"],
                                        command=self.gorsel_sec)
        self.btn_gorsel.pack(fill="x", padx=20, pady=15)

        self.lbl_gorsel_isim = ctk.CTkLabel(main_frame, text="Henüz görsel seçilmedi.", text_color=COLORS["subtext"],
                                            font=FONT["small"])
        self.lbl_gorsel_isim.pack(pady=(0, 10))

        # Kaydet Butonu
        ctk.CTkButton(main_frame, text="Aracı Kaydet", fg_color=COLORS["success"], hover_color="#059669",
                      height=45, command=self.kaydet).pack(fill="x", padx=20, pady=(20, 10))

    def gorsel_sec(self):
        dosya_yolu = filedialog.askopenfilename(
            title="Araç Görseli Seç",
            filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg")]
        )
        if dosya_yolu:
            self.secilen_gorsel_yolu = dosya_yolu
            dosya_adi = os.path.basename(dosya_yolu)
            self.lbl_gorsel_isim.configure(text=f"Seçilen: {dosya_adi}", text_color=COLORS["success"])

    def kaydet(self):
        plaka = self.ent_plaka.get().strip().upper()
        marka = self.ent_marka.get().strip()
        ucret = self.ent_ucret.get().strip()

        if not plaka or not marka or not ucret:
            return messagebox.showwarning("Eksik Bilgi", "Lütfen plaka, marka ve ücret alanlarını doldurun.")

        if not ucret.isdigit():
            return messagebox.showerror("Hata", "Günlük ücret sadece rakamlardan oluşmalıdır.")

        araclar = verileri_yukle(CARS_FILE)

        # Plaka çakışma kontrolü
        if any(a["plaka"] == plaka for a in araclar):
            return messagebox.showerror("Hata", "Bu plakaya sahip bir araç zaten mevcut!")

        # Eğer görsel seçildiyse, assets klasörüne plaka adıyla kopyala
        if self.secilen_gorsel_yolu:
            hedef_klasor = os.path.join(os.getcwd(), "assets", "cars")
            os.makedirs(hedef_klasor, exist_ok=True)  # Klasör yoksa oluştur

            # Sistemin rahat okuması için uzantıyı png yapıyoruz
            hedef_dosya = os.path.join(hedef_klasor, f"{plaka}.png")
            try:
                shutil.copy(self.secilen_gorsel_yolu, hedef_dosya)
            except Exception as e:
                print(f"Resim kopyalanamadı: {e}")

        # Yeni aracı veritabanına ekle
        yeni_arac = {
            "plaka": plaka,
            "marka": marka,
            "ucret": int(ucret),
            "durum": "müsait",
            "toplam_ucret": 0,
            "kiralayan": "",
            "baslangic": "",
            "bitis": "",
            "gecmis": []
        }

        araclar.append(yeni_arac)
        verileri_kaydet(CARS_FILE, araclar)

        messagebox.showinfo("Başarılı", "Araç sisteme başarıyla eklendi!")
        self.on_update_callback()  # Dashboard'u güncelle
        self.destroy()