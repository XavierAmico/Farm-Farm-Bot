import json, os
from datetime import datetime, timezone

DATA_FILE = "pearls.json"

colors = {"Black", "Blue", "Cyan", "Green", "Magenta", "Red", "White", "Yellow"}

def get_today():
    utc_now = datetime.now(timezone.utc)
    return utc_now.strftime("%B %d, %Y")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: corrupted JSON file, starting fresh.")
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_today_pearls():
    data = load_data()
    today = get_today()
    return data.get(today, [])

def add(color: str, x: int, y: int):
    data = load_data()
    today = get_today()

    if today not in data:
        data[today] = []

    data[today].append({"color": color, "x": x, "y": y})

    save_data(data)

def remove(x: int, y: int):
    data = load_data()
    today = get_today()

    if today not in data:
        return False  # nothing to remove

    original_len = len(data[today])

    # Remove matching pearls
    data[today] = [
        pearl for pearl in data[today]
        if not (pearl["x"] == x and pearl["y"] == y)
    ]

    # Save only if something changed
    if len(data[today]) < original_len:
        save_data(data)
        return True  # removal successful

    return False  # nothing matched

def clear():
    today = get_today()
    data = load_data()
    data[today] = []

    save_data(data)

def is_duplicate( color: str, x: int, y:int):
    data = load_data()
    today = get_today()

    if today not in data:
        return False  # no pearls recorded for today yet

    for pearl in data[today]:
        if (pearl["color"].lower() == color.lower() and
                pearl["x"] == x and
                pearl["y"] == y):
            return True  # duplicate found
    return False