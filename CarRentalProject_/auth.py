# auth.py
import customtkinter as ctk
import tkinter as tk  # messagebox gibi araçlar için gerekli
from tkinter import messagebox
from theme import COLORS, FONT, SIZE, WINDOW
from services.json_service import verileri_yukle, verileri_kaydet, USERS_FILE


class LoginWindow(ctk.CTk):
    def __init__(self, on_success_callback): # <-- BURAYA CALLBACK EKLENDİ
        super().__init__()
        self.on_success_callback = on_success_callback

        # Pencere Ayarları
        self.title("Sistem Girişi")
        self.geometry(f"{WINDOW['width']}x{WINDOW['height']}")
        self.minsize(WINDOW['min_width'], WINDOW['min_height'])
        self.configure(fg_color=COLORS["background"])

        # Kart Görünümlü Ana Çerçeve
        self.main_frame = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=SIZE["radius"], width=450,
                                       height=480)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.main_frame.pack_propagate(False)

        # Json Dosya Yolu
        self.kullanici_dosyasi = USERS_FILE

        # İlk açılışta varsayılan admin hesabı ekle
        kullanicilar = verileri_yukle(self.kullanici_dosyasi)
        if "admin" not in kullanicilar:
            kullanicilar["admin"] = {"sifre": "1234", "rol": "admin"}
            verileri_kaydet(self.kullanici_dosyasi, kullanicilar)

        self.ekran_giris()

    def ekran_giris(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Araç Kiralama Giriş", font=FONT["title"], text_color=COLORS["text"]).pack(
            pady=(40, 30))

        ctk.CTkLabel(self.main_frame, text="Kullanıcı Adı:", text_color=COLORS["text"], font=FONT["normal"]).pack(
            anchor="w", padx=40)
        self.ent_user = ctk.CTkEntry(self.main_frame, width=350, height=SIZE["entry_height"], font=FONT["normal"])
        self.ent_user.pack(pady=5, padx=40)

        ctk.CTkLabel(self.main_frame, text="Şifre:", text_color=COLORS["text"], font=FONT["normal"]).pack(anchor="w",
                                                                                                          padx=40,
                                                                                                          pady=(15, 0))
        self.ent_pass = ctk.CTkEntry(self.main_frame, width=350, height=SIZE["entry_height"], show="*",
                                     font=FONT["normal"])
        self.ent_pass.pack(pady=5, padx=40)

        ctk.CTkButton(self.main_frame, text="Giriş Yap", fg_color=COLORS["primary"],
                      hover_color=COLORS["primary_hover"], text_color=COLORS["white"], font=FONT["button"],
                      height=SIZE["button_height"], command=self.giris_yap).pack(pady=(30, 15), padx=40, fill="x")

        ctk.CTkButton(self.main_frame, text="Yeni Müşteri Kaydı", fg_color="transparent", text_color=COLORS["primary"],
                      hover_color=COLORS["hover"], command=self.ekran_kayit).pack()

    def ekran_kayit(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Müşteri Kayıt", font=FONT["title"], text_color=COLORS["text"]).pack(
            pady=(40, 30))

        ctk.CTkLabel(self.main_frame, text="Kullanıcı Adı:", text_color=COLORS["text"], font=FONT["normal"]).pack(
            anchor="w", padx=40)
        self.reg_user = ctk.CTkEntry(self.main_frame, width=350, height=SIZE["entry_height"], font=FONT["normal"])
        self.reg_user.pack(pady=5, padx=40)

        ctk.CTkLabel(self.main_frame, text="Şifre:", text_color=COLORS["text"], font=FONT["normal"]).pack(anchor="w",
                                                                                                          padx=40,
                                                                                                          pady=(15, 0))
        self.reg_pass = ctk.CTkEntry(self.main_frame, width=350, height=SIZE["entry_height"], show="*",
                                     font=FONT["normal"])
        self.reg_pass.pack(pady=5, padx=40)

        ctk.CTkButton(self.main_frame, text="Kaydol", fg_color=COLORS["success"], hover_color="#059669",
                      text_color=COLORS["white"], font=FONT["button"], height=SIZE["button_height"],
                      command=self.kayit_ol).pack(pady=(30, 15), padx=40, fill="x")

        ctk.CTkButton(self.main_frame, text="Geri Dön", fg_color="transparent", text_color=COLORS["danger"],
                      hover_color="#FEE2E2", command=self.ekran_giris).pack()

    def kayit_ol(self):
        u, p = self.reg_user.get().strip(), self.reg_pass.get().strip()

        if not u or not p:
            return messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun!")

        kullanicilar = verileri_yukle(self.kullanici_dosyasi)

        if u in kullanicilar:
            return messagebox.showerror("Hata", "Kullanıcı mevcut!")

        kullanicilar[u] = {"sifre": p, "rol": "user"}
        verileri_kaydet(self.kullanici_dosyasi, kullanicilar)

        messagebox.showinfo("Başarılı", "Kayıt olundu!")
        self.ekran_giris()

    def giris_yap(self):
        u, p = self.ent_user.get().strip(), self.ent_pass.get().strip()
        kullanicilar = verileri_yukle(self.kullanici_dosyasi)

        if u in kullanicilar and kullanicilar[u]["sifre"] == p:
            rol = kullanicilar[u]["rol"]
            self.on_success(u, rol)
        else:
            messagebox.showerror("Hata", "Yanlış kullanıcı adı veya şifre!")

    def on_success(self, username, rol):
        # messagebox.showinfo("Giriş Başarılı", f"Hoş geldin, {username}!") # İstersen bu mesajı silebilirsin
        self.destroy()  # Giriş ekranını kapat
        self.on_success_callback(username, rol)  # Dashboard bağlanana kadar pencereyi kapat