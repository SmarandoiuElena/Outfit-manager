from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from  PIL import Image, ImageTk
import os.path

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
    set_backgrond(parent, "images/background/strips_bg.jpg", 1000, 1000)
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

# this is the class for the view outfits window
class View_outfits_window:
    
    def __init__(self, parent):
        self.window = parent 
        self.build()
        
    def build(self):
        set_backgrond(self.window, "images/background/strips_bg.jpg", 1000, 1000)        
        inner_frame = make_scrollable_frame(self.window)
        
        for i in range(10):
            card = Frame(inner_frame, bg = "white", height=700, width=600)
            card.pack_propagate(False)
            card.pack(pady=10)
            
            Button(card, text="Delete", bg="red", fg="black", width=10).place(relx=1.0, rely=1.0, anchor="se")
            Button(card, text="Add to favourite", bg="pink", fg="black", width=10).place(relx=0.0, rely=1.0, anchor="sw")
            Label(card, text=f"Outfit {i+1}", bg="white", font=("Arial", 12)).pack(anchor="w")
           
     
# this is the class for adding an item
class add_item_window():
    
    def __init__(self, parent, category):
        self.window = parent
        self.image_path=None
        self.category = category
        self.build()
        
    def build(self):
        set_backgrond(self.window, "images/background/strips_bg.jpg", 1000, 1000)
        # title
        Label(self.window, text=f"Add {self.category}", bg="pink", 
              font=("Arial", 16, "bold")).pack(pady=20)

        # name field
        Label(self.window, text="Name:", bg="pink").pack(anchor="w", padx=40)
        self.name_entry = Entry(self.window, width=40)
        self.name_entry.pack(padx=40, pady=5)
        
        # color field
        Label(self.window, text="Color:", bg="pink").pack(anchor="w", padx=40)
        self.color_entry = Entry(self.window, width=40)
        self.color_entry.pack(padx=40, pady=5)
        
        # category dropdown
        Label(self.window, text="Category:", bg="pink").pack(anchor="w", padx=40)
        self.category_var = StringVar(value=self.category)
        OptionMenu(self.window, self.category_var, 
                   "top", "bottom", "shoes", "dress", 
                   "accessory", "bag", "other").pack(padx=40, pady=5, anchor="w")
        
        # occasion dropdown
        Label(self.window, text="Occasion:", bg="pink").pack(anchor="w", padx=40)
        self.occasion_var = StringVar(value="select option")
        OptionMenu(self.window, self.occasion_var,
                   "casual", "formal", "sport").pack(padx=40, pady=5, anchor="w")
        
        # image upload
        Label(self.window, text="Photo:", bg="pink").pack(anchor="w", padx=40)
        Button(self.window, text="Upload photo", 
               command=self.upload_image).pack(padx=40, pady=5, anchor="w")
        
        # image preview
        self.image_label = Label(self.window, bg="pink", text="no image selected")
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
        
        # to do: create the clothing item and save it to csv
        print(f"Saving: {name}, {color}, {category}, {occasion}, {self.image_path}")
        
        messagebox.showinfo("Success", f"{name} added successfully!")
        self.clear_frame()
        self.show_home()
        
    def show_home(self):
        self.clear_frame()
        set_backgrond(self.window, "images/background/clothes-bkg.jpg", 1000, 1000)
        
# this is the class for the wardrobe
class view_wardrobe_window:
    
    def __init__(self, parent, category = None):
        self.window = parent
        self.category = category
        self.build()
        
    def build(self):
        set_backgrond(self.window, "images/background/strips_bg.jpg", 1000, 1000)
        inner_frame = make_scrollable_frame(self.window)
     
    #--------------will uncomemt after the csv files are ready-----------------
       # if self.category:
            
        #    items_to_show = []   
         #   for item in self.wardrobe.items:
          #      if item.category == self.category:
           #         items_to_show.append(item)
                
        #else:
         #   items_to_show = self.wardrobe.items
            
        #for item in items_to_show:
            
         #   card = Frame(inner_frame, bg="white", height=150)
          #  card.pack_propagate(False)
           # card.pack(pady=8, padx=20, fill=X)
            
        # test cards
         
