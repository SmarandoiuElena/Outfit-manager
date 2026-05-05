class ClothingItem:
    def __init__(self, name, category, color, occasion, image_path):
        self.name = name
        self.category = category
        self.color = color
        self.occasion = occasion
        self.image_path = image_path

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "color": self.color,
            "occasion": self.occasion,
            "image_path": self.image_path
        }

    def __str__(self):
        return f"{self.name} ({self.category}, {self.color}, {self.occasion})"


class Outfit:
    def __init__(self, name, top=None, bottom=None, shoes=None, accessory=None):
        self.name = name
        self.top = top
        self.bottom = bottom
        self.shoes = shoes
        self.accessory = accessory

    def to_dict(self):
        return {
            "name": self.name,
            "top": self.top.name if self.top else "",
            "bottom": self.bottom.name if self.bottom else "",
            "shoes": self.shoes.name if self.shoes else "",
            "accessory": self.accessory.name if self.accessory else ""
        }

    def __str__(self):
        return f"Outfit: {self.name}"


class Wardrobe:
    def __init__(self):
        self.items = []
        self.outfits = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, name):
        self.items = [item for item in self.items if item.name != name]

    def get_item_by_name(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None

    def filter_by_category(self, category):
        return [item for item in self.items if item.category == category]

    def filter_by_occasion(self, occasion):
        return [item for item in self.items if item.occasion == occasion]

    def add_outfit(self, outfit):
        self.outfits.append(outfit)

    def remove_outfit(self, name):
        self.outfits = [outfit for outfit in self.outfits if outfit.name != name]