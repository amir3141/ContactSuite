import qrcode

from tkinter import Toplevel, Label, filedialog, messagebox
from PIL import ImageTk


class QRService:
    def __init__(self, service):
        self.service = service

    def generate(self, contact=None):
        if contact is None:
            messagebox.showwarning(
                "Warning",
                "Please select a contact."
            )
            return

        payload = self._build_vcard(contact)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )

        qr.add_data(payload)
        qr.make(fit=True)

        image = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        destination = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png")
            ],
        )

        if not destination:
            return

        image.save(destination)

        messagebox.showinfo(
            "Completed",
            "QR Code saved successfully."
        )

        self.preview(image)

    def preview(self, image):
        window = Toplevel()
        window.title("QR Code")

        preview = ImageTk.PhotoImage(image)

        label = Label(
            window,
            image=preview,
        )

        label.image = preview
        label.pack(
            padx=15,
            pady=15,
        )

    @staticmethod
    def _build_vcard(contact):
        return f"""BEGIN:VCARD
VERSION:3.0
FN:{contact.full_name}
N:{contact.last_name};{contact.first_name};;;
TEL;TYPE=CELL:{contact.mobile}
TEL;TYPE=HOME:{contact.landline}
ADR;TYPE=HOME:;;{contact.address};;;
NOTE:{contact.notes}
END:VCARD"""