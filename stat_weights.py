import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

class StatWeightsDialog(ttk.Toplevel):
    def __init__(self, parent, stats_list):
        super().__init__(parent)
        self.title("Select Stats and Assign Weights")
        self.selected_stats = None
        self.geometry("400x500")

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = ttk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.checkboxes = {}
        self.entries = {}

        for stat in stats_list:
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill="x", pady=2, padx=5)

            var = ttk.BooleanVar()
            chk = ttk.Checkbutton(frame, text=stat, variable=var, bootstyle="info")
            chk.pack(side="left", anchor="w")

            entry = ttk.Entry(frame, width=6)
            entry.insert(0, "0.5")
            entry.pack(side="right", anchor="e")

            self.checkboxes[stat] = var
            self.entries[stat] = entry

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        submit_btn = ttk.Button(btn_frame, text="Submit", command=self.on_submit, bootstyle="success")
        submit_btn.pack(side="left", padx=5)

        info_btn = ttk.Button(btn_frame, text="i", width=3, command=self.show_position_guide, bootstyle="info")
        info_btn.pack(side="left")


        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        parent.wait_window(self)

    def show_position_guide(self):
        from tkinter import ttk as tkttk  # to avoid ttkbootstrap conflict

        guide_win = ttk.Toplevel(self)
        guide_win.title("Recommended Stats per Position")
        guide_win.geometry("1100x400")

        columns = ["Position"]
        for i in range(1, 8):
            columns.append(f"Stat {i}")
            columns.append(f"W{i}")

        tree = tkttk.Treeview(guide_win, columns=columns, show="headings")

        # Set up column headers
        tree.heading("Position", text="Position")
        for i in range(1, 8):
            tree.heading(f"Stat {i}", text=f"Stat {i}")
            tree.heading(f"W{i}", text="W")

        # Set up column widths and alignment
        tree.column("Position", width=150, anchor="w")
        for i in range(1, 8):
            tree.column(f"Stat {i}", width=120, anchor="w")
            tree.column(f"W{i}", width=50, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(guide_win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Data from HTML (converted to list of rows)
        data = [
            ("Goalkeeper (GK)", "Sv %", 0.95, "Sv/90", 0.85, "Cln/90", 0.75, "Pens Saved", 0.70, "xGP", 0.60, "All/90", 0.50, "Shutouts", 0.65),
            ("Centre Back (CB)", "Hdr %", 0.90, "Clr/90", 0.85, "Tck/90", 0.80, "Int/90", 0.75, "Blk/90", 0.70, "Hdrs W/90", 0.65, "Yel", 0.30),
            ("Fullback (FB/WB)", "Crs A/90", 0.85, "Drb/90", 0.75, "Tck/90", 0.70, "Int/90", 0.65, "OP-KP/90", 0.60, "Ps C/90", 0.55, "Pas %", 0.50),
            ("Defensive Mid (DM)", "Tck/90", 0.90, "Int/90", 0.85, "Pr passes/90", 0.70, "Pas %", 0.65, "Blk/90", 0.60, "K Tck/90", 0.55, "Fls", 0.40),
            ("Centre Mid (CM)", "xA/90", 0.80, "Pr passes/90", 0.75, "Int/90", 0.70, "Ps C/90", 0.65, "K Pas/90", 0.60, "Tck/90", 0.55, "Drb/90", 0.50),
            ("Attacking Mid (AM)", "xA/90", 0.90, "OP-KP/90", 0.85, "Ch C/90", 0.75, "Drb/90", 0.70, "Gls/90", 0.65, "xG/90", 0.60, "Pas %", 0.50),
            ("Winger (LW/RW)", "Crs A/90", 0.90, "xA/90", 0.85, "Drb/90", 0.80, "OP-KP/90", 0.75, "Gls/90", 0.60, "Shot %", 0.50, "Tck/90", 0.45),
            ("Striker (ST)", "xG/90", 1.00, "Gls/90", 0.95, "Conv %", 0.85, "xG/shot", 0.80, "ShT/90", 0.75, "Asts/90", 0.60, "Shot %", 0.55),
        ]

        # Insert rows
        for row in data:
            tree.insert("", "end", values=row)


    def on_submit(self):
        selected = {}
        for stat, var in self.checkboxes.items():
            if var.get():
                try:
                    weight = float(self.entries[stat].get())
                    if 0 <= weight <= 1:
                        selected[stat] = weight
                    else:
                        Messagebox.show_error("Invalid weight", f"Weight for {stat} must be between 0 and 1.")
                        return
                except ValueError:
                    Messagebox.show_error("Invalid input", f"Weight for {stat} must be a number.")
                    return

        self.selected_stats = selected
        self.destroy()

    def on_close(self):
        self.selected_stats = {}
        self.destroy()

    

def get_stat_weights(root):
    stats_list = [
        'Dist/90','Poss Won/90', 'Poss Lost/90', 'Gwin','Pts/Gm', 'Tgls/90', 'Tcon/90', 'Gls','Gls/90', 'Conv %',
        'Mins/Gl', 'Last Gl', 'xG', 'xG/90', 'xG-OP', 'NP-xG', 'NP-xG/90', 'Shots','Shot/90', 'xG/shot', 'ShT', 'ShT/90',
        'Shot %', 'Shots Outside Box/90', 'Goals Outside Box', 'Pens', 'Pens S', 'Pen/R', 'Ast', 'Asts/90', 'xA',
        'xA/90', 'Pas A', 'Ps A/90', 'Ps C', 'Ps C/90', 'Pas %', 'Pr Passes', 'Pr passes/90', 'K Pas', 'K Ps/90',
        'OP-KP', 'OP-KP/90', 'CCC', 'Ch C/90', 'Cr A', 'Crs A/90', 'Cr C', 'Cr C/90', 'Cr C/A', 'OP-Crs A',
        'OP-Crs A/90', 'OP-Crs C', 'OP-Crs C/90', 'OP-Cr %', 'Drb', 'Drb/90', 'FA', 'Off', 'Sprints/90', 'Tck A',
        'Tck/90', 'Tck C', 'Tck R', 'K Tck', 'K Tck/90', 'Itc', 'Int/90', 'Blk', 'Blk/90', 'Shts Blckd',
        'Shts Blckd/90', 'Clear', 'Clr/90', 'Fls', 'Yel', 'Red', 'Gl Mst', 'Hdrs A', 'Aer A/90', 'Hdrs', 'Hdrs W/90',
        'Hdrs L/90', 'Hdr %', 'K Hdrs/90', 'Pres A', 'Pres A/90', 'Pres C', 'Pres C/90', 'Shutouts', 'Cln/90',
        'Conc', 'All/90', 'Last C', 'xGP', 'xGP/90', 'Svh', 'Svp', 'Svt', 'Saves/90', 'Sv %', 'xSv %', 'Pens Faced',
        'Pens Saved', 'Pens Saved Ratio'
    ]
    dialog = StatWeightsDialog(root, stats_list)
    return dialog.selected_stats

