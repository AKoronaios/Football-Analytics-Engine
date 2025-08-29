import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Listbox, Scrollbar, VERTICAL, MULTIPLE, END, StringVar


class FilterWindow:
    def __init__(self, master, df, callback):
        self.df = df
        self.filtered_df = df.copy()
        self.callback = callback

        self.window = ttk.Toplevel(master)
        self.window.title("Filter Data")
        self.window.geometry("800x800")

        self.min_apps_var = ttk.IntVar(value=0)
        self.age_min = ttk.IntVar(value=14)
        self.age_max = ttk.IntVar(value=55)
        self.salary_min = ttk.IntVar(value=int(df["Salary"].min()))
        self.salary_max = ttk.IntVar(value=int(df["Salary"].max()))

        self.age_min_label = StringVar(value=str(self.age_min.get()))
        self.age_max_label = StringVar(value=str(self.age_max.get()))

        frame = ttk.Frame(self.window, padding=10)
        frame.pack(fill=BOTH, expand=True)

        ttk.Label(frame, text="Nationality:", bootstyle="primary").grid(row=0, column=0, sticky=W)
        self.nat_listbox = Listbox(frame, height=6, selectmode=MULTIPLE)
        scrollbar_nat = Scrollbar(frame, orient=VERTICAL, command=self.nat_listbox.yview)
        self.nat_listbox.configure(yscrollcommand=scrollbar_nat.set)
        for nat in ["All"] + sorted(df["Nat"].dropna().unique().tolist()):
            self.nat_listbox.insert(END, nat)
        self.nat_listbox.grid(row=1, column=0, sticky=EW, pady=5)
        scrollbar_nat.grid(row=1, column=1, sticky=NS)

        ttk.Label(frame, text="Division:", bootstyle="primary").grid(row=2, column=0, sticky=W)
        self.div_listbox = Listbox(frame, height=6, selectmode=MULTIPLE)
        scrollbar_div = Scrollbar(frame, orient=VERTICAL, command=self.div_listbox.yview)
        self.div_listbox.configure(yscrollcommand=scrollbar_div.set)
        for div in ["All"] + sorted(df["Division"].dropna().unique().tolist()):
            self.div_listbox.insert(END, div)
        self.div_listbox.grid(row=3, column=0, sticky=EW, pady=5)
        scrollbar_div.grid(row=3, column=1, sticky=NS)


        ttk.Label(frame, text="Position(s):", bootstyle="primary").grid(row=6, column=0, sticky=W)
        pos_frame = ttk.Frame(frame)
        pos_frame.grid(row=7, column=0, sticky=EW, pady=5)

        self.position_vars = {}
        position_grid = [
            [None, "STC", None],
            ["AML", "AMC", "AMR"],
            ["ML",  "MC",  "MR"],
            ["WDL", "DM",  "WDR"],
            ["DL",  "DC",  "DR"],
            [None, "GK", None]
        ]

        for r, row in enumerate(position_grid):
            for c, pos in enumerate(row):
                if pos:
                    var = ttk.BooleanVar()
                    chk = ttk.Checkbutton(pos_frame, text=pos, variable=var, bootstyle="info")
                    chk.grid(row=r, column=c, padx=2, pady=2)
                    self.position_vars[pos] = var


        ttk.Label(frame, text="Age Range:", bootstyle="primary").grid(row=8, column=0, sticky=W)
        age_frame = ttk.Frame(frame)
        age_frame.grid(row=9, column=0, sticky=W, pady=5)
        ttk.Label(age_frame, textvariable=self.age_min_label).pack(side=LEFT, padx=5)
        ttk.Scale(age_frame, from_=14, to=55, variable=self.age_min, orient=HORIZONTAL, command=self.update_age_labels).pack(side=LEFT, padx=5)
        ttk.Label(age_frame, textvariable=self.age_max_label).pack(side=LEFT, padx=5)
        ttk.Scale(age_frame, from_=14, to=55, variable=self.age_max, orient=HORIZONTAL, command=self.update_age_labels).pack(side=LEFT, padx=5)

        ttk.Label(frame, text="Salary Range:", bootstyle="primary").grid(row=10, column=0, sticky=W)
        salary_frame = ttk.Frame(frame)
        salary_frame.grid(row=11, column=0, sticky=W, pady=5)
        ttk.Label(salary_frame, text="Min:").pack(side=LEFT)
        ttk.Entry(salary_frame, textvariable=self.salary_min, width=10).pack(side=LEFT, padx=5)
        ttk.Label(salary_frame, text="Max:").pack(side=LEFT)
        ttk.Entry(salary_frame, textvariable=self.salary_max, width=10).pack(side=LEFT, padx=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=12, column=0, columnspan=2, sticky=EW, pady=20)
        ttk.Button(btn_frame, text="Apply Filters", bootstyle="success", command=self.apply_filters).pack(side=LEFT, padx=10)
        ttk.Button(btn_frame, text="Reset Filters", bootstyle="warning", command=self.reset_filters).pack(side=LEFT, padx=10)

    def update_age_labels(self, *args):
        self.age_min_label.set(f"Min Age: {self.age_min.get()}")
        self.age_max_label.set(f"Max Age: {self.age_max.get()}")

    def apply_filters(self):
        df = self.df.copy()
        selected_nat = [self.nat_listbox.get(i) for i in self.nat_listbox.curselection() if self.nat_listbox.get(i) != "All"]
        if selected_nat:
            df = df[df["Nat"].isin(selected_nat)]
        selected_div = [self.div_listbox.get(i) for i in self.div_listbox.curselection() if self.div_listbox.get(i) != "All"]
        if selected_div:
            df = df[df["Division"].isin(selected_div)]
        selected_pos = [pos for pos, var in self.position_vars.items() if var.get()]
        if selected_pos:
            df = df[df["Position"].apply(lambda pos: bool(set(selected_pos) & pos if isinstance(pos, set) else {pos}))]

        
        df = df[(df["Age"] >= self.age_min.get()) & (df["Age"] <= self.age_max.get())]
        df = df[(df["Salary"] >= self.salary_min.get()) & (df["Salary"] <= self.salary_max.get())]
        df = df[df['Apps'] >= self.min_apps_var.get()]
        self.filtered_df = df.copy()
        self.callback(self.filtered_df)
        self.window.destroy()

    def reset_filters(self):
        self.nat_listbox.selection_clear(0, END)
        self.div_listbox.selection_clear(0, END)
        for var in self.position_vars.values():
            var.set(False)
        # self.position_listbox.selection_clear(0, END)
        self.age_min.set(14)
        self.age_max.set(55)
        self.salary_min.set(int(self.df["Salary"].min()))
        self.salary_max.set(int(self.df["Salary"].max()))
        self.min_apps_var.set(0)
        self.update_age_labels()
