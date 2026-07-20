# ui/reports.py
import customtkinter as ctk
from theme import COLORS, FONT


def RaporlarSayfasi(parent, araclar):
    # Scrollable frame yerine doğrudan bir frame kullanarak alanı tam yönetiyoruz
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(frame, text="📊 Detaylı Sistem Raporları", font=FONT["title"]).pack(anchor="w", pady=(0, 20))

    # İstatistik Hesaplamaları
    toplam = len(araclar)
    kirada = len([a for a in araclar if a.get("durum") == "kirada"])
    toplam_gelir = sum([float(a.get("toplam_ucret", 0)) for a in araclar])
    verimlilik = (kirada / toplam * 100) if toplam > 0 else 0

    # Kartları tutacak kapsayıcı
    grid_container = ctk.CTkFrame(frame, fg_color="transparent")
    grid_container.pack(fill="x", pady=10)

    # 4 Sütunlu Grid Yapısı
    for i in range(4):
        grid_container.grid_columnconfigure(i, weight=1)

    for i, (baslik, deger, renk) in enumerate([
        ("Toplam Araç", toplam, COLORS["text"]),
        ("Kiradaki Araç", kirada, COLORS["danger"]),
        ("Toplam Gelir", f"{toplam_gelir:,.0f} TL", COLORS["warning"]),
        ("Doluluk Oranı", f"%{verimlilik:.1f}", COLORS["success"])
    ]):
        k = ctk.CTkFrame(grid_container, fg_color=COLORS["card"], height=120)
        k.grid(row=0, column=i, padx=5, sticky="ew")
        ctk.CTkLabel(k, text=baslik, font=FONT["small"]).pack(pady=(25, 5))
        ctk.CTkLabel(k, text=deger, font=FONT["card_title"], text_color=renk).pack()

    # Araç Bazlı Liste
    ctk.CTkLabel(frame, text="📋 Araç Bazlı Performans Listesi", font=FONT["card_title"]).pack(anchor="w", pady=(30, 10))

    # Liste için kaydırılabilir bir alan
    list_frame = ctk.CTkScrollableFrame(frame, fg_color=COLORS["card"])
    list_frame.pack(fill="both", expand=True)

    for a in araclar:
        satir = ctk.CTkFrame(list_frame, fg_color="transparent")
        satir.pack(fill="x", pady=5, padx=10)
        ctk.CTkLabel(satir, text=f"• {a['plaka']} - {a['marka']}", font=FONT["normal"]).pack(side="left")
        ctk.CTkLabel(satir, text=f"{a.get('toplam_ucret', 0)} TL", font=FONT["normal"],
                     text_color=COLORS["primary"]).pack(side="right")