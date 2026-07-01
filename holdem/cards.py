SUITS = ['S', 'H', 'D', 'C']
RANK_NAMES = {**{n: str(n) for n in range(2, 11)}, 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}


def make_deck():
    return [(r, s) for r in range(2, 15) for s in SUITS]


def card_str(c):
    r, s = c
    return f"{RANK_NAMES[r]}{s}"


def cards_str(cards):
    return ' '.join(card_str(c) for c in cards)