# TO DO -------------------------- FILTER BUTTON
        for i in range(10):
            
            card = Frame(inner_frame, bg = "white", height=500, width=400)
            card.pack_propagate(False)
            card.pack(pady=8, padx=20)
            
            # image on the left
            image_label = Label(card, bg="white", text="no image")
            image_label.place(relx=0.0, rely=0.5, anchor="w")
            
            # item info in the middle
            Label(card, text=f"Item {i+1}", bg="white", 
                  font=("Arial", 12, "bold")).place(relx=0.3, rely=0.3, anchor="w")
            Label(card, text="Color: blue", bg="white",
                  font=("Arial", 10)).place(relx=0.3, rely=0.6, anchor="w")
            
            # delete button bottom right
            Button(card, text="Delete", bg="red", fg="black",
                   width=10).place(relx=1.0, rely=1.0, anchor="se")
            
            # favourite button bottom left
            Button(card, text="Favourite", bg="pink", fg="black",
                   width=10).place(relx=0.0, rely=1.0, anchor="sw")
            
# this is the class for the Outfit manager app  
class Outfit_manager:
    
    def __init__(self, window, wardrobe):
        self.window = window
        self.wardrobe = wardrobe
        self.build_menu()
        
    def build_menu(self):
        self.window.title("Outfit manager")
        self.window.config(bg = "pink")
        self.window.geometry("1000x1000")
        set_backgrond(self.window, "images/background/clothes-bkg.jpg", 1000, 1000)
        
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
        main_menu.add_command(label = "Settings", command = None)
        main_menu.add_separator()
        main_menu.add_command(label = "Exit", command = self.window.destroy)
        
        # adding the 'add item' menu
        add_item = Menu(menubar, tearoff=0)
        menubar.add_cascade(label = "Add item", menu = add_item)
        add_item.add_command(label = "Add top", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "top")])
        add_item.add_command(label = "Add bottom", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "bottom")])
        add_item.add_command(label = "Add shoes", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "shoes")])
        add_item.add_command(label = "Add dresses", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "dress")])
        add_item.add_separator()
        add_item.add_command(label = "Add accessory", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "accessory")])
        add_item.add_command(label = "Add bag", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "bag")])
        add_item.add_command(label = "Add another item", command = lambda: [self.clear_content(), add_item_window(self.content_frame, "item")])
        
        # adding the 'View wardrobe' menu
        view_wardrobe = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "View wardrobe", menu = view_wardrobe)
        view_wardrobe.add_command(label = "View all", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, None)])
        view_wardrobe.add_separator()
        view_wardrobe.add_command(label = "View tops", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "top")])
        view_wardrobe.add_command(label = "View bottoms", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "bottom")])
        view_wardrobe.add_command(label = "View dresses", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "dress")])
        view_wardrobe.add_command(label = "View shoes", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "shoes")])
        view_wardrobe.add_separator()
        view_wardrobe.add_command(label = "View accessory", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "accessory")])
        view_wardrobe.add_command(label = "View bags", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "bag")])
        view_wardrobe.add_command(label = "View others", command = lambda: [self.clear_content(), view_wardrobe_window(self.content_frame, "item")])
        
        # adding the 'Create outfit' menu
        create_outfit = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "Create outfit", menu = create_outfit)
        create_outfit.add_command(label = "Randomize", command = None)
        create_outfit.add_command(label = "Create from scratch", command = None)
        
        # adding the 'View outfits' menu
        view_outfits = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "View outfits", menu = view_outfits)
        view_outfits.add_command(label = "View all outfits", command = lambda: [self.clear_content(), View_outfits_window(self.content_frame)])
        
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
        set_backgrond(self.content_frame, "images/background/clothes-bkg.jpg", 1000, 1000)
        
window = Tk()
wardrobe = []
app = Outfit_manager(window, wardrobe)
window.mainloop()