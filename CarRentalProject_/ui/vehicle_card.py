# ui/vehicle_card.py
import os
import customtkinter as ctk
from PIL import Image
from theme import COLORS, FONT, SIZE


def AracKarti(parent, arac, kiralama_cmd):
    # Kartı büyüttük: width=260, height=330
    kart = ctk.CTkFrame(parent, fg_color=COLORS["card"], width=260, height=330,
                        corner_radius=15, border_width=1, border_color=COLORS["border"])
    kart.grid_propagate(False)

    plaka = arac.get("plaka", "default")
    resim_yolu = f"assets/cars/{plaka}.png"

    if not os.path.exists(resim_yolu):
        resim_yolu = f"assets/cars/{plaka}.jpg"

    if not os.path.exists(resim_yolu):
        resim_yolu = "assets/cars/default.png"

    try:
        # Resmi de büyüttük: size=(230, 130)
        arac_resmi = Image.open(resim_yolu)
        resim_ctk = ctk.CTkImage(light_image=arac_resmi, dark_image=arac_resmi, size=(230, 130))

        resim_label = ctk.CTkLabel(kart, image=resim_ctk, text="")
        resim_label.pack(pady=(15, 5))
    except Exception:
        ikon = "🚗" if "sedan" in arac.get("marka", "").lower() else "🚙"
        ctk.CTkLabel(kart, text=ikon, font=("Segoe UI", 80)).pack(pady=(15, 5))

    ctk.CTkLabel(kart, text=arac.get("marka", "Bilinmeyen"), font=FONT["card_title"], text_color=COLORS["text"]).pack()
    ctk.CTkLabel(kart, text=arac.get("plaka", "00 XX 00"), font=FONT["card_text"], text_color=COLORS["subtext"]).pack()

    ctk.CTkLabel(kart, text=f"{arac.get('ucret', '0')} TL / Gün", font=FONT["heading"],
                 text_color=COLORS["primary"]).pack(pady=10)

    durum = arac.get("durum", "müsait").lower()
    durum_renk = COLORS["available_text"] if durum == "müsait" else COLORS["rented_text"]
    durum_bg = COLORS["available"] if durum == "müsait" else COLORS["rented"]
    durum_ikon = "🟢" if durum == "müsait" else "🔴"

    badge = ctk.CTkFrame(kart, fg_color=durum_bg, corner_radius=10)
    badge.pack(pady=5)
    ctk.CTkLabel(badge, text=f"{durum_ikon} {durum.capitalize()}", font=FONT["small"], text_color=durum_renk).pack(
        padx=10, pady=2)

    ctk.CTkButton(kart, text="İncele & İşlem", fg_color="transparent", text_color=COLORS["primary"],
                  hover_color=COLORS["hover"],
                  border_width=1, border_color=COLORS["primary"], font=FONT["button"],
                  command=lambda: kiralama_cmd(arac["plaka"])).pack(side="bottom", fill="x", padx=15, pady=(0, 15))

    return kart