# main.py
import customtkinter as ctk
from auth import LoginWindow
from dashboard import DashboardWindow

def baslat_dashboard(username, rol):
    # Giriş başarılı olduğunda bu fonksiyon çalışır ve Dashboard'u açar
    app = DashboardWindow(username, rol)
    app.mainloop()

def main():
    # Tema ayarları
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Giriş ekranını oluştur ve başarı durumunda 'baslat_dashboard' fonksiyonunu tetikle
    app = LoginWindow(on_success_callback=baslat_dashboard)
    app.mainloop()

if __name__ == "__main__":
    main()