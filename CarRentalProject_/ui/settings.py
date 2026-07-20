# ui/settings.py
import customtkinter as ctk
from tkinter import messagebox
from theme import COLORS, FONT

def AyarlarSayfasi(parent, rol):
    # ScrollableFrame değil, normal Frame kullanıyoruz.
    # Çünkü parent (grid_frame) zaten scroll özelliğine sahip.
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="both", expand=True)

    ctk.CTkLabel(frame, text="⚙️ Sistem Yönetim Paneli", font=("Arial", 28, "bold")).pack(anchor="w", padx=20, pady=20)

    # --- 1. GÜVENLİK ---
    k1 = ctk.CTkFrame(frame, fg_color=COLORS["card"], corner_radius=10)
    k1.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(k1, text="🔐 Hesap Güvenliği", font=FONT["card_title"]).pack(anchor="w", padx=20, pady=10)
    ctk.CTkEntry(k1, placeholder_text="Yeni Yönetici Şifresi", show="*").pack(fill="x", padx=20, pady=5)
    ctk.CTkButton(k1, text="Şifreyi Güncelle", fg_color=COLORS["primary"]).pack(anchor="e", padx=20, pady=15)

    # --- 2. TERCİHLER ---
    # ui/settings.py içindeki tercih kısmını bu şekilde güncelle
    k2 = ctk.CTkFrame(frame, fg_color=COLORS["card"], corner_radius=10)
    k2.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(k2, text="🛠️ Genel Tercihler", font=FONT["card_title"]).pack(anchor="w", padx=20, pady=10)

    # Tema switch'i için özel fonksiyon
    def tema_degistir(deger):
        if deger:  # Switch açıldıysa
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    # Switch'i oluştur
    tema_switch = ctk.CTkSwitch(k2, text="Karanlık Modu Kullan", font=FONT["normal"],
                                command=lambda: tema_degistir(tema_switch.get()))
    tema_switch.pack(anchor="w", padx=20, pady=8)

    # Mevcut modun durumuna göre switch'i ayarla
    if ctk.get_appearance_mode() == "Dark":
        tema_switch.select()

    # Diğer switch'ler...
    ctk.CTkSwitch(k2, text="Otomatik Yedekleme", font=FONT["normal"]).pack(anchor="w", padx=20, pady=8)
    ctk.CTkSwitch(k2, text="İşlem Onaylarını Göster", font=FONT["normal"]).pack(anchor="w", padx=20, pady=8)

    for txt in ["Otomatik Yedekleme", "İşlem Onayları", "Karanlık Mod", "Bildirimler"]:
        ctk.CTkSwitch(k2, text=txt, font=FONT["normal"]).pack(anchor="w", padx=20, pady=8)

    # --- 3. HAKKINDA ---
    k3 = ctk.CTkFrame(frame, fg_color=COLORS["card"], corner_radius=10)
    k3.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(k3, text="ℹ️ Sistem Hakkında", font=FONT["card_title"]).pack(anchor="w", padx=20, pady=10)
    ctk.CTkLabel(k3, text="Rent-Car Yönetim Sistemi v1.5.0\nMarmara Üniversitesi Projesi", text_color=COLORS["subtext"]).pack(anchor="w", padx=20, pady=(0, 20))

    # --- 4. SIFIRLA ---
    if rol == "admin":
        ctk.CTkButton(frame, text="⚠️ TÜM VERİTABANINI SIFIRLA", fg_color=COLORS["danger"], height=40).pack(fill="x", padx=20, pady=20)