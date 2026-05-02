from tkinter import *
from tkinter import messagebox
import os.path

def about_elena():
    messagebox.showinfo("About", "Smărăndoiu Elena\nOutfit Manager App 2026")
    
def about_bianca():
    messagebox.showinfo("About", "Lazăr Bianca\nOutfit Manager App 2026")


# this is the class for the view outfits window
class View_outfits_window:
    
    def __init__(self, parent):
   
        self.window = Toplevel(parent) 
        self.window.title("View outfits")
        self.build()
        
    def build(self):
        self.window.config(bg = "pink")
        self.window.config(padx=300, pady=300)
        canvas = Canvas(self.window, height=200, width=200, bg = "white")
        canvas.grid(row=0, column=1)
        scrollbar = Scrollbar(self.window, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side = LEFT, fill=Y)
        
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
        canvas = Canvas(self.window, height=200, width=200, bg = "white")
        canvas.grid(row=0, column=1)
   
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