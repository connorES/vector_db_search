import queue
from  customtkinter import CTkProgressBar, CTkFrame
from utils.threading import start_thread


class ProgressBar(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.progress_queue = queue.Queue()
        self.is_running = False
        self.total_steps = 100
        
        self.progress_bar = CTkProgressBar(self, mode="determinate")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10, padx=10, fill="x", expand=True)
        
        # Initially hidden
        self.pack_forget()  

    def start(self, total_steps=100):
        self.total_steps = total_steps
        self.pack(pady=10, padx=10, fill="x", expand=True)
        self.progress_bar.set(0)
        self.is_running = True
        start_thread(self.update_progress)

    def stop(self):
        self.is_running = False
        
        # Hide after a short delay
        self.after(200, self.pack_forget) 

    def update_progress(self):
        while self.is_running:
            try:
                progress = self.progress_queue.get(timeout=0.1)
                self.master.after(0, self._set_progress, progress)
                if progress >= 1:
                    self.stop()
            except queue.Empty:
                continue

    def _set_progress(self, progress):
        self.progress_bar.set(progress)
        self.update_idletasks()


    def set(self, current_step):
        """
        Update the progress bar with a single function call.
        :param current_step: The current step of the process.
        """
        progress = min(current_step / self.total_steps, 1)
        self.progress_bar.set(progress)