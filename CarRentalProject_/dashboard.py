# dashboard.py
import customtkinter as ctk
from theme import COLORS, FONT, SIZE, WINDOW
from services.json_service import verileri_yukle, CARS_FILE
from ui.status_card import IstatistikKarti
from ui.vehicle_card import AracKarti
from ui.dialogs import AracDetayDialog
from ui.dialogs import AracDetayDialog, AracEkleDialog

class DashboardWindow(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.rol = rol
        self.username = username

        # Pencere Ayarları
        self.title(WINDOW["title"])
        self.geometry(f"{WINDOW['width']}x{WINDOW['height']}")
        self.minsize(WINDOW['min_width'], WINDOW['min_height'])
        self.configure(fg_color=COLORS["background"])

        self.araclar = verileri_yukle(CARS_FILE)

        self.sidebar_olustur()
        self.sag_icerik_olustur()

    def sidebar_olustur(self):
        self.sidebar = ctk.CTkFrame(self, width=SIZE["sidebar_width"], fg_color=COLORS["sidebar"], corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="🚗 RENT-CAR", font=FONT["title"], text_color=COLORS["white"]).pack(
            pady=(40, 10))
        ctk.CTkLabel(self.sidebar, text=f"👤 {self.username.capitalize()}\n[{self.rol.upper()}]", font=FONT["normal"],
                     text_color=COLORS["subtext"]).pack(pady=(0, 40))

        menuler = ["Dashboard", "Araçlar", "Kiralama", "Geçmiş", "Raporlar", "Ayarlar"]

        for menu in menuler:
            # Lambda kullanarak butona tıklandığında hangi menünün seçildiğini fonksiyona gönderiyoruz
            btn = ctk.CTkButton(self.sidebar, text=f"   {menu}", fg_color="transparent", text_color=COLORS["white"],
                                font=FONT["sidebar"], anchor="w", hover_color=COLORS["sidebar_hover"], height=40,
                                command=lambda m=menu: self.menuye_tiklandi(m))
            btn.pack(fill="x", padx=15, pady=2)

        # Çıkış butonunu ayrı ekle
        ctk.CTkButton(self.sidebar, text="   Çıkış", fg_color="transparent", text_color=COLORS["danger"],
                      font=FONT["sidebar"], anchor="w", hover_color="#451a1a", height=40,
                      command=self.destroy).pack(fill="x", padx=15, pady=(20, 2))

    # Dashboard sınıfının içine bu fonksiyonu mutlaka ekle
    def menuye_tiklandi(self, menu_adi):
        # 1. Mevcut tüm içeriği tamamen temizle
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # 2. Seçilen sayfayı yükle
        if menu_adi == "Dashboard":
            self.ekrani_yenile()
        elif menu_adi == "Araçlar":
            self.ekrani_yenile()
        elif menu_adi == "Kiralama":
            araclar = verileri_yukle(CARS_FILE)
            kiradakiler = [a for a in araclar if a["durum"] == "kirada"]
            self.kartlari_ciz(kiradakiler)
        elif menu_adi == "Geçmiş":
            from ui.history import GecmisSayfasi
            GecmisSayfasi(self.grid_frame, self.araclar)
        elif menu_adi == "Raporlar":
            from ui.reports import RaporlarSayfasi
            # self.grid_frame'i tam doldurması için parametreyi direkt gönderiyoruz
            RaporlarSayfasi(self.grid_frame, self.araclar)
        elif menu_adi == "Ayarlar":
            from ui.settings import AyarlarSayfasi
            AyarlarSayfasi(self.grid_frame, self.rol)
    def sag_icerik_olustur(self):
        self.main_content = ctk.CTkFrame(self, fg_color=COLORS["background"], corner_radius=0)
        self.main_content.pack(side="left", fill="both", expand=True, padx=SIZE["padding"], pady=SIZE["padding"])

        # --- İSTATİSTİK KARTLARI ---
        self.stats_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=(0, 20))
        self.istatistikleri_guncelle()

        # --- ARAMA ÇUBUĞU ---
        search_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 20))

        # Placeholder özelliği (Focus in/out hack'ine gerek kalmadı)
        self.ent_search = ctk.CTkEntry(search_frame, placeholder_text="🔍 Araç marka veya plaka ara...",
                                       font=FONT["normal"], height=SIZE["search_height"], width=400, corner_radius=8,
                                       fg_color=COLORS["search_bg"], border_color=COLORS["border"])
        self.ent_search.pack(side="left")
        self.ent_search.bind("<KeyRelease>", self.arama_yap)

        # Eğer rol Admin ise Yeni Araç Ekle butonu göster
        if self.rol == "admin":
            ctk.CTkButton(search_frame, text="✚ Yeni Araç Ekle", font=FONT["button"], fg_color=COLORS["success"],
                          hover_color="#059669", height=SIZE["search_height"],
                          command=self.yeni_arac_penceresi).pack(side="right")

        # --- ARAÇ KARTLARI BÖLÜMÜ (Aşağı Kaydırılabilir) ---
        self.grid_frame = ctk.CTkScrollableFrame(self.main_content, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True)

        self.kartlari_ciz(self.araclar)

    def istatistikleri_guncelle(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        toplam = len(self.araclar)
        kirada = len([a for a in self.araclar if a.get("durum") == "kirada"])
        musait = toplam - kirada
        gelir = sum([float(a.get("toplam_ucret", 0)) for a in self.araclar])

        IstatistikKarti(self.stats_frame, "Toplam Araç", str(toplam), COLORS["text"])
        IstatistikKarti(self.stats_frame, "Kirada", str(kirada), COLORS["danger"])
        IstatistikKarti(self.stats_frame, "Müsait", str(musait), COLORS["success"])
        IstatistikKarti(self.stats_frame, "Toplam Gelir", f"{gelir:,.0f} TL", COLORS["warning"])

    def arama_yap(self, event=None):
        sorgu = self.ent_search.get().lower().strip()
        if not sorgu:
            gosterilecek = self.araclar
        else:
            gosterilecek = [a for a in self.araclar if sorgu in a.get("marka", "").lower() or sorgu in a.get("plaka", "").lower()]

        self.kartlari_ciz(gosterilecek)

    def kartlari_ciz(self, arac_listesi):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        sutun_sayisi = 4

        # YENİ EKLENEN KISIM: Kalan boşluğu 4 sütuna eşit olarak dağıtır
        for i in range(sutun_sayisi):
            self.grid_frame.grid_columnconfigure(i, weight=1)

        for index, arac in enumerate(arac_listesi):
            row = index // sutun_sayisi
            col = index % sutun_sayisi

            # YENİ EKLENEN KISIM: sticky="n" ekleyerek kartları kendi hücresi içinde ortalıyoruz
            AracKarti(self.grid_frame, arac, self.arac_detay).grid(row=row, column=col, padx=10, pady=15, sticky="n")

    def arac_detay(self, plaka):
        secili_arac = next((a for a in self.araclar if a["plaka"] == plaka), None)
        if secili_arac:
            AracDetayDialog(self, secili_arac, self.rol, self.ekrani_yenile)
    def yeni_arac_penceresi(self):
        AracEkleDialog(self, self.ekrani_yenile)
    def ekrani_yenile(self):
        self.araclar = verileri_yukle(CARS_FILE)
        self.istatistikleri_guncelle()
        self.arama_yap(None)