import csv
import os

from models import ClothingItem, Outfit


def save_items(items, filename="items.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "category", "color", "occasion", "image_path"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for item in items:
            writer.writerow(item.to_dict())


def load_items(filename="items.csv"):
    items = []

    if not os.path.exists(filename):
        return items

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            item = ClothingItem(
                row["name"],
                row["category"],
                row["color"],
                row["occasion"],
                row["image_path"]
            )
            items.append(item)

    return items


def save_outfits(outfits, filename="outfits.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "top", "bottom", "shoes", "accessory"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for outfit in outfits:
            writer.writerow(outfit.to_dict())


def load_outfits(items, filename="outfits.csv"):
    outfits = []

    if not os.path.exists(filename):
        return outfits

    def find_item_by_name(name):
        for item in items:
            if item.name == name:
                return item
        return None

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            outfit = Outfit(
                name=row["name"],
                top=find_item_by_name(row["top"]),
                bottom=find_item_by_name(row["bottom"]),
                shoes=find_item_by_name(row["shoes"]),
                accessory=find_item_by_name(row["accessory"])
            )
            outfits.append(outfit)

    return outfits