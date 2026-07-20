# ui/history.py
import customtkinter as ctk
from theme import COLORS, FONT


def GecmisSayfasi(parent, araclar):
    # Ana çerçeve
    frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    frame.pack(fill="both", expand=True)

    ctk.CTkLabel(frame, text="🕒 Kiralama Geçmişi", font=FONT["title"], text_color=COLORS["text"]).pack(anchor="w",
                                                                                                       padx=20, pady=20)

    # Verileri işle
    for arac in araclar:
        gecmis_listesi = arac.get("gecmis", [])
        if gecmis_listesi:
            kart = ctk.CTkFrame(frame, fg_color=COLORS["card"], corner_radius=10)
            kart.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(kart, text=f"🚗 {arac.get('marka')} ({arac.get('plaka')})", font=FONT["normal"],
                         text_color=COLORS["primary"]).pack(anchor="w", padx=15, pady=(10, 0))

            for kayit in gecmis_listesi:
                ctk.CTkLabel(kart, text=f"• {kayit}", font=FONT["small"], text_color=COLORS["subtext"]).pack(anchor="w",
                                                                                                             padx=30,
                                                                                                             pady=2)