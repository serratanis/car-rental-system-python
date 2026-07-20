# ui/forms.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from theme import COLORS, FONT
from services.rental_service import araci_kirala


class KiralamaFormu:
    def __init__(self, parent, arac, aktif_kullanici, on_success):
        self.arac = arac
        self.kullanici = aktif_kullanici
        self.on_success = on_success

        self.form = tk.Toplevel(parent)
        self.form.title(f"Kiralama İşlemi - {arac['plaka']}")
        self.form.geometry("350x450")
        self.form.configure(bg=COLORS["card_bg"])
        self.form.resizable(False, False)
        self.form.grab_set()  # Modal pencere

        self.arayuz_olustur()

    def tarih_secici(self, parent):
        frame = tk.Frame(parent, bg=COLORS["card_bg"])
        bugun = datetime.now()

        gunler = [str(i).zfill(2) for i in range(1, 32)]
        aylar = [str(i).zfill(2) for i in range(1, 13)]
        yillar = [str(i) for i in range(bugun.year, bugun.year + 3)]

        c_gun = ttk.Combobox(frame, values=gunler, width=3, state="readonly")
        c_gun.set(bugun.strftime("%d"))
        c_gun.pack(side="left", padx=2)

        c_ay = ttk.Combobox(frame, values=aylar, width=3, state="readonly")
        c_ay.set(bugun.strftime("%m"))
        c_ay.pack(side="left", padx=2)

        c_yil = ttk.Combobox(frame, values=yillar, width=5, state="readonly")
        c_yil.set(bugun.strftime("%Y"))
        c_yil.pack(side="left", padx=2)

        return frame, c_gun, c_ay, c_yil

    def arayuz_olustur(self):
        tk.Label(self.form, text="Araç Kiralama", font=FONTS["h1"], bg=COLORS["card_bg"], fg=COLORS["primary"]).pack(
            pady=20)

        tk.Label(self.form, text=f"Araç: {self.arac.get('marka')} ({self.arac.get('ucret')} TL/Gün)",
                 font=FONTS["body_bold"], bg=COLORS["card_bg"]).pack(pady=5)

        tk.Label(self.form, text="Müşteri Adı:", bg=COLORS["card_bg"], font=FONTS["body"]).pack(anchor="w", padx=40,
                                                                                                pady=(10, 0))
        self.ent_musteri = tk.Entry(self.form, width=30, font=FONTS["body"])
        self.ent_musteri.insert(0, self.kullanici)  # Giriş yapan kullanıcıyı otomatik yazdır
        self.ent_musteri.pack(pady=5)

        tk.Label(self.form, text="Başlangıç Tarihi:", bg=COLORS["card_bg"], font=FONTS["body"]).pack(anchor="w",
                                                                                                     padx=40,
                                                                                                     pady=(10, 0))
        f_bas, self.g_bas, self.a_bas, self.y_bas = self.tarih_secici(self.form)
        f_bas.pack()

        tk.Label(self.form, text="Bitiş Tarihi:", bg=COLORS["card_bg"], font=FONTS["body"]).pack(anchor="w", padx=40,
                                                                                                 pady=(10, 0))
        f_bit, self.g_bit, self.a_bit, self.y_bit = self.tarih_secici(self.form)
        f_bit.pack()

        tk.Button(self.form, text="Kiralamayı Onayla", bg=COLORS["success"], fg="white", font=FONTS["body_bold"],
                  width=20, pady=8, command=self.islemi_tamamla).pack(pady=30)

    def islemi_tamamla(self):
        musteri = self.ent_musteri.get().strip()
        bas_str = f"{self.g_bas.get()}.{self.a_bas.get()}.{self.y_bas.get()}"
        bit_str = f"{self.g_bit.get()}.{self.a_bit.get()}.{self.y_bit.get()}"

        if not musteri:
            return messagebox.showwarning("Uyarı", "Müşteri adı boş olamaz!", parent=self.form)

        try:
            # Tarihlerin mantığını kontrol et
            bas_date = datetime.strptime(bas_str, "%d.%m.%Y")
            bit_date = datetime.strptime(bit_str, "%d.%m.%Y")
            if bit_date < bas_date:
                return messagebox.showerror("Hata", "Bitiş tarihi, başlangıç tarihinden önce olamaz!", parent=self.form)
        except ValueError:
            return messagebox.showerror("Hata", "Geçersiz tarih!", parent=self.form)

        # Her şey doğruysa servisi çağır
        araci_kirala(self.arac["plaka"], musteri, bas_str, bit_str)
        messagebox.showinfo("Başarılı", "Araç başarıyla kiralandı!", parent=self.form)

        self.form.destroy()
        self.on_success()  # Dashboard'u yenile
        # ui/forms.py (Dosyanın sonuna eklenecek)
        from services.rental_service import yeni_arac_ekle  # En üste import eklemeyi unutma

        class AracEkleFormu:
            def __init__(self, parent, on_success):
                self.on_success = on_success

                self.form = tk.Toplevel(parent)
                self.form.title("Yeni Araç Ekle")
                self.form.geometry("350x450")
                self.form.configure(bg=COLORS["card_bg"])
                self.form.resizable(False, False)
                self.form.grab_set()  # Modal pencere

                self.arayuz_olustur()

            def arayuz_olustur(self):
                tk.Label(self.form, text="✚ Yeni Araç Ekle", font=FONTS["h1"], bg=COLORS["card_bg"],
                         fg=COLORS["primary"]).pack(pady=20)

                tk.Label(self.form, text="Araç Marka ve Modeli:", bg=COLORS["card_bg"], font=FONTS["body"]).pack(
                    anchor="w", padx=40, pady=(10, 0))
                self.ent_marka = tk.Entry(self.form, width=30, font=FONTS["body"])
                self.ent_marka.pack(pady=5)

                tk.Label(self.form, text="Plaka:", bg=COLORS["card_bg"], font=FONTS["body"]).pack(anchor="w", padx=40,
                                                                                                  pady=(10, 0))
                self.ent_plaka = tk.Entry(self.form, width=30, font=FONTS["body"])
                self.ent_plaka.pack(pady=5)

                tk.Label(self.form, text="Günlük Kiralama Ücreti (TL):", bg=COLORS["card_bg"], font=FONTS["body"]).pack(
                    anchor="w", padx=40, pady=(10, 0))
                self.ent_ucret = tk.Entry(self.form, width=30, font=FONTS["body"])
                self.ent_ucret.pack(pady=5)

                tk.Button(self.form, text="Sisteme Kaydet", bg=COLORS["success"], fg="white", font=FONTS["body_bold"],
                          width=20, pady=8, command=self.kaydet).pack(pady=30)

            def kaydet(self):
                marka = self.ent_marka.get().strip()
                plaka = self.ent_plaka.get().strip()
                ucret = self.ent_ucret.get().strip()

                # Basit Validasyon (Doğrulama)
                if not marka or not plaka or not ucret:
                    return messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!", parent=self.form)

                if not ucret.isdigit():
                    return messagebox.showerror("Hata", "Ücret sadece rakamlardan oluşmalıdır!", parent=self.form)

                # Servisi çağır
                basarili_mi, mesaj = yeni_arac_ekle(plaka, marka, ucret)

                if basarili_mi:
                    messagebox.showinfo("Başarılı", mesaj, parent=self.form)
                    self.form.destroy()
                    self.on_success()  # Ekranı (Dashboard) yenile
                else:
                    messagebox.showerror("Hata", mesaj, parent=self.form)