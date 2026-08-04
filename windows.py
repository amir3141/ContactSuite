import tkinter as tk
from tkinter import ttk, messagebox


class SearchDialog(tk.Toplevel):
    def __init__(self, application):
        super().__init__(application.root)

        self.application = application

        self.title("Search Contacts")
        self.geometry("420x150")
        self.resizable(False, False)
        self.transient(application.root)
        self.grab_set()

        self.keyword = tk.StringVar()

        self._build()

    def _build(self):
        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Search"
        ).pack(anchor="w")

        entry = ttk.Entry(
            container,
            textvariable=self.keyword,
            width=40
        )
        entry.pack(fill="x", pady=10)
        entry.focus()

        controls = ttk.Frame(container)
        controls.pack(fill="x")

        ttk.Button(
            controls,
            text="Search",
            command=self.perform_search
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="Reset",
            command=self.reset_results
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="Close",
            command=self.destroy
        ).pack(side="right")

        self.bind("<Return>", lambda _: self.perform_search())

    def perform_search(self):
        keyword = self.keyword.get().strip()

        if not keyword:
            messagebox.showwarning(
                "Warning",
                "Please enter a search term."
            )
            return

        for row in self.application.table.get_children():
            self.application.table.delete(row)

        results = self.application.service.search_contacts(keyword)

        for contact in results:
            self.application.table.insert(
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

        self.application.status.set(
            f"Results: {len(results)}"
        )

        self.destroy()

    def reset_results(self):
        self.application.refresh()
        self.destroy()