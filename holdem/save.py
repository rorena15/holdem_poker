import json
import os

SAVE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'save.json')

DEFAULT_STATE = {
    'chips': 1000,
    'coins': 0,
    'quest': None,
}


def load_state():
    if not os.path.exists(SAVE_PATH):
        return dict(DEFAULT_STATE)
    try:
        with open(SAVE_PATH, encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_STATE)
    state = dict(DEFAULT_STATE)
    state.update(data)
    return state


def save_state(state):
    with open(SAVE_PATH, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
