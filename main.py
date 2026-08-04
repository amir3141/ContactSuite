import tkinter as tk

from dashboard import ContactBookApplication


def run():
    window = tk.Tk()
    application = ContactBookApplication(window)
    window.protocol("WM_DELETE_WINDOW", application.shutdown)
    window.mainloop()


if __name__ == "__main__":
    run()