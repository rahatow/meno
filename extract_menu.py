import argparse
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
import pytesseract


@dataclass
class MenuItem:
    name: str
    price: float
    description: str = ""

def extract_text(image_path: Path, lang: str = "rus") -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image, lang=lang)

def parse_menu(text: str):
    items = []
    for line in text.splitlines():
        match = re.search(r"(.+?)\s*(\d+[.,]?\d*)", line)
        if match:
            name = match.group(1).strip()
            price_str = match.group(2).replace(",", ".")
            try:
                price = float(price_str)
            except ValueError:
                continue
            items.append(MenuItem(name=name, price=price))
    return items

def store_menu(restaurant: str, items, db_path: Path = Path("menu.db")):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS menu (restaurant TEXT, dish TEXT, price REAL, description TEXT)"
    )
    for item in items:
        cur.execute(
            "INSERT INTO menu VALUES (?,?,?,?)",
            (restaurant, item.name, item.price, item.description),
        )
    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Extract menu items from an image")
    parser.add_argument("image", type=Path, help="Path to menu photo")
    parser.add_argument("restaurant", help="Restaurant name")
    parser.add_argument("--lang", default="rus", help="OCR language")
    args = parser.parse_args()

    text = extract_text(args.image, lang=args.lang)
    items = parse_menu(text)
    store_menu(args.restaurant, items)

    for item in items:
        print(f"{item.name} - {item.price}")


if __name__ == "__main__":
    main()
