import tkinter as tk
from tkinter import ttk

def show_evaluation_table(df):
    # Create new popup window
    window = tk.Toplevel()
    window.title("Player Evaluation Results")

    frame = ttk.Frame(window)
    frame.pack(fill='both', expand=True)

    # Create Treeview
    tree = ttk.Treeview(frame)
    tree.pack(side='left', fill='both', expand=True)

    # Add vertical scrollbar
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    # Define columns
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"  # Hide first empty column

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w")

    # Insert data rows
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    window.geometry("800x400")
