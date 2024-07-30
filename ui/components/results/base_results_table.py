from tksheet import Sheet
from tksheet.themes import theme_dark

class BaseResultsTable:
    def __init__(self, master, results, height=400):
        self.results = results
        self.sheet = Sheet(master, height=height, show_x_scrollbar=False)
        self.sheet.enable_bindings(("single_select",
                                    "row_select",
                                    "column_select",
                                    "column_width_resize",
                                    "arrowkeys",
                                    "vertical_scroll",
                                    "horizontal_scroll",
                                    "right_click_popup_menu",
                                    "rc_select",
                                    "copy",
                                    "double_click_column_resize",
                                    "drag_select",
                                    "undo",
                                    "select_all",
                                    "edit_cell",
                                    "edit_header"
                                    ))
        
        # Sorting functionality
        self.sheet.extra_bindings("begin_edit_header", self.sort_column)
        self.last_sort_column = None
        self.sort_ascending = True
        self.associated_data = {}
        
        self.prepare_results()
        self.set_headers()
        self.sheet.set_sheet_data(self.formatted_results)
        self.sheet.set_all_cell_sizes_to_text()
        self.apply_custom_theme()
        self.sheet.refresh()

    def prepare_results(self):
        # This method should be implemented in child classes
        raise NotImplementedError

    def set_headers(self):
        # This method should be implemented in child classes
        raise NotImplementedError
    
    def apply_custom_theme(self):
        custom_dark_theme = dict(theme_dark)
        gold_color = "#efbd55"
        blue_color = "#6aa2fc"

        for key, value in custom_dark_theme.items():
            if isinstance(value, str) and value.lower() == blue_color.lower():
                custom_dark_theme[key] = gold_color

        custom_dark_theme["header_selected_columns_bg"] = gold_color
        custom_dark_theme["index_selected_rows_bg"] = gold_color
        custom_dark_theme["table_selected_rows_border_fg"] = gold_color
        custom_dark_theme["table_selected_columns_border_fg"] = gold_color
        custom_dark_theme["table_bg"] = "#1E1E1E"
        custom_dark_theme["table_fg"] = "#FFFFFF"
        custom_dark_theme["table_grid_fg"] = "#3A3A3A"
        custom_dark_theme["table_selected_cells_bg"] = "#2A2A2A"
        custom_dark_theme["table_selected_rows_bg"] = "#2A2A2A"
        custom_dark_theme["table_selected_columns_bg"] = "#2A2A2A"
        custom_dark_theme["header_bg"] = "#1A1A1A"
        custom_dark_theme["index_bg"] = "#1A1A1A"

        self.sheet.set_options(**custom_dark_theme)
        self.sheet.config(bg=custom_dark_theme["table_bg"])
        self.sheet.MT.recreate_all_selection_boxes()


    def sort_column(self, event):
        column = event['column']
        data = self.sheet.get_sheet_data()
        headers = self.sheet.headers()
        header = headers[column]

        # Save current column widths
        column_widths = [self.sheet.column_width(col) for col in range(len(headers))]

        # Determine if we're sorting in ascending or descending order
        if self.last_sort_column == column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_ascending = True

        # Create a list of tuples: (row_data, index)
        indexed_data = list(enumerate(data))

        # Sort the data
        sorted_indexed_data = sorted(indexed_data, key=lambda x: self.sort_key(x[1][column]), reverse=not self.sort_ascending)

        # Separate the sorted data and the original indices
        sorted_data = [row for _, row in sorted_indexed_data]
        sorted_indices = [index for index, _ in sorted_indexed_data]

        # Update the sheet with sorted data
        self.sheet.set_sheet_data(sorted_data)

        # Sort associated data
        for key, value_list in self.associated_data.items():
            self.associated_data[key] = [value_list[i] for i in sorted_indices]

        # Update headers to show sort direction and adjust column width
        arrow_width = 15  # Adjust this value as needed
        for i, h in enumerate(headers):
            # Remove any existing sort indicators
            h = h.replace(' ↑', '').replace(' ↓', '')
            
            if i == column:
                # Add the appropriate sort indicator
                headers[i] = f"{h} {'↑' if self.sort_ascending else '↓'}"
                # Increase width of sorted column if it wasn't already sorted
                if i != self.last_sort_column:
                    column_widths[i] += arrow_width
            else:
                headers[i] = h
                # Reset width of previously sorted column
                if i == self.last_sort_column:
                    column_widths[i] -= arrow_width

        self.sheet.headers(headers)

        # Restore column widths
        for col, width in enumerate(column_widths):
            self.sheet.column_width(col, width)

        # Remember the last sorted column
        self.last_sort_column = column
        self.sheet.refresh()

    def sort_key(self, value):
        """Helper function to determine the key for sorting."""
        if isinstance(value, (int, float)):
            return value
        elif isinstance(value, str):
            # Try to convert to float if it's a number string
            try:
                return float(value)
            except ValueError:
                return value.lower()  # Case-insensitive string sorting
        else:
            return str(value).lower()  # Fall back to string sorting for other types