from load_cleaning_data import *
from stat_weights import *
from evaluate_players_by_position import *
from show_evalution import show_evaluation_table
from filter_dataset import FilterWindow

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap import Style
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog

# Global storage

df_cleaned = None
filtered_result = None
stat_weights_dict = None

def handle_load_data():
    global df_cleaned
    file_path = filedialog.askopenfilename(
        filetypes=[("HTML Files", "*.html")],
        title="Select HTML file"
    )
    if file_path:
        try:
            df_cleaned = load_cleaning_data(file_path)
            Messagebox.show_info("Success", "Data cleaned")
        except Exception as e:
            Messagebox.show_error("Error", f"Failed to process file:\n{e}")

def handle_filters():
    global filtered_result
    if df_cleaned is None:
        Messagebox.show_warning("Warning", "Please load and clean data first.")
        return

    def save_filtered(df):
        global filtered_result
        filtered_result = {"df": df}
        Messagebox.show_info("Success", "Data filtered successfully.")

    FilterWindow(root, df_cleaned, callback=save_filtered)

def handle_stats():
    global stat_weights_dict
    try:
        stat_weights_dict = get_stat_weights(root)
        if stat_weights_dict:
            Messagebox.show_info("Success", "Stats and weights selected!")
        else:
            Messagebox.show_info("Info", "No stats selected.")
        return stat_weights_dict
    except Exception as e:
        Messagebox.show_error("Error", f"Stat selection failed:\n{e}")
        return {}

def handle_evaluate():
    if filtered_result is None or stat_weights_dict is None:
        Messagebox.show_warning("Warning", "Please filter data and set stat weights first.")
        return
    try:
        evaluated_df = evaluate_players_by_position(filtered_result['df'], stat_weights_dict)
        show_evaluation_table(evaluated_df)
    except Exception as e:
        Messagebox.show_error("Error", f"Evaluation failed:\n{e}")

# -------------------------
# Main UI Setup
# -------------------------
root = ttk.Window(themename="flatly")  # Choose your theme here
root.title("Football Analytics Tool")
root.geometry("400x300")

ttk.Label(root, text="Football Analytics Tool", font=("Helvetica", 16)).pack(pady=20)

ttk.Button(root, text="1. Load & Clean Data", command=handle_load_data, width=30, bootstyle="primary").pack(pady=5)
ttk.Button(root, text="2. Set Up Filters", command=handle_filters, width=30, bootstyle="info").pack(pady=5)
ttk.Button(root, text="3. Select Stats & Weights", command=handle_stats, width=30, bootstyle="warning").pack(pady=5)
ttk.Button(root, text="4. Evaluate Players", command=handle_evaluate, width=30, bootstyle="success").pack(pady=5)
ttk.Button(root, text="Exit", command=root.quit, width=30, bootstyle="danger").pack(pady=20)

root.mainloop()
