import tkinter as tk
from auth import GirişEkrani
from app_logic import AracKiralamaApp

def uygulama_baslat(root_pencere):
    AracKiralamaApp(root_pencere)

if __name__ == "__main__":
    root = tk.Tk()

    app = GirişEkrani(root, on_success=lambda: uygulama_baslat(root))
    root.mainloop()