import customtkinter as ctk
from theme import COLORS, FONT


def IstatistikKarti(parent, baslik, deger, renk):
    kart = ctk.CTkFrame(parent, fg_color=COLORS["card"], corner_radius=10, border_width=1,
                        border_color=COLORS["border"])
    kart.pack(side="left", fill="both", expand=True, padx=10)

    ctk.CTkLabel(kart, text=baslik, font=FONT["stat_text"], text_color=COLORS["subtext"]).pack(pady=(15, 5))
    ctk.CTkLabel(kart, text=deger, font=FONT["stat_number"], text_color=renk).pack(pady=(0, 15))