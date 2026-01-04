import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Menu
from database import df, RenovationLogic, DELIVERY_FLAT_RATE, INSTALLATION_FLAT_RATE
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime


# [HAZIQ] MAIN APPLICATION SETUP
class RenovationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RENOVISION: Smart Interior Assistant")
        self.geometry("1100x800")

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

    # [HAZIQ] CENTERING POPUPS
    def center_popup(self, popup, width, height):
        self.update_idletasks()
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_w = self.winfo_width()
        main_h = self.winfo_height()
        x = main_x + (main_w // 2) - (width // 2)
        y = main_y + (main_h // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

    def create_menu(self):
        my_menu = Menu(self)
        self.config(menu=my_menu)

        file_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="File", menu=file_menu)
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


# [AMANINA] HOME PAGE DESIGN
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.center_box = tk.Frame(self)
        self.center_box.place(relx=0.5, rely=0.5, anchor="center")

        self.logo_img = None
        try:
            load = Image.open("images/logo.png")
            load = load.resize((150, 150), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(load)
            tk.Label(self.center_box, image=self.logo_img).pack(pady=10)
        except Exception:
            tk.Label(self.center_box, text="[LOGO]", font=("Arial", 20, "bold")).pack(pady=10)

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


# [AMANINA] DASHBOARD
class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.top_bar = tk.Frame(self)
        self.top_bar.pack(fill="x", side="top", padx=10, pady=10)

        self.logo_img = None
        try:
            load = Image.open("images/logo.png")
            load = load.resize((50, 50), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(load)
            tk.Label(self.top_bar, image=self.logo_img).pack(side="left")
        except:
            pass

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

        # [AMANINA] ORANGE THEME
        make_btn("HOME PAGE", lambda: controller.show_frame("HomePage"), "#FFA94D")
        make_btn("MATERIAL MENU", lambda: controller.show_frame("MaterialPage"), "#FFA94D")
        make_btn("CONSULTATION", lambda: controller.show_frame("CalculatorPage"), "#FFA94D")
        make_btn("EXIT", controller.quit, "#FFA94D")

    def update_colors(self, c):
        self.config(bg=c["bg"])
        self.center_box.config(bg=c["bg"])
        self.top_bar.config(bg=c["bg"])
        for lbl in self.labels:
            lbl.config(bg=c["bg"], fg=c["fg"])


# [KER QIN] MATERIAL CATALOG PAGE
class MaterialPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.header_frame = tk.Frame(self)
        self.header_frame.pack(fill="x", padx=20, pady=20)

        self.logo_img = None
        try:
            load = Image.open("images/logo.png")
            load = load.resize((50, 50), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(load)
            tk.Label(self.header_frame, image=self.logo_img).pack(side="left", padx=(0, 10))
        except:
            pass

        self.title_lbl = tk.Label(self.header_frame, text="Material Catalog", font=("Arial", 20, "bold"))
        self.title_lbl.pack(side="left")
        tk.Button(self.header_frame, text="Back to Menu",
                  command=lambda: controller.show_frame("DashboardPage")).pack(side="right")

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # [KER QIN] SPLIT LAYOUT (FLOOR VS WALL)
        self.floor_frame = tk.Frame(self.content_frame)
        self.floor_frame.pack(side="left", fill="both", expand=True, padx=10)
        self.lbl_floor = tk.Label(self.floor_frame, text="Flooring Options", font=("Arial", 14, "bold"))
        self.lbl_floor.pack(anchor="w", pady=5)
        self.floor_list = tk.Listbox(self.floor_frame, font=("Arial", 12), height=15, exportselection=False)
        self.floor_list.pack(side="left", fill="both", expand=True)
        floor_scroll = tk.Scrollbar(self.floor_frame, command=self.floor_list.yview)
        floor_scroll.pack(side="left", fill="y")
        self.floor_list.config(yscrollcommand=floor_scroll.set)

        self.wall_frame = tk.Frame(self.content_frame)
        self.wall_frame.pack(side="right", fill="both", expand=True, padx=10)
        self.lbl_wall = tk.Label(self.wall_frame, text="Wall Finishes", font=("Arial", 14, "bold"))
        self.lbl_wall.pack(anchor="w", pady=5)
        self.wall_list = tk.Listbox(self.wall_frame, font=("Arial", 12), height=15, exportselection=False)
        self.wall_list.pack(side="left", fill="both", expand=True)
        wall_scroll = tk.Scrollbar(self.wall_frame, command=self.wall_list.yview)
        wall_scroll.pack(side="left", fill="y")
        self.wall_list.config(yscrollcommand=wall_scroll.set)

        self.floor_list.bind("<<ListboxSelect>>", lambda e: self.wall_list.selection_clear(0, "end"))
        self.wall_list.bind("<<ListboxSelect>>", lambda e: self.floor_list.selection_clear(0, "end"))

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(fill="x", pady=20)
        tk.Button(self.btn_frame, text="VIEW SPEC & IMAGE ➤",
                  font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", height=2,
                  command=self.open_popup).pack()
        self.load_list()

    def load_list(self):
        self.floor_list.delete(0, "end")
        self.wall_list.delete(0, "end")
        for index, row in df.iterrows():
            if row['Type'] == 'Floor':
                self.floor_list.insert("end", row['Material'])
            elif row['Type'] == 'Wall':
                self.wall_list.insert("end", row['Material'])

    def open_popup(self):
        selection = None
        if self.floor_list.curselection():
            selection = self.floor_list.get(self.floor_list.curselection())
        elif self.wall_list.curselection():
            selection = self.wall_list.get(self.wall_list.curselection())
        if not selection:
            messagebox.showwarning("Selection", "Please select a material first.")
            return
        row = df[df['Material'] == selection].iloc[0]

        popup = tk.Toplevel(self)
        popup.title(f"{selection} - Details")
        self.controller.center_popup(popup, 500, 450)

        c = self.controller.colors[self.controller.current_mode]
        popup.config(bg=c["bg"])
        img_frame = tk.Frame(popup, width=400, height=200, bg="grey")
        img_frame.pack(pady=20)
        img_frame.pack_propagate(False)

        # [KER QIN] VARIABLES
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
        self.floor_frame.config(bg=c["bg"])
        self.wall_frame.config(bg=c["bg"])
        self.btn_frame.config(bg=c["bg"])
        self.lbl_floor.config(bg=c["bg"], fg=c["fg"])
        self.lbl_wall.config(bg=c["bg"], fg=c["fg"])
        self.floor_list.config(bg=c["input_bg"], fg=c["fg"])
        self.wall_list.config(bg=c["input_bg"], fg=c["fg"])


# [AIMAN] CALCULATOR PAGE
class CalculatorPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.final_room_image = None
        self.last_results = None
        self.top_bar = tk.Frame(self)
        self.top_bar.pack(fill="x", side="top", padx=10, pady=10)

        self.logo_img = None
        try:
            load = Image.open("images/logo.png")
            load = load.resize((50, 50), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(load)
            tk.Label(self.top_bar, image=self.logo_img).pack(side="left", padx=(0, 10))
        except:
            pass

        tk.Label(self.top_bar, text="Consultation", font=("Arial", 20, "bold")).pack(side="left")
        tk.Button(self.top_bar, text="Back to Menu",
                  command=lambda: controller.show_frame("DashboardPage")).pack(side="right")

        self.left_pane = tk.Frame(self, padx=15, pady=15)
        self.left_pane.place(relx=0, rely=0.1, relwidth=0.4, relheight=0.9)
        self.right_pane = tk.Frame(self, padx=20, pady=20)
        self.right_pane.place(relx=0.4, rely=0.1, relwidth=0.6, relheight=0.9)
        self.labels = []
        self.setup_inputs(self.left_pane)
        self.setup_outputs(self.right_pane)

    def setup_inputs(self, parent):
        input_container = tk.Frame(parent)
        input_container.pack(fill="both", expand=True)
        self.input_container = input_container
        col1 = tk.Frame(input_container)
        col1.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.col1 = col1
        col2 = tk.Frame(input_container)
        col2.pack(side="right", fill="both", expand=True, padx=(5, 0))
        self.col2 = col2

        def create_lbl(container, text):
            lbl = tk.Label(container, text=text, font=("Arial", 9, "bold"), anchor="w")
            lbl.pack(fill="x", pady=(5, 0))
            self.labels.append(lbl)
            return lbl

        create_lbl(col1, "Room Type:")
        self.room_var = tk.StringVar(value="Living Room")
        ttk.Combobox(col1, textvariable=self.room_var,
                     values=["Living Room", "Bedroom", "Kitchen", "Bathroom"]).pack(fill="x", ipady=3)
        create_lbl(col1, "Flooring:")
        self.floor_var = tk.StringVar()
        self.floor_combo = ttk.Combobox(col1, textvariable=self.floor_var,
                                        values=list(df[df['Type'] == 'Floor']['Material']))
        self.floor_combo.pack(fill="x", ipady=3)
        self.floor_combo.bind("<<ComboboxSelected>>", self.update_tile_choices)
        create_lbl(col1, "Wall Finish:")
        self.wall_var = tk.StringVar()
        ttk.Combobox(col1, textvariable=self.wall_var,
                     values=list(df[df['Type'] == 'Wall']['Material'])).pack(fill="x", ipady=3)
        create_lbl(col1, "Tile Size (cm):")
        self.tile_var = tk.StringVar()
        self.tile_combo = ttk.Combobox(col1, textvariable=self.tile_var, values=["30x30 cm", "60x60 cm"])
        self.tile_combo.pack(fill="x", ipady=3)
        self.tile_combo.current(0)

        tk.Label(col2, text="--- FLOOR SIZE ---", font=("Arial", 9, "bold", "italic"), fg="grey").pack(fill="x",
                                                                                                       pady=(10, 2))
        create_lbl(col2, "Floor Width (m):")
        self.width_entry = tk.Entry(col2)
        self.width_entry.pack(fill="x", ipady=3)
        create_lbl(col2, "Floor Length (m):")
        self.length_entry = tk.Entry(col2)
        self.length_entry.pack(fill="x", ipady=3)

        tk.Label(col2, text="--- WALL SIZE ---", font=("Arial", 9, "bold", "italic"), fg="grey").pack(fill="x",
                                                                                                      pady=(10, 2))
        create_lbl(col2, "Wall Height (m):")
        self.height_entry = tk.Entry(col2)
        self.height_entry.pack(fill="x", ipady=3)
        self.height_entry.insert(0, "3.0")

        tk.Label(col2, text="--- FINANCIAL ---", font=("Arial", 9, "bold", "italic"), fg="grey").pack(fill="x",
                                                                                                      pady=(10, 2))
        create_lbl(col2, "Budget (RM):")
        self.budget_entry = tk.Entry(col2)
        self.budget_entry.pack(fill="x", ipady=3)

        self.is_member = tk.BooleanVar()
        tk.Checkbutton(col2, text="Member Discount (5%)", variable=self.is_member,
                       font=("Arial", 9, "bold")).pack(fill="x", pady=(10, 0))

        self.btn_frame = tk.Frame(parent)
        self.btn_frame.pack(fill="x", pady=20, side="bottom")
        tk.Button(self.btn_frame, text="CALCULATE PLAN", bg="blue", fg="white",
                  font=("Arial", 11, "bold"), command=self.run_calc).pack(fill="x", pady=5, ipady=3)
        self.btn_print = tk.Button(self.btn_frame, text="PRINT INVOICE", bg="grey", fg="white",
                                   font=("Arial", 11, "bold"), state="disabled",
                                   command=self.save_receipt)
        self.btn_print.pack(fill="x", pady=5, ipady=3)

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
        self.input_container.config(bg=c["frame_bg"])
        self.col1.config(bg=c["frame_bg"])
        self.col2.config(bg=c["frame_bg"])
        self.btn_frame.config(bg=c["frame_bg"])
        for lbl in self.labels:
            try:
                lbl.config(bg=c["frame_bg"] if lbl.master in [self.left_pane, self.col1, self.col2] else c["bg"],
                           fg=c["fg"])
            except tk.TclError:
                pass
        for parent_frame in [self.col1, self.col2]:
            for widget in parent_frame.winfo_children():
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

        # [HAZIQ] SAFETY CHECK
        is_safe, msg = RenovationLogic.check_safety(r_type, f_mat)
        if not is_safe:
            messagebox.showwarning("Safety Lock", msg)
            return
        try:
            w = float(self.width_entry.get())
            l = float(self.length_entry.get())
            h = float(self.height_entry.get())
            b = float(self.budget_entry.get())

            # [HAZIQ] INPUT VALIDATION
            if w <= 0 or l <= 0 or h <= 0 or b < 0:
                messagebox.showerror("Input Error", "Dimensions must be greater than 0.\nBudget cannot be negative.")
                return
        except Exception:
            messagebox.showerror("Error", "Please check your numbers.")
            return

        self.last_results = RenovationLogic.calculate_project(w, l, h, f_mat, self.wall_var.get(), self.tile_var.get())

        # [AIMAN] DISCOUNT CALCULATION LOGIC
        if self.is_member.get():
            discount_amount = self.last_results['total_cost'] * 0.05
            self.last_results['total_cost'] -= discount_amount
            # Store discount for invoice receipt
            self.last_results['discount'] = discount_amount
        else:
            self.last_results['discount'] = 0.0

        self.lbl_cost.config(text=f"Total Estimate: RM {self.last_results['total_cost']:.2f}")
        self.btn_print.config(state="normal", bg="#4CAF50")

        try:
            CANVAS_W, CANVAS_H = 400, 250
            # [KER QIN] FAUX 3D RENDER OF ROOM
            wall_img = Image.open(self.last_results['wall_img']).resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
            final_img = wall_img.copy()
            floor_tex = Image.open(self.last_results['floor_img']).resize((CANVAS_W, CANVAS_H),
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

    # [HAZIQ] PRINT INVOICE
    def save_receipt(self):
        if not self.last_results:
            messagebox.showwarning("Warning", "Please run a calculation first.")
            return
        win = tk.Toplevel(self)
        win.title("Service Selection")
        self.controller.center_popup(win, 400, 300)
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

        # [NEW] Logic to show discount if applied
        discount_text = ""
        if res.get('discount', 0) > 0:
            discount_text = f"Member Discount (5%):                           -RM {res['discount']:>7.2f}\n{thin_line}"

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
  Ceiling Height: {self.height_entry.get()}m
  Tile Size:      {self.tile_var.get()}

{thin_line}
ITEMIZED BREAKDOWN
{thin_line}
{'ITEM':<25} | {'QTY':<10} | {'UNIT PRICE':<10} | {'TOTAL':>10}
{thin_line}
FLOORING: {self.floor_var.get():<15} | {res['floor_area']:<6.1f} sqm | RM {res['floor_price']:<7.2f} | RM {res['floor_cost']:>7.2f}
WALL: {self.wall_var.get():<19} | {res['wall_area']:<6.1f} sqm | RM {res['wall_price']:<7.2f} | RM {res['wall_cost']:>7.2f}
{thin_line}
Subtotal (Materials):                               RM {res['total_cost'] + res.get('discount', 0):>7.2f}
{discount_text}
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