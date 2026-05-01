from tkinter import *
import os.path


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
   
        label = Label(self.window, text="heio")
        label.grid(row=1, column=0)
        
window = Tk()
wardrobe = []
app = Outfit_manager(window, wardrobe)
window.mainloop()