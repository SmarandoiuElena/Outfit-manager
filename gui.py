from tkinter import *
from tkinter import messagebox
import os.path

def about_elena():
    messagebox.showinfo("About", "Smărăndoiu Elena\nOutfit Manager App 2026")
    
def about_bianca():
    messagebox.showinfo("About", "Lazăr Bianca\nOutfit Manager App 2026")

# making the scrollbar
# we put the frames inside the canvas and scroll the canvas 
def make_scrollable_frame(parent):
    # the frame that contains everything
    # holds the canvas and the scrollbar together
    outer_frame = Frame(parent, bg="pink")
    outer_frame.grid(row=0, column=0, sticky="nsew")

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
   
        self.window = Toplevel(parent) 
        self.window.title("View outfits")
        self.build()
        
    def build(self):
        self.window.config(bg = "pink")
        self.window.geometry("800x600")
        
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        
        inner_frame = make_scrollable_frame(self.window)
        
        for i in range(10):
            card = Frame(inner_frame, bg = "white", height=800, width=500)
            card.pack_propagate(False)
            card.pack(pady=10)
            
            Button(card, text="Delete", bg="red", fg="white", width=10).place(relx=1.0, rely=1.0, anchor="se")
            Label(card, text=f"Outfit {i+1}", bg="white", font=("Arial", 12)).pack(anchor="w")
           
     
# this is the class for the Outfit manager app  
class Outfit_manager:
    
    def __init__(self, window, wardrobe):
        self.window = window
        self.wardrobe = wardrobe
        self.build_menu()
        
    def build_menu(self):
        self.window.title("Outfit manager")
        self.window.config(bg = "pink")
        self.window.config(padx=300, pady=300)
        self.window.geometry("600x600")
   
        # creating the menu
        menubar = Menu(self.window)
        
        # adding the main menu
        main_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label = "Main menu", menu = main_menu)
        main_menu.add_command(label = "Home", command = None)
        main_menu.add_command(label = "Settings", command = None)
        main_menu.add_separator()
        main_menu.add_command(label = "Exit", command = self.window.destroy)
        
        # adding the 'add item' menu
        add_item = Menu(menubar, tearoff=0)
        menubar.add_cascade(label = "Add item", menu = add_item)
        add_item.add_command(label = "Add top", command = None)
        add_item.add_command(label = "Add bottom", command = None)
        add_item.add_command(label = "Add shoes", command = None)
        add_item.add_command(label = "Add dresses", command = None)
        add_item.add_separator()
        add_item.add_command(label = "Add accesories", command = None)
        add_item.add_command(label = "Add bag", command = None)
        add_item.add_command(label = "Add another item", command = None)
        
        # adding the 'View wardrobe' menu
        view_wardrobe = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "View wardrobe", menu = view_wardrobe)
        view_wardrobe.add_command(label = "View all", command = None)
        view_wardrobe.add_separator()
        view_wardrobe.add_command(label = "View tops", command = None)
        view_wardrobe.add_command(label = "View bottoms", command = None)
        view_wardrobe.add_command(label = "View dresses", command = None)
        view_wardrobe.add_command(label = "View shoes", command = None)
        view_wardrobe.add_separator()
        view_wardrobe.add_command(label = "View accesories", command = None)
        view_wardrobe.add_command(label = "View bags", command = None)
        view_wardrobe.add_command(label = "View others", command = None)
        
        # adding the 'Create outfit' menu
        create_outfit = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "Create outfit", menu = create_outfit)
        create_outfit.add_command(label = "Randomize", command = None)
        create_outfit.add_command(label = "Create from scratch", command = None)
        
        # adding the 'View outfits' menu
        view_outfits = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "View outfits", menu = view_outfits)
        view_outfits.add_command(label = "View all outfits", command = lambda: View_outfits_window(self.window))
        
        # adding the 'About us' menu
        about_us = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "About us", menu = about_us)
        about_us.add_command(label = "Smărăndoiu Elena", command = about_elena)
        about_us.add_command(label = "Lazăr Bianca", command = about_bianca)
        
        # this adds the menu
        self.window.config(menu = menubar)
        
window = Tk()
wardrobe = []
app = Outfit_manager(window, wardrobe)
window.mainloop()