import json

from tkinter import filedialog, messagebox

from entities import Contact


class BackupService:
    def __init__(self, service):
        self.service = service

    def create_backup(self):
        contacts = self.service.list_contacts()

        if not contacts:
            messagebox.showinfo(
                "Information",
                "There are no contacts to back up."
            )
            return

        destination = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON File", "*.json")
            ],
        )

        if not destination:
            return

        payload = [
            contact.as_dict()
            for contact in contacts
        ]

        with open(
            destination,
            "w",
            encoding="utf-8",
        ) as stream:
            json.dump(
                payload,
                stream,
                ensure_ascii=False,
                indent=4,
            )

        messagebox.showinfo(
            "Completed",
            "Backup completed successfully."
        )

    def restore_backup(self):
        source = filedialog.askopenfilename(
            filetypes=[
                ("JSON File", "*.json")
            ],
        )

        if not source:
            return

        try:
            with open(
                source,
                "r",
                encoding="utf-8",
            ) as stream:
                records = json.load(stream)

            self.service.delete_everything()

            for record in records:
                contact = Contact(
                    first_name=record.get("first_name", ""),
                    last_name=record.get("last_name", ""),
                    mobile=record.get("mobile", ""),
                    landline=record.get("landline", ""),
                    address=record.get("address", ""),
                    notes=record.get("notes", ""),
                )

                self.service.save_contact(contact)

            messagebox.showinfo(
                "Completed",
                "Contacts restored successfully."
            )

        except Exception as error:
            messagebox.showerror(
                "Restore Failed",
                str(error),
            )