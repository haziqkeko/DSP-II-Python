import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Menu
from database import df, RenovationLogic, DELIVERY_FLAT_RATE, INSTALLATION_FLAT_RATE
from PIL import Image, ImageTk, ImageDraw
import os
from datetime import datetime


class RenovationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RENOVISION: Smart Interior Assistant")
        self.geometry("1100x800")

        # --- THEME CONFIGURATION ---
        self.current_mode = "light"
        self.dark_mode_var = tk.BooleanVar(value=False)
        self.colors = {
            "light": {
                "bg": "#f0f0f0", "fg": "black",
                "frame_bg": "#f0f0f0", "input_bg": "white",
                "chart_bg": "#f0f0f0", "canvas_bg": "#e0e0e0",
                "btn_bg": "#e1e1e1"
            },
            "dark": {
                "bg": "#2b2b2b", "fg": "#ffffff",
                "frame_bg": "#2b2b2b", "input_bg": "#3a3a3a",
                "chart_bg": "#2b2b2b", "canvas_bg": "#404040",
                "btn_bg": "#4a4a4a"
            }
        }

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.create_menu()

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, DashboardPage, MaterialPage, CalculatorPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_frame("HomePage")
        self.apply_theme()

    def create_menu(self):
        my_menu = Menu(self)
        self.config(menu=my_menu)

        file_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="File", menu=file_menu)
        # UPDATED: Removed "Save Receipt" from here as requested
        file_menu.add_command(label="Exit", command=self.quit)

        view_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Dark Mode", onvalue=True, offvalue=False,
                                  variable=self.dark_mode_var, command=self.toggle_theme)

        help_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "RENOVISION v1.0"))

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def toggle_theme(self):
        if self.dark_mode_var.get():
            self.current_mode = "dark"
        else:
            self.current_mode = "light"
        self.apply_theme()

    def apply_theme(self):
        c = self.colors[self.current_mode]
        self.config(bg=c["bg"])
        self.container.config(bg=c["bg"])
        self.style.configure("TCombobox", fieldbackground=c["input_bg"], background=c["bg"], foreground=c["fg"])
        self.style.map("TCombobox", fieldbackground=[("readonly", c["input_bg"])],
                       selectbackground=[("readonly", c["bg"])])

        self.style.configure("Treeview", background=c["input_bg"], foreground=c["fg"], fieldbackground=c["input_bg"])
        self.style.configure("Treeview.Heading", background=c["btn_bg"], foreground=c["fg"])

        for frame in self.frames.values():
            frame.update_colors(c)


# --- PAGE 1: WELCOME SCREEN ---
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.center_box = tk.Frame(self)
        self.center_box.place(relx=0.5, rely=0.5, anchor="center")

        self.title_lbl = tk.Label(self.center_box, text="RENOVISION", font=("Arial", 36, "bold"))
        self.title_lbl.pack(pady=5)

        self.sub_lbl = tk.Label(self.center_box, text="Smart Interior Assistant", font=("Arial", 16))
        self.sub_lbl.pack(pady=(0, 40))

        tk.Button(self.center_box, text="START PROJECT",
                  command=lambda: controller.show_frame("DashboardPage"),
                  font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                  padx=30, pady=10).pack()

    def update_colors(self, c):
        self.config(bg=c["bg"])
        self.center_box.config(bg=c["bg"])
        self.title_lbl.config(bg=c["bg"], fg=c["fg"])
        self.sub_lbl.config(bg=c["bg"], fg="grey" if self.controller.current_mode == "light" else "#aaaaaa")


# --- PAGE 2: DASHBOARD ---
class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.center_box = tk.Frame(self)
        self.center_box.place(relx=0.5, rely=0.5, anchor="center")
        self.labels = []

        title = tk.Label(self.center_box, text="MAIN MENU", font=("Arial", 24, "bold"))
        title.pack(pady=(0, 30))
        self.labels.append(title)

        def make_btn(text, command, color):
            btn = tk.Button(self.center_box, text=text, font=("Arial", 12, "bold"),
                            bg=color, fg="black", width=25, height=2,
                            command=command)
            btn.pack(pady=10)
            return btn

        make_btn("HOME PAGE", lambda: controller.show_frame("HomePage"), "#FFD1DC")
        make_btn("MATERIAL MENU", lambda: controller.show_frame("MaterialPage"), "#FFD1DC")
        make_btn("CONSULTATION", lambda: controller.show_frame("CalculatorPage"), "#FFD1DC")
        make_btn("EXIT", controller.quit, "#FFD1DC")

    def update_colors(self, c):
        self.config(bg=c["bg"])
        self.center_box.config(bg=c["bg"])
        for lbl in self.labels:
            lbl.config(bg=c["bg"], fg=c["fg"])


