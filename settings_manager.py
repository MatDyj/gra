import json
import os

DEFAULTS = {
    "key_left" : "left",
    "key_right": "right",
    "key_up"   : "up",
    "key_down" : "down",
    "key_fire" : "space",
    "difficulty": "medium",
    "sound": True
}
SETTINGS_FILE = "settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULTS)
        return DEFAULTS.copy()
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # uzupełnij brakujące pola domyślnymi
            for k, v in DEFAULTS.items():
                data.setdefault(k, v)
            return data
        except json.JSONDecodeError:
            return DEFAULTS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
