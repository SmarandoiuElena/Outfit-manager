from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from  PIL import Image, ImageTk
from music import resume_music, pause_music, stop_music, start_music
import os.path
import pygame
from csv_handler import save_outfits
from models import Outfit


from models import ClothingItem
from csv_handler import save_items


def about_elena():
    messagebox.showinfo("About", "Smărăndoiu Elena\nOutfit Manager App 2026")
    
def about_bianca():
    messagebox.showinfo("About", "Lazăr Bianca\nOutfit Manager App 2026")


def set_backgrond(window, image_path, x, y):

    image = Image.open(image_path)
    image = image.resize((x, y))
    photo = ImageTk.PhotoImage(image)
    
    background = Label(window, image = photo)
    background.image = photo
    background.place(x=0, y=0, relwidth=1, relheight=1)
    background.lower()
    
# making the scrollbar
# we put the frames inside the canvas and scroll the canvas 
def make_scrollable_frame(parent):
    # the frame that contains everything
    # holds the canvas and the scrollbar together
    set_backgrond(parent, "images/background/strips_bg.jpg", 800, 800)
    outer_frame = Frame(parent, bg="pink")
    outer_frame.pack(fill=BOTH, expand=True)

    outer_frame.rowconfigure(0, weight=1)
    outer_frame.columnconfigure(0, weight=0)
    outer_frame.columnconfigure(1, weight=1)
    
    # the scrollbar is on the left
    scrollbar = Scrollbar(outer_frame, orient=VERTICAL)
    scrollbar.grid(row=0, column=0, sticky="ns")

    # the canvas that scrolls
    # we link the canva to the scrollbar
    canvas = Canvas(outer_frame, bg="pink", yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=1, sticky="nsew")

    # connecting the scrollbar to the canvas
    scrollbar.config(command=canvas.yview)

    # inner frame
    # this is where we put the widgets
    inner_frame = Frame(canvas, bg="pink")
    canvas_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # update scroll region
    # how far we scroll
    def update_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    inner_frame.bind("<Configure>", update_scroll)
    
    def resize_inner(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", resize_inner)

    return inner_frame

# this is the window for creating an outfit
class create_outfit_window:
    
    def __init__(self, parent, wardrobe, home):
        self.window = parent
        self.wardrobe = wardrobe
        self.home = home
        self.build()
    
    def build(self):
        
        for widget in self.window.winfo_children():
            widget.destroy()
            
        set_backgrond(self.window, "images/background/strips_bg.jpg", 800, 800)
        inner_frame = make_scrollable_frame(self.window)

        Label(inner_frame, text="Create Outfit", bg="white",
            font=("Georgia", 24, "bold")).pack(pady=20)

        # Outfit name
        Label(inner_frame, text="Outfit name:", bg="white",
            font=("Arial", 12)).pack(anchor="w", padx=40)
        self.name_entry = Entry(inner_frame, width=40)
        self.name_entry.pack(padx=40, pady=5, anchor="w")

        self.selections = {}
        self.preview_labels = {}

        categories = ["top", "bottom", "shoes", "accessory"]

        for cat in categories:
            cat_items = self.wardrobe.filter_by_category(cat)
            item_names = [item.name for item in cat_items] or ["(none available)"]

            # Category label
            Label(inner_frame, text=f"{cat.capitalize()}:", bg="white",
              font=("Arial", 11, "bold")).pack(anchor="w", padx=40, pady=(15, 0))

            # Dropdown
            var = StringVar(value=item_names[0])
            self.selections[cat] = var

            dropdown = OptionMenu(inner_frame, var, *item_names,
                              command=lambda _, c=cat: self.update_preview(c))
            dropdown.config(width=30)
            dropdown.pack(anchor="w", padx=40, pady=3)

            # Large image preview below dropdown
            preview = Label(inner_frame, bg="white", text="no image")
            preview.pack(padx=40, pady=5, anchor="w")
            self.preview_labels[cat] = preview

            self.update_preview(cat)

        # Buttons
        btn_frame = Frame(inner_frame, bg="white")
        btn_frame.pack(pady=20)

        Button(btn_frame, text="Randomize", bg="orchid", fg="white",
            width=15, font=("Arial", 10),
            command=self.randomize).pack(side=LEFT, padx=10)

        Button(btn_frame, text="Save Outfit", bg="green", fg="white",
            width=15, font=("Arial", 10),
            command=self.save_outfit).pack(side=LEFT, padx=10)

        Button(btn_frame, text="Cancel", bg="red", fg="white",
            width=15, font=("Arial", 10),
            command=self.clear_frame).pack(side=LEFT, padx=10)
    
    def update_preview(self, category):
        selected_name = self.selections[category].get()
        item = self.wardrobe.get_item_by_name(selected_name)
        label = self.preview_labels[category]

        if item:
            try:
                image = Image.open(item.image_path)
                image = image.resize((200, 200))
                photo = ImageTk.PhotoImage(image)
                label.config(image=photo, text="")
                label.image = photo  
            except:
                label.config(image="", text="no image")
        else:
            label.config(image="", text="no image")

    def randomize(self):
        import random
        for cat, var in self.selections.items():
            cat_items = self.wardrobe.filter_by_category(cat)
            if cat_items:
                chosen = random.choice(cat_items)
                var.set(chosen.name)
                self.update_preview(cat)

    def save_outfit(self):
        outfit_name = self.name_entry.get().strip()
        if not outfit_name:
            messagebox.showerror("Error", "Please enter an outfit name!")
            return

        # Build the outfit from selected item names
        outfit = Outfit(
            name=outfit_name,
            top=self.wardrobe.get_item_by_name(self.selections["top"].get()),
            bottom=self.wardrobe.get_item_by_name(self.selections["bottom"].get()),
            shoes=self.wardrobe.get_item_by_name(self.selections["shoes"].get()),
            accessory=self.wardrobe.get_item_by_name(self.selections["accessory"].get()),
        )

        self.wardrobe.add_outfit(outfit)
        save_outfits(self.wardrobe.outfits)  # persist to outfits.csv

        messagebox.showinfo("Success", f"Outfit '{outfit_name}' saved!")
        self.clear_frame()
        self.show_home()

    def clear_frame(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        
    def show_home(self):
        self.clear_frame()
        set_backgrond(self.window, "images/background/clothes-bkg.jpg", 800, 800)

# this is the class for the setting window

class settings_window:
    
    def __init__(self, parent):
        self.window = parent
        self.build()
        
    def build(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.config(bg="pink")
        set_backgrond(self.window, "images/background/strips_bg.jpg", 800, 800)
        # title
        Label(self.window, text="Settings", bg="white",
              font=("Georgia", 24, "bold")).pack(pady=20)
        
        # ---- music section ----
        Label(self.window, text="Choose a song:", bg="white",
             font=("Arial", 14, "bold")).pack(anchor="w", padx=40, pady=10)

        # this variable stores which song is selected
        self.song_var = StringVar(value="music/Music1.mpeg")  # default selection

        Radiobutton(self.window, text="Song 1",
            variable=self.song_var,
            value="music/Music1.mpeg",
            bg="white",
            command=lambda: start_music(self.song_var.get())).pack(anchor="w", padx=40)

        Radiobutton(self.window, text="Song 2",
            variable=self.song_var,
            value="music/Music2.mpeg",
            bg="white",
            command=lambda: start_music(self.song_var.get())).pack(anchor="w", padx=40)

        Radiobutton(self.window, text="Song 3",
            variable=self.song_var,
            value="music/Music3.mpeg",
            bg="white",
            command=lambda: start_music(self.song_var.get())).pack(anchor="w", padx=40)
        
        # play / pause / stop buttons
        music_frame = Frame(self.window, bg="white")
        music_frame.pack(anchor="w", padx=40, pady=5)
        
        Button(music_frame, text="▶ Play", bg="green", fg="white",
               width=10, command=resume_music).pack(side=LEFT, padx=5)
        Button(music_frame, text="⏸ Pause", bg="orange", fg="white",
               width=10, command=pause_music).pack(side=LEFT, padx=5)
        Button(music_frame, text="⏹ Stop", bg="red", fg="white",
               width=10, command=stop_music).pack(side=LEFT, padx=5)
        
        # ---- volume section ----
        Label(self.window, text="🔊 Volume", bg="white",
              font=("Arial", 14, "bold")).pack(anchor="w", padx=40, pady=10)
        
        # volume slider
        self.volume_var = DoubleVar(value=0.5)  # default volume 50%
        volume_slider = Scale(self.window, 
                              from_=0, to=1,        # range 0 to 1
                              resolution=0.01,       # step size
                              orient=HORIZONTAL,     # horizontal slider
                              variable=self.volume_var,
                              command=self.change_volume,
                              bg="white",
                              length=300,
                              label="Volume")
        volume_slider.pack(padx=40, anchor="w")
        
    def change_volume(self, value):
        pygame.mixer.music.set_volume(float(value))
        
        
# this is the class for the view outfits window
class View_outfits_window:
    
    def __init__(self, parent, wardrobe):
        self.window = parent
        self.wardrobe = wardrobe
        self.build()
        
    def build(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        set_backgrond(self.window, "images/background/strips_bg.jpg", 800, 800)
        inner_frame = make_scrollable_frame(self.window)

        Label(inner_frame, text="My Outfits", bg="white",
              font=("Georgia", 22, "bold")).pack(pady=15)

        if not self.wardrobe.outfits:
            Label(inner_frame, text="No outfits saved yet!",
                  bg="pink", font=("Arial", 14)).pack(pady=30)
            return

        for outfit in self.wardrobe.outfits:
            # Outer card
            card = Frame(inner_frame, bg="white", bd=2, relief="groove")
            card.pack(pady=15, padx=30, fill="x")

            # Outfit name header
            Label(card, text=outfit.name, bg="pink",
                  font=("Georgia", 14, "bold")).pack(fill="x", pady=(0, 8))

            # Row of item images
            items_row = Frame(card, bg="white")
            items_row.pack(pady=5, padx=10)

            # Each slot: top, bottom, shoes, accessory
            slots = [
                ("Top",       outfit.top),
                ("Bottom",    outfit.bottom),
                ("Shoes",     outfit.shoes),
                ("Accessory", outfit.accessory),
            ]

            for label_text, item in slots:
                slot_frame = Frame(items_row, bg="white", padx=8)
                slot_frame.pack(side=LEFT)

                # Category label
                Label(slot_frame, text=label_text, bg="white",
                      font=("Arial", 9, "bold"), fg="gray").pack()

                if item:
                    try:
                        image = Image.open(item.image_path)
                        image = image.resize((100, 100))
                        photo = ImageTk.PhotoImage(image)
                        img_label = Label(slot_frame, image=photo, bg="white")
                        img_label.image = photo  # prevent garbage collection
                        img_label.pack()
                    except:
                        Label(slot_frame, text="No image", bg="#f0f0f0",
                              width=10, height=5).pack()

                    # Item name + occasion below image
                    Label(slot_frame, text=item.name, bg="white",
                          font=("Arial", 8, "bold")).pack()
                    Label(slot_frame, text=item.occasion, bg="white",
                          font=("Arial", 7), fg="gray").pack()
                else:
                    # Empty slot placeholder
                    Label(slot_frame, text="—", bg="#f5f5f5",
                          width=10, height=5).pack()

            # Buttons row
            btn_frame = Frame(card, bg="white")
            btn_frame.pack(fill="x", pady=8, padx=10)

            Button(btn_frame, text="Delete", bg="#ff4d4d", fg="white",
                   font=("Arial", 9),
                   command=lambda o=outfit: self.delete_outfit(o)).pack(side=RIGHT, padx=5)

            Button(btn_frame, text="Favourite", bg="pink",
                   font=("Arial", 9),
                   command=lambda o=outfit: self.toggle_favourite(o)).pack(side=LEFT, padx=5)

    def delete_outfit(self, outfit):
        confirm = messagebox.askyesno("Delete", f"Delete outfit '{outfit.name}'?")
        if confirm:
            self.wardrobe.remove_outfit(outfit.name)
            save_outfits(self.wardrobe.outfits)
            # Refresh the view
            for widget in self.window.winfo_children():
                widget.destroy()
            self.build()

    def toggle_favourite(self, outfit):
        # Placeholder — hook into a favourites system if you add one later
        messagebox.showinfo("Favourite", f"'{outfit.name}' added to favourites!")
           
     
# this is the class for adding an item
class add_item_window():
    
    def __init__(self, parent, category, wardrobe):
        self.window = parent
        self.wardrobe = wardrobe
        self.image_path=None
        self.category = category
        self.build()
        
    def build(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        set_backgrond(self.window, "images/background/strips_bg.jpg", 800, 800)
        # title
        Label(self.window, text=f"Add {self.category}", bg="white", 
              font=("Arial", 16, "bold")).pack(pady=20)

        # name field
        Label(self.window, text="Name:", bg="white").pack(anchor="w", padx=40)
        self.name_entry = Entry(self.window, width=40)
        self.name_entry.pack(padx=40, pady=5)
        
        # color field
        Label(self.window, text="Color:", bg="white").pack(anchor="w", padx=40)
        self.color_entry = Entry(self.window, width=40)
        self.color_entry.pack(padx=40, pady=5)
        
        # category dropdown
        Label(self.window, text="Category:", bg="white").pack(anchor="w", padx=40)
        self.category_var = StringVar(value=self.category)
        OptionMenu(self.window, self.category_var, 
                   "top", "bottom", "shoes", "dress", 
                   "accessory", "bag", "other").pack(padx=40, pady=5, anchor="w")
        
        # occasion dropdown
        Label(self.window, text="Occasion:", bg="white").pack(anchor="w", padx=40)
        self.occasion_var = StringVar(value="select option")
        OptionMenu(self.window, self.occasion_var,
                   "casual", "formal", "sport").pack(padx=40, pady=5, anchor="w")
        
        # image upload
        Label(self.window, text="Photo:", bg="white").pack(anchor="w", padx=40)
        Button(self.window, text="Upload photo", 
               command=self.upload_image).pack(padx=40, pady=5, anchor="w")
        
        # image preview
        self.image_label = Label(self.window, bg="white", text="no image selected")
        self.image_label.pack(pady=5)

        # save and cancel buttons
        Button(self.window, text="Save", bg="green", fg="white", 
               width=15, command=self.save_item).pack(pady=10)
        Button(self.window, text="Cancel", bg="red", fg="white", 
               width=15, command= lambda: [self.clear_frame(), self.show_home()]).pack()
        
    def clear_frame(self):
        for widget in self.window.winfo_children():
            widget.destroy()
            
    def upload_image(self):
         
        # opens the file browser 
        file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        
        # if the image exists
        if file_path:
            self.image_path = file_path
            # we open and resize the image for display
            image = Image.open(file_path)
            image = image.resize((150, 150))
            # converting immage for tkinter
            photo = ImageTk.PhotoImage(image)
            #displaying for preview
            self.image_label.config(image = photo, text = "")
            self.image_label.image = photo
        
    def save_item(self):
        
        name = self.name_entry.get()
        color = self.color_entry.get()
        category = self.category_var.get()
        occasion = self.occasion_var.get()
        
        if not name or not color or not occasion or not self.image_path:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        #create the clothing item and save it to csv
        item = ClothingItem(name, category, color, occasion, self.image_path)
        self.wardrobe.add_item(item)
        save_items(self.wardrobe.items)
        
        messagebox.showinfo("Success", f"{name} added successfully!")
        self.clear_frame()
        self.show_home()
        
    def show_home(self):
        set_backgrond(self.window, "images/background/clothes-bkg.jpg", 800, 800)
        
# this is the class for the wardrobe
class view_wardrobe_window:
    
    def __init__(self, parent, category = None, wardrobe=None):
        self.window = parent
        self.category = category
        self.wardrobe = wardrobe
        self.build()
        
    def build(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        #set_backgrond(self.window, "images/background/strips_bg.jpg", 800, 800)
        inner_frame = make_scrollable_frame(self.window)

        # filter by category or show all
        if self.category:
            items_to_show = self.wardrobe.filter_by_category(self.category)
        else:
            items_to_show = self.wardrobe.items

        # show message if no items
        if not items_to_show:
            Label(inner_frame, text="No items found!", 
                bg="pink", font=("Arial", 14)).pack(pady=20)
            return

        # show real items
        for item in items_to_show:
            # Main container card - increased height to 250-300 for better vertical look
            card = Frame(inner_frame, bg="white", height=600, width=400)
            card.pack_propagate(False)
            card.pack(pady=15, padx=20)

            # --- TOP SECTION (75% - Image) ---
            top_area = Frame(card, bg="white")
            top_area.place(relx=0, rely=0, relwidth=1, relheight=0.75)

            try:
                # Use a larger resize to fill the 75% area effectively
                image = Image.open(item.image_path)
                image = image.resize((300, 300)) 
                photo = ImageTk.PhotoImage(image)
                image_label = Label(top_area, image=photo, bg="white")
                image_label.image = photo 
                image_label.pack(expand=True, fill="both")
            except:
                Label(top_area, text="No Image", bg="#f0f0f0").pack(expand=True, fill="both")

            # --- BOTTOM SECTION (25% - Info & Buttons) ---
            bottom_area = Frame(card, bg="white", bd=1, relief="flat")
            bottom_area.place(relx=0, rely=0.75, relwidth=1, relheight=0.25)

            # Item name (Centered)
            Label(bottom_area, text=item.name, bg="white",
                  font=("Arial", 11, "bold")).pack(pady=(5, 0))

            # Details (Color • Occasion)
            details_text = f"{item.color} • {item.occasion}"
            Label(bottom_area, text=details_text, bg="white",
                  font=("Arial", 9), fg="gray").pack()

            # Buttons Container
            btn_frame = Frame(bottom_area, bg="white")
            btn_frame.pack(side="bottom", fill="x", pady=5)

            # Favourite Button (Left)
            Button(btn_frame, text="Favourite", bg="pink", font=("Arial", 8),
                   command=lambda i=item: self.toggle_favourite(i)).pack(side="left", padx=10)

            # Delete Button (Right)
            Button(btn_frame, text="Delete", bg="#ff4d4d", fg="white", font=("Arial", 8),
                   command=lambda i=item: self.delete_item(i)).pack(side="right", padx=10)
    
    def delete_item(self, item):
        confirm = messagebox.askyesno("Delete", f"Delete '{item.name}'?")
        if confirm:
            self.wardrobe.remove_item(item.name)
            save_items(self.wardrobe.items)
            for widget in self.window.winfo_children():
                widget.destroy()
            self.build()

    def toggle_favourite(self, item):
        messagebox.showinfo("Favourite", f"'{item.name}' added to favourites!")
            
# this is the class for the Outfit manager app  
class Outfit_manager:
    
    def __init__(self, window, wardrobe):
        self.window = window
        self.wardrobe = wardrobe
        self.build_menu()
        
    def build_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.title("Outfit manager")
        self.window.config(bg = "pink")
        self.window.geometry("800x800")
        set_backgrond(self.window, "images/background/clothes-bkg.jpg", 800, 800)
        
        # the frame that will change depending on the button presses
        self.content_frame = Frame(self.window, bg = "pink")
        self.content_frame.pack(fill=BOTH, expand=True)
        
        self.show_home()
        # creating the menu
        menubar = Menu(self.window)
        
        # adding the main menu
        main_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label = "Main menu", menu = main_menu)
        main_menu.add_command(label = "Home", command = self.show_home)
        main_menu.add_command(label = "Settings", command = lambda: [self.clear_content(), settings_window(self.content_frame)])
        main_menu.add_separator()
        main_menu.add_command(label = "Exit", command = self.window.destroy)
        
        # adding the 'add item' menu
        add_item = Menu(menubar, tearoff=0)
        menubar.add_cascade(label = "Add item", menu = add_item)
        add_item.add_command(label = "Add top", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "top", self.wardrobe)])
        add_item.add_command(label = "Add bottom", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "bottom", self.wardrobe)])
        add_item.add_command(label = "Add shoes", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "shoes", self.wardrobe)])
        add_item.add_command(label = "Add dresses", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "dress", self.wardrobe)])
        add_item.add_separator()
        add_item.add_command(label = "Add accessory", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "accessory", self.wardrobe)])
        add_item.add_command(label = "Add bag", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "bag", self.wardrobe)])
        add_item.add_command(label = "Add another item", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "item", self.wardrobe)])
        
        # adding the 'View wardrobe' menu
        view_wardrobe = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "View wardrobe", menu = view_wardrobe)
        view_wardrobe.add_command(label = "View all", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, None, self.wardrobe)])
        view_wardrobe.add_separator()
        view_wardrobe.add_command(label = "View tops", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "top", self.wardrobe)])
        view_wardrobe.add_command(label = "View bottoms", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "bottom", self.wardrobe)])
        view_wardrobe.add_command(label = "View dresses", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "dress", self.wardrobe)])
        view_wardrobe.add_command(label = "View shoes", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "shoes", self.wardrobe)])
        view_wardrobe.add_separator()
        view_wardrobe.add_command(label = "View accessory", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "accessory", self.wardrobe)])
        view_wardrobe.add_command(label = "View bags", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "bag", self.wardrobe)])
        view_wardrobe.add_command(label = "View others", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "other", self.wardrobe)])
        
        # adding the 'Create outfit' menu
        create_outfit = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "Create outfit", menu = create_outfit)
        create_outfit.add_command(label = "Randomize", command=lambda: [self.clear_content(), create_outfit_window(self.content_frame, self.wardrobe, self.show_home)])
        create_outfit.add_command(label = "Create from scratch", command=lambda: [self.clear_content(), create_outfit_window(self.content_frame, self.wardrobe, self.show_home)])
        
        # adding the 'View outfits' menu
        view_outfits = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "View outfits", menu = view_outfits)
        view_outfits.add_command(label = "View all outfits", command = lambda: [self.clear_content(), View_outfits_window(self.content_frame, self.wardrobe)])
        
        # adding the 'About us' menu
        about_us = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "About us", menu = about_us)
        about_us.add_command(label = "Smărăndoiu Elena", command = about_elena)
        about_us.add_command(label = "Lazăr Bianca", command = about_bianca)
        
        # this adds the menu
        self.window.config(menu = menubar)
        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def show_home(self):
        self.clear_content()
        set_backgrond(self.content_frame, "images/background/clothes-bkg.jpg", 800, 800)
