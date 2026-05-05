from tkinter import Tk

from gui import Outfit_manager
from music import start_music
from models import Wardrobe
from csv_handler import load_items, load_outfits


window = Tk()

wardrobe = Wardrobe()
wardrobe.items = load_items()
wardrobe.outfits = load_outfits(wardrobe.items)

start_music("music/Music1.mpeg")

for item in load_items():
    wardrobe.add_item(item)

app = Outfit_manager(window, wardrobe)

window.mainloop()