# ==========================================================
# theme.py
# Araç Kiralama Sistemi v3.0
# Global Tema Dosyası
# ==========================================================

import customtkinter as ctk

# ----------------------------------------------------------
# Appearance
# ----------------------------------------------------------

ctk.set_appearance_mode("light")      # light / dark / system
ctk.set_default_color_theme("blue")


# ----------------------------------------------------------
# Renk Paleti
# ----------------------------------------------------------

COLORS = {

    # Ana renkler
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",

    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",

    # Arkaplanlar
    "background": "#F4F7FB",
    "card": "#FFFFFF",
    "sidebar": "#1E293B",
    "sidebar_hover": "#334155",

    # Yazılar
    "text": "#1F2937",
    "subtext": "#6B7280",
    "white": "#FFFFFF",

    # Kenarlık
    "border": "#E5E7EB",

    # Kart durumları
    "available": "#DCFCE7",
    "rented": "#FEE2E2",

    # Rozet
    "available_text": "#15803D",
    "rented_text": "#B91C1C",

    # Search
    "search_bg": "#FFFFFF",

    # Hover
    "hover": "#EFF6FF"
}


# ----------------------------------------------------------
# Fontlar
# ----------------------------------------------------------

FONT = {

    "title": ("Segoe UI", 24, "bold"),

    "subtitle": ("Segoe UI", 18, "bold"),

    "heading": ("Segoe UI", 15, "bold"),

    "normal": ("Segoe UI", 12),

    "small": ("Segoe UI", 10),

    "button": ("Segoe UI", 12, "bold"),

    "card_title": ("Segoe UI", 15, "bold"),

    "card_text": ("Segoe UI", 11),

    "stat_number": ("Segoe UI", 26, "bold"),

    "stat_text": ("Segoe UI", 12),

    "sidebar": ("Segoe UI", 13, "bold")
}


# ----------------------------------------------------------
# Boyutlar
# ----------------------------------------------------------

SIZE = {

    "sidebar_width": 240,

    "topbar_height": 80,

    "card_width": 280,

    "card_height": 260,

    "button_height": 42,

    "entry_height": 42,

    "search_height": 40,

    "icon": 22,

    "radius": 14,

    "padding": 20,

    "gap": 15
}


# ----------------------------------------------------------
# Dashboard Kartları
# ----------------------------------------------------------

STAT_CARDS = {

    "toplam": {

        "title": "Toplam Araç",
        "icon": "🚗",
        "color": COLORS["primary"]

    },

    "kirada": {

        "title": "Kiradaki",
        "icon": "🔑",
        "color": COLORS["danger"]

    },

    "musait": {

        "title": "Müsait",
        "icon": "✅",
        "color": COLORS["success"]

    },

    "gelir": {

        "title": "Toplam Gelir",
        "icon": "💰",
        "color": COLORS["warning"]

    }

}


# ----------------------------------------------------------
# Araç Durumları
# ----------------------------------------------------------

STATUS = {

    "müsait": {

        "text": "Müsait",

        "emoji": "🟢",

        "bg": COLORS["available"],

        "fg": COLORS["available_text"]

    },

    "kirada": {

        "text": "Kirada",

        "emoji": "🔴",

        "bg": COLORS["rented"],

        "fg": COLORS["rented_text"]

    }

}


# ----------------------------------------------------------
# Buton Renkleri
# ----------------------------------------------------------

BUTTON = {

    "primary": {

        "fg": COLORS["primary"],

        "hover": COLORS["primary_hover"]

    },

    "success": {

        "fg": COLORS["success"],

        "hover": "#059669"

    },

    "danger": {

        "fg": COLORS["danger"],

        "hover": "#DC2626"

    },

    "warning": {

        "fg": COLORS["warning"],

        "hover": "#D97706"

    }

}


# ----------------------------------------------------------
# Resim Dosyaları
# ----------------------------------------------------------

IMAGES = {

    "background": "assets/background.jpg",

    "logo": "assets/logo.png",

    "default_car": "assets/cars/default.png"

}


# ----------------------------------------------------------
# Sayfa Başlıkları
# ----------------------------------------------------------

PAGES = {

    "dashboard": "Dashboard",

    "vehicles": "Araçlar",

    "rentals": "Kiralama",

    "history": "Geçmiş",

    "reports": "Raporlar",

    "settings": "Ayarlar"

}


# ----------------------------------------------------------
# Pencere Ayarları
# ----------------------------------------------------------

WINDOW = {

    "title": "Araç Kiralama Yönetim Sistemi",

    "width": 1500,

    "height": 900,

    "min_width": 1200,

    "min_height": 750

}