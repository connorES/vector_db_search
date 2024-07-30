from customtkinter import CTkButton


class SidebarFunctionButton:
    def __init__(self, master, text, command):
        self.master = master
        self.text = text
        self.command = command
        self.button = self.create_button()
        self.is_selected = False

    def create_button(self):
        return CTkButton(
            master=self.master,
            width=410,
            height=80,
            font=("Helvetica", 14, "bold"),
            corner_radius=10,
            text=self.text,
            command=self.on_click
        )

    def pack(self, **kwargs):
        self.button.pack(**kwargs)

    def on_click(self):
        self.command()

    def set_selected(self, is_selected):
        self.is_selected = is_selected
        if is_selected:
            self.button.configure(border_width=2, border_color="#FFFFFF")
        else:
            self.button.configure(border_width=0)
