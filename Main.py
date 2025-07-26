'''
Written by Ed Gramza
This program uses three different frames: Rax, Checkbox, Speech, and Display.
*** Rax
This section is used for gathering all the information from the user. Unfortunately,
I couldn't find a way to get an automatic location, so it depends on the user to provide
it. There is no error checking for any of the fields the user fills out, but that will
come in a later iteration.
'''

import Tkinter as tk
import tkMessageBox
import time
from difflib import get_close_matches


class Rax:
    def __init__(self, root):
        self.root = root
        self.root.title("Input and Edit App")

        # List used for storing dictionaries entered by the user
        self.entries = []

        # List of US states (abbreviations, full names, and pronunciations)
        self.states = {
            "AL": ("Alabama", "al-uh-BAM-uh"),
            "AK": ("Alaska", "uh-LAS-kuh"),
            "AZ": ("Arizona", "ar-uh-ZOH-nuh"),
            "AR": ("Arkansas", "AR-kuhn-saw"),
            "CA": ("California", "kal-uh-FORN-yuh"),
            "CO": ("Colorado", "kol-uh-RAD-oh"),
            "CT": ("Connecticut", "kuh-NEH-ti-kuht"),
            "DE": ("Delaware", "DEL-uh-wair"),
            "FL": ("Florida", "FLOR-uh-duh"),
            "GA": ("Georgia", "JOR-juh"),
            "HI": ("Hawaii", "huh-WAI-ee"),
            "ID": ("Idaho", "EYE-duh-hoh"),
            "IL": ("Illinois", "il-uh-NOY"),
            "IN": ("Indiana", "in-dee-AN-uh"),
            "IA": ("Iowa", "EYE-uh-wuh"),
            "KS": ("Kansas", "KAN-zuhs"),
            "KY": ("Kentucky", "ken-TUK-ee"),
            "LA": ("Louisiana", "loo-ee-zee-AN-uh"),
            "ME": ("Maine", "mayn"),
            "MD": ("Maryland", "MAIR-uh-luhnd"),
            "MA": ("Massachusetts", "mass-uh-CHOO-sits"),
            "MI": ("Michigan", "MISH-uh-guhn"),
            "MN": ("Minnesota", "min-uh-SOH-tuh"),
            "MS": ("Mississippi", "miss-uh-SIP-ee"),
            "MO": ("Missouri", "miz-ZUR-ee"),
            "MT": ("Montana", "mon-TAN-uh"),
            "NE": ("Nebraska", "nuh-BRAS-kuh"),
            "NV": ("Nevada", "nuh-VAD-uh"),
            "NH": ("New Hampshire", "noo HAMP-shur"),
            "NJ": ("New Jersey", "noo JUR-zee"),
            "NM": ("New Mexico", "noo MEX-i-coh"),
            "NY": ("New York", "noo YORK"),
            "NC": ("North Carolina", "north kar-uh-LINE-uh"),
            "ND": ("North Dakota", "north duh-KOH-tuh"),
            "OH": ("Ohio", "oh-HIGH-oh"),
            "OK": ("Oklahoma", "oh-kluh-HOH-muh"),
            "OR": ("Oregon", "OR-uh-guhn"),
            "PA": ("Pennsylvania", "pen-suhl-VAY-nee-uh"),
            "RI": ("Rhode Island", "rohd EYE-luhnd"),
            "SC": ("South Carolina", "south kar-uh-LINE-uh"),
            "SD": ("South Dakota", "south duh-KOH-tuh"),
            "TN": ("Tennessee", "ten-uh-SEE"),
            "TX": ("Texas", "TEKS-uhs"),
            "UT": ("Utah", "YOO-tah"),
            "VT": ("Vermont", "ver-MONT"),
            "VA": ("Virginia", "ver-JIN-yuh"),
            "WA": ("Washington", "WASH-ing-tuhn"),
            "WV": ("West Virginia", "west ver-JIN-yuh"),
            "WI": ("Wisconsin", "wis-KON-sin"),
            "WY": ("Wyoming", "wy-OH-ming")
        }

        # Left frame used for user input
        self.rax_frame = tk.Frame(root)
        self.rax_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Input labels and entry fields
        self.fields = ['Location', 'Place', 'Type', 'Quantity', 'Time Begin', 'Time End']
        self.input_vars = {field: tk.StringVar() for field in self.fields}

        # Loop through fields list and assign user input fields
        for field in self.fields:
            tk.Label(self.rax_frame, text="{}:".format(field)).pack(anchor=tk.W)
            entry = tk.Entry(self.rax_frame, textvariable=self.input_vars[field])
            entry.pack(fill=tk.X)

            # Bind Place entry to dictionary of locations for automatic suggestions
            if field == "Place":
                entry.bind('<KeyRelease>', self.show_state_suggestions)
            self.input_vars[field].trace('w', self.update_dynamic_speech)

        # Dropdown for location suggestions
        self.suggestion_listbox = tk.Listbox(self.rax_frame, height=4)
        self.suggestion_listbox.pack(fill=tk.X)
        self.suggestion_listbox.bind('<<ListboxSelect>>', self.select_state_suggestion)

        # Data for the checkboxes
        self.checkbox_times = {i: None for i in range(1, 6)}

        # Checkbox labels
        self.checkbox_labels_text = ["In Cart", "Ordered", "Shipped", "Delivered", "Other"]

        # Checkboxes for storing time
        self.checkbox_frame = tk.Frame(self.rax_frame)
        self.checkbox_frame.pack(pady=5)

        self.checkbox_vars = {}
        self.checkbox_labels = {}

        # Generate checkboxes using the checkbox_labels_text list
        for i, label_text in enumerate(self.checkbox_labels_text, start=1):
            # Create a variable to monitor the state of the checkbox: 1 = Checked, 0 = Unchecked
            var = tk.IntVar()
            checkbox = tk.Checkbutton(
                self.checkbox_frame,
                text=label_text,
                variable=var,
                command=lambda i=i: self.store_checkbox_time(i)
            )
            checkbox.pack(anchor=tk.W, padx=10)
            self.checkbox_vars[i] = var

            # Label for displaying the time next to each checkbox
            label = tk.Label(self.checkbox_frame, text="", fg="blue")
            label.pack(anchor=tk.W, padx=20)
            self.checkbox_labels[i] = label

        # Add button
        self.add_button = tk.Button(self.rax_frame, text="Add", command=self.add_entry)
        self.add_button.pack(fill=tk.X, pady=5)

        # Speech generation frame that will be generated by variables entered by user
        self.speech_frame = tk.Frame(root)
        self.speech_frame.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(self.speech_frame, text="Generated Speech:").pack(anchor=tk.W)
        self.speech_text = tk.Text(self.speech_frame, height=20, width=40, wrap=tk.WORD, state=tk.DISABLED)
        self.speech_text.pack()

        # Frame used for displaying previously saved calls
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.display_frame, selectmode=tk.SINGLE, width=75)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.edit_entry)

        # Delete button
        self.delete_button = tk.Button(self.display_frame, text="Delete", command=self.delete_entry)
        self.delete_button.pack(fill=tk.X, pady=5)

        self.display_mode = "start_time"  # Default mode
        self.toggle_button = tk.Button(self.display_frame, text="Toggle View", command=self.toggle_display_mode)
        self.toggle_button.pack(fill=tk.X, pady=5)

        self.copy_button = tk.Button(self.display_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(fill=tk.X, pady=5)

    def update_dynamic_speech(self, *args):
        #Generate dynamic speech based on current input values.
        current_entry = {field: var.get().strip() for field, var in self.input_vars.items()}
        place = current_entry.get('Place', '').strip()

        # Check if the place is in the states dictionary
        if place in self.states:
            full_name, pronunciation = self.states[place]
            place_text = "{} ({})".format(full_name, pronunciation)
        else:
            # Use the user-entered value if not found in the states list
            place_text = place if place else "N/A"

        # Generate the speech text
        speech = "Location: {}, Place: {}, Type: {}, Quantity: {}, Start: {}, End: {}".format(
            current_entry.get('Location', 'N/A'),
            place_text,
            current_entry.get('Type', 'N/A'),
            current_entry.get('Quantity', 'N/A'),
            current_entry.get('Time Begin', 'N/A'),
            current_entry.get('Time End', 'N/A')
        )
        self.speech_text.config(state=tk.NORMAL)
        self.speech_text.delete(1.0, tk.END)
        self.speech_text.insert(tk.END, speech)
        self.speech_text.config(state=tk.DISABLED)

    def store_checkbox_time(self, i):
        #Store the time a checkbox is clicked and display it next to the checkbox.
        if self.checkbox_vars[i].get():
            self.checkbox_times[i] = time.strftime("%H:%M:%S")
        else:
            self.checkbox_times[i] = None
        self.update_checkbox_labels()

    def update_checkbox_labels(self):
        #Update the time labels next to each checkbox.
        for i, label in self.checkbox_labels.items():
            label.config(text=self.checkbox_times[i] if self.checkbox_times[i] else "")

    def add_entry(self):
        #Add the current input data to the list of entries.
        entry = {field: var.get().strip() for field, var in self.input_vars.items()}
        entry['Checkbox Times'] = {i: self.checkbox_times[i] for i in range(1, 6)}
        self.entries.append(entry)
        self.refresh_listbox()
        self.reset_inputs()

    def refresh_listbox(self):
        #Refresh the listbox display based on the current display mode.
        self.listbox.delete(0, tk.END)
        for idx, entry in enumerate(self.entries, 1):
            if self.display_mode == "start_time":
                display_text = "{}: {} ({})".format(
                    idx,
                    entry.get('Place', 'N/A'),
                    entry.get('Time Begin', 'N/A')
                )
            elif self.display_mode == "quantity_type":
                display_text = "{}: {} ({})".format(
                    idx,
                    entry.get('Place', 'N/A'),
                    "{} {}".format(entry.get('Quantity', 'N/A'), entry.get('Type', 'N/A'))
                )
            self.listbox.insert(tk.END, display_text)

    def toggle_display_mode(self):
        #Toggle the display mode and refresh the listbox.
        if self.display_mode == "start_time":
            self.display_mode = "quantity_type"
        else:
            self.display_mode = "start_time"
        self.refresh_listbox()

    def reset_inputs(self):
        #Clear all input fields and reset checkboxes.
        for var in self.input_vars.values():
            var.set("")
        for i in range(1, 6):
            self.checkbox_vars[i].set(0)
            self.checkbox_times[i] = None
        self.update_checkbox_labels()
        self.update_dynamic_speech()

    def edit_entry(self, event):
        #Open a pop-up window to edit the selected entry.
        try:
            idx = self.listbox.curselection()[0]
            selected_entry = self.entries[idx]

            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Entry")

            edit_vars = {field: tk.StringVar(value=selected_entry.get(field, "")) for field in self.fields}
            for field, var in edit_vars.items():
                tk.Label(edit_window, text="{}:".format(field)).pack(anchor=tk.W)
                tk.Entry(edit_window, textvariable=var).pack(fill=tk.X, padx=10, pady=2)

            checkbox_times = {}
            for i in range(1, 6):
                time_label = tk.Label(edit_window, text="Checkbox {} Time: {}".format(i, selected_entry['Checkbox Times'].get(i, "Not Set")))
                time_label.pack(anchor=tk.W, padx=10)
                checkbox_times[i] = time_label

            def save_changes():
                for field, var in edit_vars.items():
                    selected_entry[field] = var.get()
                for i in range(1, 6):
                    selected_entry['Checkbox Times'][i] = self.checkbox_times[i]
                self.refresh_listbox()
                edit_window.destroy()

            tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)
        except IndexError:
            tkMessageBox.showerror("Error", "No item selected!")

    def delete_entry(self):
        #Delete the selected entry.
        try:
            idx = self.listbox.curselection()[0]
            del self.entries[idx]
            self.refresh_listbox()
        except IndexError:
            tkMessageBox.showerror("Error", "No item selected!")

    def select_state_suggestion(self, event):
        selected = self.suggestion_listbox.get(tk.ACTIVE)
        self.input_vars['Place'].set(selected)
        self.suggestion_listbox.pack_forget()

    def show_state_suggestions(self, event):
        #Show state suggestions based on what the user is entering
        input_text = self.input_vars['Place'].get()
        matches = get_close_matches(input_text, self.states.keys(), n=5)
        self.suggestion_listbox.delete(0, tk.END)
        for match in matches:
            self.suggestion_listbox.insert(tk.END, match)
        self.suggestion_listbox.pack() if matches else self.suggestion_listbox.pack_forget()

    def copy_to_clipboard(self):
        #Copy the contents of both toggle views to the clipboard.
        start_time_view = []
        quantity_type_view = []

        for idx, entry in enumerate(self.entries, 1):
            start_time_view.append(
                "{}: {} ({})".format(
                    idx,
                    entry.get('Place', 'N/A'),
                    entry.get('Time Begin', 'N/A')
                )
            )
            quantity_type_view.append(
                "{}: {} ({})".format(
                    idx,
                    entry.get('Place', 'N/A'),
                    "{} {}".format(entry.get('Quantity', 'N/A'), entry.get('Type', 'N/A'))
                )
            )

        # Format the combined text
        clipboard_text = "Start Time View:\n" + "\n".join(start_time_view) + "\n\n"
        clipboard_text += "Quantity and Type View:\n" + "\n".join(quantity_type_view)

        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(clipboard_text)
        self.root.update()  # Necessary to push the updated clipboard content
        tkMessageBox.showinfo("Copied", "Content copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = Rax(root)
    root.mainloop()