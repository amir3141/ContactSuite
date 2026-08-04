from tkinter import filedialog, messagebox
from fpdf import FPDF
import webbrowser


class ExportService:
    def __init__(self, service):
        self.service = service

    def export_all_pdf(self):
        contacts = self.service.list_contacts()

        if not contacts:
            messagebox.showinfo(
                "Information",
                "No contacts available."
            )
            return

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(
            0,
            12,
            "Contact Directory",
            ln=True,
            align="C",
        )

        pdf.ln(8)

        pdf.set_font("Helvetica", "B", 10)

        headers = [
            ("ID", 12),
            ("First Name", 38),
            ("Last Name", 38),
            ("Mobile", 42),
            ("Landline", 42),
            ("Address", 58),
        ]

        for title, width in headers:
            pdf.cell(width, 10, title, border=1)

        pdf.ln()

        pdf.set_font("Helvetica", "", 9)

        for contact in contacts:
            pdf.cell(12, 8, str(contact.id), border=1)
            pdf.cell(38, 8, contact.first_name[:20], border=1)
            pdf.cell(38, 8, contact.last_name[:20], border=1)
            pdf.cell(42, 8, contact.mobile[:20], border=1)
            pdf.cell(42, 8, contact.landline[:20], border=1)
            pdf.cell(58, 8, contact.address[:30], border=1)
            pdf.ln()

        destination = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[
                ("PDF Files", "*.pdf")
            ],
        )

        if not destination:
            return

        pdf.output(destination)

        messagebox.showinfo(
            "Completed",
            "The PDF file has been created successfully."
        )

        webbrowser.open(destination)

    def export_contact_pdf(self, contact):
        if contact is None:
            messagebox.showwarning(
                "Warning",
                "No contact selected."
            )
            return

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(
            0,
            12,
            "Contact Details",
            ln=True,
            align="C",
        )

        pdf.ln(10)

        pdf.set_font("Helvetica", "", 11)

        rows = [
            ("First Name", contact.first_name),
            ("Last Name", contact.last_name),
            ("Mobile", contact.mobile),
            ("Landline", contact.landline),
            ("Address", contact.address),
            ("Notes", contact.notes),
        ]

        for label, value in rows:
            pdf.cell(
                45,
                10,
                f"{label}:",
            )
            pdf.multi_cell(
                0,
                10,
                value or "-"
            )

        destination = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[
                ("PDF Files", "*.pdf")
            ],
        )

        if not destination:
            return

        pdf.output(destination)

        messagebox.showinfo(
            "Completed",
            "Contact exported successfully."
        )

        webbrowser.open(destination)

    def export_vcard(self, contact):
        if contact is None:
            messagebox.showwarning(
                "Warning",
                "No contact selected."
            )
            return

        destination = filedialog.asksaveasfilename(
            defaultextension=".vcf",
            filetypes=[
                ("vCard", "*.vcf")
            ],
        )

        if not destination:
            return

        content = f"""BEGIN:VCARD
VERSION:3.0
FN:{contact.full_name}
N:{contact.last_name};{contact.first_name};;;
TEL;TYPE=CELL:{contact.mobile}
TEL;TYPE=HOME:{contact.landline}
ADR;TYPE=HOME:;;{contact.address};;;
NOTE:{contact.notes}
END:VCARD"""

        with open(
            destination,
            "w",
            encoding="utf-8",
        ) as stream:
            stream.write(content)

        messagebox.showinfo(
            "Completed",
            "vCard exported successfully."
        )