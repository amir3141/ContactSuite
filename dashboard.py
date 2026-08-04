import tkinter as tk
from tkinter import ttk, messagebox

from repository import ContactRepository
from contact_manager import ContactService
from entities import Contact
from apperance import apply_theme
from windows import SearchDialog
from document_exporter import ExportService
from qr_generator import QRService
from storage_manager import BackupService


class ContactBookApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("1150x720")

        apply_theme(self.root)

        self.service = ContactService(ContactRepository())
        self.exporter = ExportService(self.service)
        self.qr = QRService(self.service)
        self.backup = BackupService(self.service)

        self.current_contact = None

        self.fields = {
            "first_name": tk.StringVar(),
            "last_name": tk.StringVar(),
            "mobile": tk.StringVar(),
            "landline": tk.StringVar(),
            "address": tk.StringVar(),
            "notes": tk.StringVar(),
        }

        self.status = tk.StringVar()

        self._build_menu()
        self._build_form()
        self._build_table()
        self._build_statusbar()

        self.refresh()

    def _build_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=False)

        file_menu.add_command(
            label="Export Contacts",
            command=self.exporter.export_all_pdf,
        )

        file_menu.add_command(
            label="Export Selected",
            command=self.export_selected,
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Backup",
            command=self.backup.create_backup,
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.shutdown,
        )

        menu.add_cascade(label="File", menu=file_menu)

    def _build_form(self):
        frame = ttk.LabelFrame(
            self.root,
            text="Contact Information",
            padding=15,
        )

        frame.pack(fill="x", padx=15, pady=15)

        labels = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Mobile", "mobile"),
            ("Landline", "landline"),
            ("Address", "address"),
            ("Notes", "notes"),
        ]

        for index, (title, key) in enumerate(labels):
            ttk.Label(frame, text=title).grid(
                row=index,
                column=0,
                sticky="w",
                pady=6,
            )

            ttk.Entry(
                frame,
                textvariable=self.fields[key],
                width=55,
            ).grid(
                row=index,
                column=1,
                padx=10,
                pady=6,
                sticky="ew",
            )

        buttons = ttk.Frame(frame)
        buttons.grid(
            row=0,
            column=2,
            rowspan=6,
            padx=20,
            sticky="ns",
        )

        ttk.Button(
            buttons,
            text="Save",
            command=self.save_contact,
        ).pack(fill="x", pady=4)

        ttk.Button(
            buttons,
            text="Edit",
            command=self.load_selected,
        ).pack(fill="x", pady=4)

        ttk.Button(
            buttons,
            text="Delete",
            command=self.delete_selected,
        ).pack(fill="x", pady=4)

        ttk.Button(
            buttons,
            text="Search",
            command=self.search_contacts,
        ).pack(fill="x", pady=4)

        ttk.Button(
            buttons,
            text="QR Code",
            command=self.qr.generate,
        ).pack(fill="x", pady=4)

        ttk.Button(
            buttons,
            text="Clear",
            command=self.clear_form,
        ).pack(fill="x", pady=4)

    def _build_table(self):
        columns = (
            "id",
            "first_name",
            "last_name",
            "mobile",
            "landline",
            "address",
        )

        self.table = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
        )

        headers = {
            "id": "ID",
            "first_name": "First Name",
            "last_name": "Last Name",
            "mobile": "Mobile",
            "landline": "Landline",
            "address": "Address",
        }

        for key in columns:
            self.table.heading(key, text=headers[key])

        self.table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10,
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self._on_selected,
        )

    def _build_statusbar(self):
        ttk.Label(
            self.root,
            textvariable=self.status,
            anchor="w",
        ).pack(fill="x")

    def refresh(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for contact in self.service.list_contacts():
            self.table.insert(
                "",
                "end",
                values=(
                    contact.id,
                    contact.first_name,
                    contact.last_name,
                    contact.mobile,
                    contact.landline,
                    contact.address,
                ),
            )

        self.status.set(
            f"Contacts: {self.service.contact_count()}"
        )

    def save_contact(self):
        try:
            contact = Contact(
                id=self.current_contact,
                first_name=self.fields["first_name"].get().strip(),
                last_name=self.fields["last_name"].get().strip(),
                mobile=self.fields["mobile"].get().strip(),
                landline=self.fields["landline"].get().strip(),
                address=self.fields["address"].get().strip(),
                notes=self.fields["notes"].get().strip(),
            )

            self.service.save_contact(contact)

            self.clear_form()
            self.refresh()

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
            )

    def delete_selected(self):
        pass

    def load_selected(self):
        pass

    def export_selected(self):
        pass

    def search_contacts(self):
        SearchDialog(self)

    def clear_form(self):
        self.current_contact = None

        for variable in self.fields.values():
            variable.set("")

    def _on_selected(self, event):
        pass

    def shutdown(self):
        self.service.shutdown()
        self.root.destroy()