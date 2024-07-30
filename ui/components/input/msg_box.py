from customtkinter import CTkLabel, CTkFrame


class msg_box:
    def __init__(self, msg, root_frame):
        frame = self.frame = CTkFrame(root_frame, width=500, height=50)
        frame.pack(pady=100)

        self.message = CTkLabel(frame, text=msg)
        self.message.pack(pady=10)

    def change_msg(self, new_msg):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.message = CTkLabel(self.frame, text=new_msg)
        self.message.pack(pady=10)

    def delayed_msg(self, new_msg):
        self.frame.after(150, lambda: self.change_msg(new_msg))

    def destroy(self):
        self.frame.destroy()

    def delayed_destroy(self):
        self.frame.after(6000, lambda: self.frame.destroy())
