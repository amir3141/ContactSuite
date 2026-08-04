from tkinter import ttk


PALETTE = {
    "background": "#F5F7FA",
    "surface": "#FFFFFF",
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "secondary": "#64748B",
    "text": "#1E293B",
    "border": "#D9E2EC",
    "success": "#16A34A",
    "danger": "#DC2626",
}


def apply_theme(root):
    root.configure(bg=PALETTE["background"])

    style = ttk.Style(root)

    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(
        ".",
        background=PALETTE["background"],
        foreground=PALETTE["text"],
        font=("Segoe UI", 10),
    )

    style.configure(
        "TFrame",
        background=PALETTE["background"],
    )

    style.configure(
        "TLabelframe",
        background=PALETTE["background"],
        borderwidth=1,
        relief="solid",
    )

    style.configure(
        "TLabelframe.Label",
        background=PALETTE["background"],
        foreground=PALETTE["text"],
        font=("Segoe UI Semibold", 11),
    )

    style.configure(
        "TLabel",
        background=PALETTE["background"],
        foreground=PALETTE["text"],
        font=("Segoe UI", 10),
    )

    style.configure(
        "TEntry",
        padding=6,
    )

    style.configure(
        "TButton",
        padding=(14, 8),
        font=("Segoe UI Semibold", 10),
    )

    style.map(
        "TButton",
        background=[
            ("active", PALETTE["primary_hover"]),
        ],
    )

    style.configure(
        "Treeview",
        rowheight=30,
        borderwidth=0,
        font=("Segoe UI", 10),
        background=PALETTE["surface"],
        fieldbackground=PALETTE["surface"],
    )

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI Semibold", 10),
        padding=8,
    )

    style.map(
        "Treeview",
        background=[
            ("selected", PALETTE["primary"]),
        ],
        foreground=[
            ("selected", "#FFFFFF"),
        ],
    )

    style.configure(
        "Horizontal.TScrollbar",
        arrowsize=14,
    )

    style.configure(
        "Vertical.TScrollbar",
        arrowsize=14,
    )