import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from data_manager import DataManager


class AracKiralamaApp:
    def __init__(self, root):
        self.root = root
        for widget in self.root.winfo_children(): widget.destroy()
        self.root.title("Araç Kiralama Sistemi v8.5")
        self.root.geometry("1280x750")
        self.root.configure(bg="#f1f3f5")


        self.top_frame = tk.Frame(self.root, bg="white", padx=10, pady=10, highlightthickness=1,
                                  highlightbackground="#d1d1d1")
        self.top_frame.pack(pady=20, padx=20, fill="x")
        tk.Label(self.top_frame, text="🔍 Ara:", bg="white").pack(side="left", padx=5)
        self.ent_search = tk.Entry(self.top_frame, width=25);
        self.ent_search.pack(side="left", padx=5)
        self.ent_search.bind("<KeyRelease>", lambda e: self.listeyi_guncelle())
        self.combo_filter = ttk.Combobox(self.top_frame, values=["Hepsi", "Müsait", "Kirada"], state="readonly",
                                         width=10)
        self.combo_filter.set("Hepsi");
        self.combo_filter.pack(side="left", padx=15)
        self.combo_filter.bind("<<ComboboxSelected>>", lambda e: self.listeyi_guncelle())

        tk.Button(self.top_frame, text="🚪 Oturumu Kapat", bg="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"),
                  command=self.cikis_yap).pack(side="right", padx=10)


        self.tree_frame = tk.Frame(self.root);
        self.tree_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.tree = ttk.Treeview(self.tree_frame, columns=("plaka", "marka", "ucret", "durum", "tarih"),
                                 show='headings')
        style = ttk.Style();
        style.theme_use("clam")
        style.configure("Treeview", rowheight=35, font=('Segoe UI', 10))
        self.tree.tag_configure('musait', foreground="green", font=('Segoe UI', 10, 'bold'))
        self.tree.tag_configure('kirada', foreground="red")

        headers = {"plaka": "Plaka", "marka": "Marka/Model", "ucret": "Günlük Ücret", "durum": "Durum",
                   "tarih": "Kiralama Dönemi"}
        for col, txt in headers.items():
            self.tree.heading(col, text=txt);
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True)


        self.btn_frame = tk.Frame(self.root, bg="white", padx=10, pady=10, highlightthickness=1,
                                  highlightbackground="#d1d1d1")
        self.btn_frame.pack(pady=20, padx=20)
        btns = [
            ("✚ Araç Ekle", "#2ecc71", self.yeni_arac_formu),
            ("✏️ Düzenle", "#9b59b6", self.arac_duzenle),
            ("🔑 Kirala", "#3498db", self.arac_kirala),
            ("🔄 İade Al", "#f1c40f", self.arac_iade_et),
            ("📜 Geçmiş", "#7f8c8d", self.kiralama_gecmisi_goster),
            ("ℹ Detay", "#1abc9c", self.arac_detay),
            ("📊 Rapor", "#34495e", self.istatistik_goster),
            ("🗑 Araç Sil", "#e74c3c", self.arac_sil)
        ]
        for text, color, cmd in btns:
            tk.Button(self.btn_frame, text=text, bg=color, fg="white", font=('Segoe UI', 8, 'bold'), width=11, height=2,
                      relief="flat", command=cmd).pack(side="left", padx=3)

        self.listeyi_guncelle()

    def cikis_yap(self):
        if messagebox.askyesno("Çıkış", "Oturumu kapatıp giriş ekranına dönmek istediğinize emin misiniz?"):
            for widget in self.root.winfo_children(): widget.destroy()
            from auth import GirişEkrani
            from main import uygulama_baslat
            GirişEkrani(self.root, on_success=uygulama_baslat)

    def listeyi_guncelle(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        arama, filtre = self.ent_search.get().lower(), self.combo_filter.get()
        for a in DataManager.verileri_yukle():
            durum_raw = str(a.get("durum", "müsait")).lower()
            if (arama in a["plaka"].lower() or arama in a["marka"].lower()):
                if filtre == "Hepsi" or filtre == durum_raw.capitalize():
                    tag = 'kirada' if durum_raw == "kirada" else 'musait'
                    tarih = f"{a.get('baslangic', '')} / {a.get('bitis', '')}" if durum_raw == "kirada" else "-"
                    self.tree.insert("", "end",
                                     values=(a["plaka"], a["marka"], f"{a['ucret']} TL", durum_raw.capitalize(), tarih),
                                     tags=(tag,))

    def tarih_secici_arayuzu(self, parent):
        frame = tk.Frame(parent, bg="white");
        bugun = datetime.now()
        cg = ttk.Combobox(frame, values=[str(i).zfill(2) for i in range(1, 32)], width=3);
        cg.set(bugun.strftime("%d"));
        cg.pack(side="left", padx=2)
        ca = ttk.Combobox(frame, values=[str(i).zfill(2) for i in range(1, 13)], width=3);
        ca.set(bugun.strftime("%m"));
        ca.pack(side="left", padx=2)
        cy = ttk.Combobox(frame, values=[str(i) for i in range(bugun.year, bugun.year + 10)], width=5);
        cy.set(bugun.strftime("%Y"));
        cy.pack(side="left", padx=2)
        return frame, cg, ca, cy

    def validate_dates(self, b_str, bit_str):
        try:
            b, bi = datetime.strptime(b_str, "%d.%m.%Y"), datetime.strptime(bit_str, "%d.%m.%Y")
            if bi < b: messagebox.showerror("Hata", "Bitiş tarihi önce olamaz!"); return False
            return True
        except:
            return False

    def yeni_arac_formu(self):
        f = tk.Toplevel(self.root);
        f.title("Yeni Araç Ekle");
        f.geometry("400x650")
        tk.Label(f, text="Plaka:").pack(pady=5);
        ep = tk.Entry(f);
        ep.pack()
        tk.Label(f, text="Marka/Model:").pack(pady=5);
        em = tk.Entry(f);
        em.pack()
        tk.Label(f, text="Günlük Ücret:").pack(pady=5);
        eu = tk.Entry(f);
        eu.pack()
        tk.Label(f, text="Durum:").pack(pady=5);
        cd = ttk.Combobox(f, values=["Müsait", "Kirada"], state="readonly");
        cd.set("Müsait");
        cd.pack()
        extra_f = tk.Frame(f)
        tk.Label(extra_f, text="Müşteri Adı:").pack();
        en = tk.Entry(extra_f);
        en.pack()
        tk.Label(extra_f, text="Başlangıç:").pack();
        fb, gb, ab, yb = self.tarih_secici_arayuzu(extra_f);
        fb.pack()
        tk.Label(extra_f, text="Bitiş:").pack();
        fbi, gbi, abi, ybi = self.tarih_secici_arayuzu(extra_f);
        fbi.pack()
        cd.bind("<<ComboboxSelected>>",
                lambda e: extra_f.pack(pady=10) if cd.get() == "Kirada" else extra_f.pack_forget())

        def kaydet():
            v = DataManager.verileri_yukle()
            p, m, u = ep.get().upper().strip(), em.get().strip(), eu.get().strip()
            if not p or not m or not u: return
            res = {"plaka": p, "marka": m, "ucret": u, "durum": cd.get().lower(), "toplam_ucret": 0, "kiralayan": "",
                   "gecmis": []}
            if cd.get() == "Kirada":
                b_s, bi_s = f"{gb.get()}.{ab.get()}.{yb.get()}", f"{gbi.get()}.{abi.get()}.{ybi.get()}"
                if not self.validate_dates(b_s, bi_s): return
                gun = (datetime.strptime(bi_s, "%d.%m.%Y") - datetime.strptime(b_s, "%d.%m.%Y")).days + 1
                res.update(
                    {"kiralayan": en.get(), "baslangic": b_s, "bitis": bi_s, "gun": gun, "toplam_ucret": int(u) * gun})
            v.append(res);
            DataManager.verileri_kaydet(v);
            self.listeyi_guncelle();
            f.destroy()

        tk.Button(f, text="Kaydet", bg="#2ecc71", fg="white", font=("bold"), command=kaydet).pack(pady=20)

    def arac_duzenle(self):
        sec = self.tree.selection()
        if not sec: return
        plaka = self.tree.item(sec)["values"][0]
        veriler = DataManager.verileri_yukle()
        arac = next((a for a in veriler if a["plaka"] == plaka), None)
        if not arac: return
        df = tk.Toplevel(self.root);
        df.title(f"Düzenle: {plaka}");
        df.geometry("400x650")
        tk.Label(df, text="Marka/Model:").pack();
        em = tk.Entry(df);
        em.insert(0, arac["marka"]);
        em.pack()
        tk.Label(df, text="Günlük Ücret:").pack();
        eu = tk.Entry(df);
        eu.insert(0, arac["ucret"]);
        eu.pack()
        tk.Label(df, text="Durum:").pack();
        cd = ttk.Combobox(df, values=["müsait", "kirada"], state="readonly");
        cd.set(arac["durum"]);
        cd.pack()
        extra_df = tk.Frame(df);
        tk.Label(extra_df, text="Müşteri Adı:").pack();
        en = tk.Entry(extra_df);
        en.insert(0, arac.get("kiralayan", ""));
        en.pack()
        tk.Label(extra_df, text="Başlangıç Tarihi:").pack();
        fb, gb, ab, yb = self.tarih_secici_arayuzu(extra_df);
        fb.pack()
        tk.Label(extra_df, text="Bitiş Tarihi:").pack();
        fbi, gbi, abi, ybi = self.tarih_secici_arayuzu(extra_df);
        fbi.pack()
        cd.bind("<<ComboboxSelected>>",
                lambda e: extra_df.pack(pady=10) if cd.get() == "kirada" else extra_df.pack_forget())
        if arac["durum"] == "kirada": extra_df.pack(pady=10)

        def guncelle():
            arac["marka"], arac["ucret"], arac["durum"] = em.get(), eu.get(), cd.get()
            if cd.get() == "kirada":
                b_s, bi_s = f"{gb.get()}.{ab.get()}.{yb.get()}", f"{gbi.get()}.{abi.get()}.{ybi.get()}"
                if not self.validate_dates(b_s, bi_s): return
                arac.update({"kiralayan": en.get(), "baslangic": b_s, "bitis": bi_s})
            else:
                arac["kiralayan"] = ""
                for k in ["baslangic", "bitis", "gun"]: arac.pop(k, None)
            DataManager.verileri_kaydet(veriler);
            self.listeyi_guncelle();
            df.destroy()

        tk.Button(df, text="Güncelle", bg="#9b59b6", fg="white", command=guncelle).pack(pady=20)

    def arac_kirala(self):
        sec = self.tree.selection()
        if not sec or "Kirada" in self.tree.item(sec)["values"][3]: return
        v_tree = self.tree.item(sec)["values"]
        kp = tk.Toplevel(self.root);
        kp.title("Kiralama");
        kp.geometry("400x550")
        tk.Label(kp, text="Müşteri:").pack();
        en = tk.Entry(kp);
        en.pack()
        fb, gb, ab, yb = self.tarih_secici_arayuzu(kp);
        fb.pack()
        fbi, gbi, abi, ybi = self.tarih_secici_arayuzu(kp);
        fbi.pack()
        tutar_label = tk.Label(kp, text="Tutar: 0 TL", font=("Segoe UI", 12, "bold"), fg="#e67e22");
        tutar_label.pack(pady=20)

        def hesapla():
            b_s, bi_s = f"{gb.get()}.{ab.get()}.{yb.get()}", f"{gbi.get()}.{abi.get()}.{ybi.get()}"
            if not self.validate_dates(b_s, bi_s): return None
            gun = (datetime.strptime(bi_s, "%d.%m.%Y") - datetime.strptime(b_s, "%d.%m.%Y")).days + 1
            ucret = int(str(v_tree[2]).replace(" TL", ""))
            toplam = gun * ucret
            tutar_label.config(text=f"Toplam: {toplam} TL ({gun} Gün)")
            return toplam, gun, b_s, bi_s

        tk.Button(kp, text="Tutarı Hesapla", command=hesapla).pack()

        def onayla():
            res = hesapla()
            if not res: return
            toplam, gun, b_s, bi_s = res
            v = DataManager.verileri_yukle()
            for a in v:
                if a["plaka"] == v_tree[0]:
                    a.update({"durum": "kirada", "kiralayan": en.get(), "baslangic": b_s, "bitis": bi_s, "gun": gun,
                              "toplam_ucret": a.get("toplam_ucret", 0) + toplam})
            DataManager.verileri_kaydet(v);
            self.listeyi_guncelle();
            kp.destroy()

        tk.Button(kp, text="Onayla", bg="#3498db", fg="white", command=onayla).pack(pady=20)

    def arac_iade_et(self):
        sec = self.tree.selection()
        if not sec: return
        plaka = self.tree.item(sec)["values"][0]
        v = DataManager.verileri_yukle()
        for a in v:
            if a["plaka"] == str(plaka) and a["durum"] == "kirada":
                if "gecmis" not in a: a["gecmis"] = []
                a["gecmis"].append({"musteri": a.get("kiralayan", ""), "baslangic": a.get("baslangic", ""),
                                    "bitis": a.get("bitis", ""), "iade": datetime.now().strftime("%d.%m.%Y")})
                a["durum"] = "müsait";
                a["kiralayan"] = ""
                for k in ["baslangic", "bitis", "gun"]: a.pop(k, None)
        DataManager.verileri_kaydet(v);
        self.listeyi_guncelle();
        messagebox.showinfo("Bilgi", "İade alındı.")

    def kiralama_gecmisi_goster(self):
        sec = self.tree.selection()
        if not sec: return
        plaka = self.tree.item(sec)["values"][0]
        v = DataManager.verileri_yukle()
        arac = next((a for a in v if a["plaka"] == str(plaka)), None)
        if not arac or not arac.get("gecmis"): messagebox.showinfo("Geçmiş", "Kayıt yok."); return
        gp = tk.Toplevel(self.root);
        gp.geometry("700x400")
        t = ttk.Treeview(gp, columns=("m", "b", "bi", "i"), show='headings')
        t.heading("m", text="Müşteri");
        t.column("m", width=150)
        t.heading("b", text="Başlangıç");
        t.column("b", width=120)
        t.heading("bi", text="Planlanan");
        t.column("bi", width=120)
        t.heading("i", text="İade Tarihi");
        t.column("i", width=120)
        t.pack(fill="both", expand=True)
        for g in arac["gecmis"]: t.insert("", "end", values=(g["musteri"], g["baslangic"], g["bitis"], g["iade"]))

    def arac_detay(self):
        sec = self.tree.selection();
        plaka = self.tree.item(sec)["values"][0]
        a = next((x for x in DataManager.verileri_yukle() if x["plaka"] == plaka), None)
        if a: messagebox.showinfo("Detay",
                                  f"🚗 {a['marka']}\nPlaka: {a['plaka']}\nDurum: {a['durum'].upper()}\nKazanç: {a.get('toplam_ucret', 0)} TL")

    def arac_sil(self):
        sec = self.tree.selection()
        if sec and messagebox.askyesno('Sil', 'Emin misiniz?'):
            v = [a for a in DataManager.verileri_yukle() if a["plaka"] != self.tree.item(sec)["values"][0]]
            DataManager.verileri_kaydet(v);
            self.listeyi_guncelle()

    def istatistik_goster(self):
        v = DataManager.verileri_yukle()
        toplam = sum(float(a.get("toplam_ucret", 0)) for a in v)
        messagebox.showinfo("Rapor", f"📈 Toplam Ciro: {toplam:,.2f} TL")