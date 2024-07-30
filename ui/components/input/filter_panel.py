from customtkinter import CTkFrame, CTkCheckBox, CTkComboBox, CTkLabel

class FilterPanel:
    def __init__(self, master, filters=None):
        self.master = master
        self.filters = filters or ["location", "clearance"]
        self.create_widgets()

    def create_widgets(self):
        self.frame = CTkFrame(self.master, fg_color="transparent", width=400)
        self.frame.pack(pady=20, padx=10)

        # Add extra space after Job ID input
        CTkFrame(self.frame, height=30, fg_color="transparent").grid(row=0, column=0)

        # Filter By Frame
        self.filter_frame = CTkFrame(self.frame, fg_color="transparent")
        self.filter_frame.grid(row=1, column=0,  pady=(0, 15), sticky="w")

        self.title = CTkLabel(self.filter_frame, text="Filter By:", font=("Helvetica", 14, "bold"))
        self.title.grid(row=0, column=0, padx=(0, 15), sticky="w")

        # checkboxes
        self.populate_filters()

        # CV Update Dropdown
        self.create_cv_update_filter()

        # Extra space before the action button
        CTkFrame(self.frame, height=20, fg_color="transparent").grid(row=3, column=0)

    def populate_filters(self):
        filter_text = {
            "location": "Location",
            "clearance": "Clearance"
        }
        for i, filter_name in enumerate(self.filters):
            filter_var = CTkCheckBox(
                master=self.filter_frame, 
                text=filter_text[filter_name], 
                onvalue=filter_name
            )
            filter_var.grid(row=0, column=i+1, padx=(0, 15), pady=5,  sticky="w")

    def create_cv_update_filter(self):
        selections = ["3 months", "6 months", "12 months", "24 months", "Any"]
        
        self.dropdown_frame = CTkFrame(self.frame, fg_color="transparent")
        self.dropdown_frame.grid(row=2, column=0, sticky="ew", pady=(0, 25))
        
        self.dropdown_label = CTkLabel(self.dropdown_frame, text="CV Updated in the last:", font=("Helvetica", 14, "bold"))
        self.dropdown_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.dropdown = CTkComboBox(self.dropdown_frame, values=selections, state='readonly')
        self.dropdown.grid(row=0, column=1, sticky='e')
        self.dropdown.set("12 months")

    def get_selected_filters(self):

        selected_filters = {}

        for child in self.filter_frame.winfo_children():
            if isinstance(child, CTkCheckBox):
                selected_filters[child.cget("onvalue")] = True if child.get() else False

        selected_filters["cv_update"] = self.dropdown.get()

        return selected_filters