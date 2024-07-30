from customtkinter import CTk, CTkToplevel, CTkLabel, CTkFrame, CTkProgressBar, ThemeManager, set_default_color_theme, set_appearance_mode 
from utils.threading import start_thread
from utils.constants import ICON_PATH

class Application(CTk):
    def __init__(self):
        super().__init__()
        self.set_appearance()
        self.withdraw()  # Hide the main window initially
        self.loading_window = None
        self.after(10, self.create_loading_screen)

    def create_loading_screen(self):
        self.loading_window = CTkToplevel(self)
        self.loading_window.geometry("300x150")
        self.loading_window.title("Loading...")
        self.loading_window.attributes('-topmost', True)
        
        self.start_icon_update(self.loading_window)
        
        label = CTkLabel(self.loading_window, text="Loading Recruitment Hive AI Helper...")
        label.pack(pady=20)
        
        self.progress_bar = CTkProgressBar(self.loading_window, mode="indeterminate")
        self.progress_bar.pack(pady=10)
        self.progress_bar.start()
        
        self.after(10, self.start_loading)

    def start_icon_update(self, window):
        self.update_icon(window)

    def update_icon(self, window):
        try:
            window.wm_iconbitmap(ICON_PATH)
        except Exception as e:
            print(f"Error setting icon: {e}")
        finally:
            window.after(100, lambda: self.update_icon(window))

    def start_loading(self):
        # threading.Thread(target=self.load_main_application, daemon=True).start()
        start_thread(self.load_main_application)


    def load_main_application(self):
        self.prepare_main_window()
        self.initialize_navigator()
        self.after(0, self.finish_loading)

    def set_appearance(self):
        try:
            set_appearance_mode("dark")
            set_default_color_theme("dark-blue")
            ThemeManager.theme["CTkButton"]["fg_color"] = "#efbd55"
            ThemeManager.theme["CTkButton"]["hover_color"] = "#d4a43e"
            ThemeManager.theme["CTkButton"]["text_color"] = "#000000"
            ThemeManager.theme["CTkLabel"]["text_color"] = "#e0e0e0"
            ThemeManager.theme["CTkProgressBar"]["progress_color"] = "#efbd55"
        except Exception as e:
            print(f"Error setting appearance: {e}")

    def prepare_main_window(self):
        self.after_idle(self.iconbitmap, ICON_PATH)
        self.after_idle(self.geometry, "1080x800")
        self.after_idle(self.title, "Recruitment Hive AI Helper V2")
        self.after_idle(self.create_root_frame)

    def create_root_frame(self):
        self.root_frame = CTkFrame(master=self)
        self.root_frame.pack(fill="both", expand=True)

    def initialize_navigator(self):
        from ui.navigator import Navigator
        self.navigator = Navigator(self.root_frame)

    def finish_loading(self):
        self.navigator.open_find_cand()
        self.loading_window.after_cancel(self.update_icon)
        self.loading_window.destroy()
        self.deiconify()