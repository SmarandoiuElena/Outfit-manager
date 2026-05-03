from gui import Outfit_manager
from music import start_music
from tkinter import Tk

window = Tk()
wardrobe = []
start_music("music/Music1.mpeg")
app = Outfit_manager(window, wardrobe)
window.mainloop()