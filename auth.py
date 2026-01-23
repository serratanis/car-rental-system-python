import tkinter as tk
from tkinter import messagebox
from data_manager import DataManager

class GirişEkrani:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("Sistem Girişi")
        self.root.geometry("800x500")
        self.root.configure(bg="#f8f9fa")

        self.main_frame = tk.Frame(self.root, bg="white", padx=30, pady=30,
                                   highlightthickness=2, highlightbackground="#3498db")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.ana_ekran_olustur()

    def ana_ekran_olustur(self):
        for widget in self.main_frame.winfo_children(): widget.destroy()
        tk.Label(self.main_frame, text="🚗 Araç Kiralama Giriş", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=10)
        tk.Label(self.main_frame, text="Kullanıcı Adı:", bg="white").pack(anchor="w")
        self.ent_user = tk.Entry(self.main_frame, width=30); self.ent_user.pack(pady=5)
        tk.Label(self.main_frame, text="Şifre:", bg="white").pack(anchor="w")
        self.ent_pass = tk.Entry(self.main_frame, width=30, show="*"); self.ent_pass.pack(pady=5)
        tk.Button(self.main_frame, text="Giriş Yap", bg="#3498db", fg="white", font=("Segoe UI", 10, "bold"), width=25, command=self.giris_yap).pack(pady=15)
        tk.Button(self.main_frame, text="Yeni Kayıt Oluştur", bg="white", fg="#7f8c8d", font=("Segoe UI", 9, "underline"), bd=0, command=self.kayit_ekrani_olustur).pack()

    def kayit_ekrani_olustur(self):
        for widget in self.main_frame.winfo_children(): widget.destroy()
        tk.Label(self.main_frame, text="📝 Kayıt Ol", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=10)
        tk.Label(self.main_frame, text="Yeni Kullanıcı Adı:", bg="white").pack(anchor="w")
        self.reg_user = tk.Entry(self.main_frame, width=30); self.reg_user.pack(pady=5)
        tk.Label(self.main_frame, text="Yeni Şifre:", bg="white").pack(anchor="w")
        self.reg_pass = tk.Entry(self.main_frame, width=30, show="*"); self.reg_pass.pack(pady=5)
        tk.Button(self.main_frame, text="Kaydı Tamamla", bg="#2ecc71", fg="white", width=25, command=self.kayit_ol).pack(pady=15)
        tk.Button(self.main_frame, text="Giriş Ekranına Dön", bg="white", fg="#e74c3c", font=("Segoe UI", 9, "underline"), bd=0, command=self.ana_ekran_olustur).pack()

    def giris_yap(self):
        u, p = self.ent_user.get().strip(), self.ent_pass.get().strip()
        k = DataManager.kullanicilari_yukle()
        if u in k and k[u] == p: self.on_success()
        else: messagebox.showerror("Hata", "Giriş başarısız!")

    def kayit_ol(self):
        u, p = self.reg_user.get().strip(), self.reg_pass.get().strip()
        if not u or not p: return
        k = DataManager.kullanicilari_yukle()
        if u in k: messagebox.showerror("Hata", "Kullanıcı mevcut!"); return
        k[u] = p
        DataManager.kullanici_kaydet(k)
        messagebox.showinfo("Başarılı", "Kayıt tamam!"); self.ana_ekran_olustur()