# --- PAGE 3: MATERIAL CATALOG ---
class MaterialPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.header_frame = tk.Frame(self)
        self.header_frame.pack(fill="x", padx=20, pady=20)

        self.title_lbl = tk.Label(self.header_frame, text="Material Catalog", font=("Arial", 20, "bold"))
        self.title_lbl.pack(side="left")

        tk.Button(self.header_frame, text="Back to Menu",
                  command=lambda: controller.show_frame("DashboardPage")).pack(side="right")

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=20)

        tk.Label(self.content_frame, text="Select a material to view details:", font=("Arial", 12)).pack(anchor="w")

        self.material_list = tk.Listbox(self.content_frame, font=("Arial", 14), height=15)
        self.material_list.pack(side="left", fill="both", expand=True, padx=(0, 20))

        scrollbar = tk.Scrollbar(self.content_frame)
        scrollbar.pack(side="left", fill="y")
        self.material_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.material_list.yview)

        tk.Button(self.content_frame, text="VIEW SPEC & IMAGE ➤",
                  font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", height=2,
                  command=self.open_popup).pack(side="right", anchor="n")

        self.load_list()

    def load_list(self):
        for material in df['Material']:
            self.material_list.insert("end", material)

    def open_popup(self):
        try:
            selection = self.material_list.get(self.material_list.curselection())
        except tk.TclError:
            messagebox.showwarning("Selection", "Please select a material first.")
            return

        row = df[df['Material'] == selection].iloc[0]

        popup = tk.Toplevel(self)
        popup.title(f"{selection} - Details")
        popup.geometry("500x450")

        c = self.controller.colors[self.controller.current_mode]
        popup.config(bg=c["bg"])

        img_frame = tk.Frame(popup, width=400, height=200, bg="grey")
        img_frame.pack(pady=20)
        img_frame.pack_propagate(False)

        image_name = row['Image_File']

        try:
            load = Image.open(image_name)
            load = load.resize((400, 200), Image.Resampling.LANCZOS)
            render = ImageTk.PhotoImage(load)

            img_label = tk.Label(img_frame, image=render, bg="grey")
            img_label.image = render
            img_label.pack(fill="both", expand=True)

        except FileNotFoundError:
            lbl = tk.Label(img_frame, text=f"Image not found:\n{image_name}", bg="lightgrey", fg="red")
            lbl.pack(fill="both", expand=True)

        info_text = (
            f"Type: {row['Type']}\n\n"
            f"Price: RM {row['Price_Per_Sqm']:.2f} / sqm\n\n"
            f"Waterproof: {'YES' if row['Is_Waterproof'] else 'NO'}"
        )

        tk.Label(popup, text=selection, font=("Arial", 18, "bold"), bg=c["bg"], fg=c["fg"]).pack()
        tk.Label(popup, text=info_text, font=("Arial", 12), bg=c["bg"], fg=c["fg"], justify="left").pack(pady=10)

        tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

    def update_colors(self, c):
        self.config(bg=c["bg"])
        self.header_frame.config(bg=c["bg"])
        self.content_frame.config(bg=c["bg"])
        self.title_lbl.config(bg=c["bg"], fg=c["fg"])
        self.material_list.config(bg=c["input_bg"], fg=c["fg"])


