from customtkinter import CTkFrame, CTkLabel, CTkTextbox
from utils.threading import start_thread

class IdInput:
    def __init__(self, master, label_text, placeholder_text, max_length=10000):
        self.master = master
        self.label_text = label_text
        self.placeholder_text = placeholder_text
        self.max_length = max_length
        self.resize_timer = None
        self.current_width = 200
        self.current_height = 25
        self.create_input()

    def create_input(self):
        self.id_frame = CTkFrame(master=self.master, fg_color="transparent")
        self.id_frame.pack(pady=10, padx=10, anchor="c")

        id_label = CTkLabel(master=self.id_frame,
                            text=self.label_text, font=("Helvetica", 12, "bold"))
        id_label.grid(row=0, column=0, padx=(0, 5), sticky="e")

        self.id_textbox = CTkTextbox(master=self.id_frame, width=self.current_width, height=self.current_height)
        self.id_textbox.grid(row=0, column=1, sticky="w")
        self.id_textbox.insert("1.0", self.placeholder_text)
        self.id_textbox.bind("<FocusIn>", self.clear_placeholder)
        self.id_textbox.bind("<FocusOut>", self.restore_placeholder)
        self.id_textbox.bind("<<Paste>>", self.handle_paste)
        self.id_textbox.bind("<KeyRelease>", self.debounce_resize)

    def clear_placeholder(self, event):
        if self.id_textbox.get("1.0", "end-1c") == self.placeholder_text:
            self.id_textbox.delete("1.0", "end")

    def restore_placeholder(self, event):
        if not self.id_textbox.get("1.0", "end-1c"):
            self.id_textbox.insert("1.0", self.placeholder_text)

    def handle_paste(self, event):
        clipboard_content = self.id_textbox.clipboard_get()
        
        if len(clipboard_content) > self.max_length:
            clipboard_content = clipboard_content[:self.max_length]
        
        start_thread(self.insert_text, clipboard_content)

        return "break"

    def insert_text(self, text):
        self.id_textbox.delete("1.0", "end")
        self.id_textbox.insert("1.0", text)
        self.debounce_resize()

    def debounce_resize(self, event=None):
        if self.resize_timer is not None:
            self.master.after_cancel(self.resize_timer)
        self.resize_timer = self.master.after(50, self.adjust_size)

    def adjust_size(self):
        content = self.id_textbox.get("1.0", "end-1c")
        lines = content.split("\n")
        new_width = max(200, min(max(len(line) for line in lines) * 8, 600))
        new_height = min(25 * max(1, len(lines)), 200)

        if new_width != self.current_width or new_height != self.current_height:
            self.current_width = new_width
            self.current_height = new_height
            self.id_textbox.configure(width=new_width, height=new_height)

    def get(self):
        content = self.id_textbox.get("1.0", "end-1c")
        return content.strip() if content != self.placeholder_text else ""
    
    def bind_enter(self, callback):
        self.id_textbox.bind("<Return>", self.on_enter)
        self.enter_callback = callback

    def on_enter(self, event):
        if not event.state & 1:  # Check if Shift key is not pressed
            self.enter_callback()
            return "break"  # Prevents the default newline behavior