# --- PAGE 4: CALCULATOR (COMPOSITE 3D ROOM) ---
class CalculatorPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.final_room_image = None
        self.last_results = None

        top_bar = tk.Frame(self, height=40)
        top_bar.pack(fill="x", side="top")
        self.top_bar = top_bar

        tk.Button(top_bar, text="< Back to Menu",
                  command=lambda: controller.show_frame("DashboardPage")).pack(side="left", padx=10, pady=5)

        self.left_pane = tk.Frame(self, padx=20, pady=20)
        self.left_pane.pack(side="left", fill="both", expand=True)

        self.right_pane = tk.Frame(self, padx=20, pady=20)
        self.right_pane.pack(side="right", fill="both", expand=True)

        self.labels = []
        self.setup_inputs(self.left_pane)
        self.setup_outputs(self.right_pane)

    def setup_inputs(self, parent):
        def create_lbl(text):
            lbl = tk.Label(parent, text=text, font=("Arial", 10, "bold"), anchor="w")
            lbl.pack(fill="x", pady=(10, 0))
            self.labels.append(lbl)
            return lbl

        create_lbl("Room Type:")
        self.room_var = tk.StringVar(value="Living Room")
        ttk.Combobox(parent, textvariable=self.room_var,
                     values=["Living Room", "Bedroom", "Kitchen", "Bathroom"]).pack(fill="x", ipady=5)

        create_lbl("Flooring Material:")
        self.floor_var = tk.StringVar()
        self.floor_combo = ttk.Combobox(parent, textvariable=self.floor_var,
                                        values=list(df[df['Type'] == 'Floor']['Material']))
        self.floor_combo.pack(fill="x", ipady=5)
        self.floor_combo.bind("<<ComboboxSelected>>", self.update_tile_choices)

        create_lbl("Wall Finish:")
        self.wall_var = tk.StringVar()
        ttk.Combobox(parent, textvariable=self.wall_var,
                     values=list(df[df['Type'] == 'Wall']['Material'])).pack(fill="x", ipady=5)

        create_lbl("Room Width (meters):")
        self.width_entry = tk.Entry(parent)
        self.width_entry.pack(fill="x", ipady=5)

        create_lbl("Room Length (meters):")
        self.length_entry = tk.Entry(parent)
        self.length_entry.pack(fill="x", ipady=5)

        create_lbl("Ceiling Height (meters):")
        self.height_var = tk.StringVar(value="3.0")
        tk.Spinbox(parent, from_=2.0, to=10.0, increment=0.1,
                   textvariable=self.height_var).pack(fill="x", ipady=5)

        create_lbl("Tile Size (cm):")
        self.tile_var = tk.StringVar()
        self.tile_combo = ttk.Combobox(parent, textvariable=self.tile_var, values=["30x30 cm", "60x60 cm"])
        self.tile_combo.pack(fill="x", ipady=5)
        self.tile_combo.current(0)

        create_lbl("Max Budget (RM):")
        self.budget_entry = tk.Entry(parent)
        self.budget_entry.pack(fill="x", ipady=5)

        tk.Button(parent, text="CALCULATE PLAN", bg="blue", fg="white",
                  font=("Arial", 12, "bold"), command=self.run_calc).pack(fill="x", pady=(20, 5), ipady=5)

        # UPDATED: Print Button is here, initially disabled
        self.btn_print = tk.Button(parent, text="PRINT INVOICE", bg="grey", fg="white",
                                   font=("Arial", 12, "bold"), state="disabled",
                                   command=self.save_receipt)
        self.btn_print.pack(fill="x", pady=5, ipady=5)

    def update_tile_choices(self, event):
        selection = self.floor_var.get()
        if selection in ["Vinyl", "Solid Wood"]:
            self.tile_combo['values'] = ["15x90 cm"]
            self.tile_var.set("15x90 cm")
        else:
            self.tile_combo['values'] = ["30x30 cm", "60x60 cm"]
            self.tile_var.set("30x30 cm")

    def setup_outputs(self, parent):
        self.preview_lbl = tk.Label(parent, text="3D Room Preview", font=("Arial", 14))
        self.preview_lbl.pack(pady=10)
        self.labels.append(self.preview_lbl)

        self.blueprint = tk.Canvas(parent, width=400, height=250, bd=2, relief="sunken", bg="grey")
        self.blueprint.pack(pady=10)
        self.image_container = self.blueprint.create_image(0, 0, anchor="nw", image=None)

        self.lbl_cost = tk.Label(parent, text="Total Estimate: RM 0.00", font=("Arial", 16, "bold"), fg="green")
        self.lbl_cost.pack(pady=20)

        self.lbl_budget_feedback = tk.Label(parent, text="", font=("Arial", 12, "italic"), wraplength=400)
        self.lbl_budget_feedback.pack(pady=10)
        self.labels.append(self.lbl_budget_feedback)

    def update_colors(self, c):
        self.config(bg=c["bg"])
        self.top_bar.config(bg=c["bg"])
        self.left_pane.config(bg=c["frame_bg"])
        self.right_pane.config(bg=c["bg"])

        for lbl in self.labels:
            try:
                lbl.config(bg=c["frame_bg"] if lbl.master == self.left_pane else c["bg"], fg=c["fg"])
            except tk.TclError:
                pass

        for widget in self.left_pane.winfo_children():
            try:
                if isinstance(widget, tk.Entry) or isinstance(widget, tk.Spinbox):
                    widget.config(bg=c["input_bg"], fg=c["fg"], insertbackground=c["fg"])
            except tk.TclError:
                pass

        self.lbl_cost.config(bg=c["bg"])
        self.lbl_budget_feedback.config(bg=c["bg"])

    def run_calc(self):
        r_type = self.room_var.get()
        f_mat = self.floor_var.get()
        is_safe, msg = RenovationLogic.check_safety(r_type, f_mat)
        if not is_safe:
            messagebox.showwarning("Safety Lock", msg)
            return

        try:
            w = float(self.width_entry.get())
            l = float(self.length_entry.get())
            h = float(self.height_var.get())
            b = float(self.budget_entry.get())
        except Exception:
            messagebox.showerror("Error", "Please check your numbers.")
            return

        self.last_results = RenovationLogic.calculate_project(w, l, h, f_mat, self.wall_var.get(), self.tile_var.get())

        self.lbl_cost.config(text=f"Total Estimate: RM {self.last_results['total_cost']:.2f}")

        # UPDATED: Enable the Print Button
        self.btn_print.config(state="normal", bg="#4CAF50")  # Turn Green

        try:
            CANVAS_W, CANVAS_H = 400, 250
            wall_img = Image.open(self.last_results['wall_image']).resize((CANVAS_W, CANVAS_H),
                                                                          Image.Resampling.LANCZOS)
            final_img = wall_img.copy()

            floor_tex = Image.open(self.last_results['floor_image']).resize((CANVAS_W, CANVAS_H),
                                                                            Image.Resampling.LANCZOS)

            floor_mask = Image.new("L", (CANVAS_W, CANVAS_H), 0)
            draw_floor = ImageDraw.Draw(floor_mask)
            floor_poly = [(0, 250), (400, 250), (300, 150), (100, 150)]
            draw_floor.polygon(floor_poly, fill=255)

            final_img.paste(floor_tex, (0, 0), floor_mask)

            ceiling_mask = Image.new("L", (CANVAS_W, CANVAS_H), 0)
            draw_ceil = ImageDraw.Draw(ceiling_mask)
            ceil_poly = [(0, 0), (400, 0), (300, 50), (100, 50)]
            draw_ceil.polygon(ceil_poly, fill=255)

            grey_block = Image.new("RGB", (CANVAS_W, CANVAS_H), (220, 220, 220))
            final_img.paste(grey_block, (0, 0), ceiling_mask)

            draw_lines = ImageDraw.Draw(final_img)
            draw_lines.rectangle([100, 50, 300, 150], outline="grey", width=2)
            draw_lines.line([(0, 0), (100, 50)], fill="grey", width=2)
            draw_lines.line([(400, 0), (300, 50)], fill="grey", width=2)
            draw_lines.line([(0, 250), (100, 150)], fill="grey", width=2)
            draw_lines.line([(400, 250), (300, 150)], fill="grey", width=2)

            self.final_room_image = ImageTk.PhotoImage(final_img)
            self.blueprint.itemconfig(self.image_container, image=self.final_room_image)

        except Exception as e:
            print(f"3D Render Error: {e}")
            self.blueprint.create_rectangle(0, 0, 400, 250, fill="grey")
            self.blueprint.create_text(200, 125, text="Image Load Error")

        self.update_budget_feedback(self.last_results['total_cost'], b)

    def update_budget_feedback(self, cost, budget):
        balance = budget - cost
        pct_left = balance / budget

        if balance < 0:
            msg = f"⚠ Budget Exceeded by RM {abs(balance):.2f}\nConsider cheaper options."
            color = "red"
        elif pct_left < 0.20:
            msg = f"✓ Balance: RM {balance:.2f}\nStatus: On Target."
            color = "#ff8800"
        else:
            msg = f"✓ Balance: RM {balance:.2f}\nStatus: Under Budget."
            color = "green"

        self.lbl_budget_feedback.config(text=msg, fg=color)

    def save_receipt(self):
        if not self.last_results:
            messagebox.showwarning("Warning", "Please run a calculation first.")
            return

        win = tk.Toplevel(self)
        win.title("Service Selection")
        win.geometry("400x300")

        tk.Label(win, text="Select Service Option:", font=("Arial", 14, "bold")).pack(pady=20)

        def finalize(service_fee, service_name):
            win.destroy()
            self.generate_ascii_invoice(service_fee, service_name)

        tk.Button(win, text="Self Collect (No Extra Charge)", width=30, height=2,
                  command=lambda: finalize(0, "Self Collection")).pack(pady=5)

        tk.Button(win, text=f"Delivery Only (+RM {DELIVERY_FLAT_RATE})", width=30, height=2,
                  command=lambda: finalize(DELIVERY_FLAT_RATE, "Delivery Only")).pack(pady=5)

        tk.Button(win, text=f"Delivery + Installation (+RM {INSTALLATION_FLAT_RATE})", width=30, height=2,
                  command=lambda: finalize(INSTALLATION_FLAT_RATE, "Delivery & Installation")).pack(pady=5)

    def generate_ascii_invoice(self, service_fee, service_name):
        res = self.last_results
        grand_total = res['total_cost'] + service_fee
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ascii_header = r"""
  _____  ______ _   _  _____      _______ _____ _____ ____  _   _ 
 |  __ \|  ____| \ | |/ _ \ \    / /_   _/ ____|_   _/ __ \| \ | |
 | |__) | |__  |  \| | | | \ \  / /  | || (___   | || |  | |  \| |
 |  _  /|  __| | . ` | | | |\ \/ /   | | \___ \  | || |  | | . ` |
 | | \ \| |____| |\  | |_| | \  /   _| |_|___) |_| || |__| | |\  |
 |_|  \_\______|_| \_|\___/   \/   |_____|_____/_____\____/|_| \_|
        """

        line = "=" * 60
        thin_line = "-" * 60

        text_content = f"""
{ascii_header}

{line}
OFFICIAL INVOICE
{line}
Date: {date_str}
Client Order: #RV-{int(datetime.now().timestamp())}
{line}

PROJECT SPECIFICATIONS:
  Room Type:      {self.room_var.get()}
  Dimensions:     {self.width_entry.get()}m x {self.length_entry.get()}m
  Ceiling Height: {self.height_var.get()}m
  Tile Size:      {self.tile_var.get()}

{thin_line}
ITEMIZED BREAKDOWN
{thin_line}
{'ITEM':<25} | {'QTY':<10} | {'UNIT PRICE':<10} | {'TOTAL':>10}
{thin_line}
FLOORING: {self.floor_var.get():<15} | {res['floor_area']:<6.1f} sqm | RM {res['floor_price_unit']:<7.2f} | RM {res['floor_cost']:>7.2f}
WALL: {self.wall_var.get():<19} | {res['wall_area']:<6.1f} sqm | RM {res['wall_price_unit']:<7.2f} | RM {res['wall_cost']:>7.2f}
{thin_line}
Subtotal (Materials):                               RM {res['total_cost']:>7.2f}
Service ({service_name}):                           RM {service_fee:>7.2f}
{line}
GRAND TOTAL:                                        RM {grand_total:>7.2f}
{line}

Thank you for choosing RENOVISION!
"""
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile="Renovision_Invoice.txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if path:
            with open(path, "w") as f:
                f.write(text_content)
            messagebox.showinfo("Success", "Invoice saved successfully!")