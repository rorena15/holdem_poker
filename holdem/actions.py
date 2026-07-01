import random

from .display import render_table
from .evaluator import best_hand

PERSONALITIES = [
    {'name': '타이트', 'tightness': 0.08, 'aggression': -0.10, 'bluff': 0.03},
    {'name': '루즈', 'tightness': -0.06, 'aggression': 0.0, 'bluff': 0.07},
    {'name': '어그로', 'tightness': -0.02, 'aggression': 0.15, 'bluff': 0.12},
    {'name': '패시브', 'tightness': 0.05, 'aggression': -0.15, 'bluff': 0.02},
]

DEFAULT_STYLE = {'tightness': 0, 'aggression': 0, 'bluff': 0.06}


def preflop_strength(hole):
    r1, r2 = sorted((c[0] for c in hole), reverse=True)
    if r1 == r2:
        return 0.55 + r1 / 28
    suited = hole[0][1] == hole[1][1]
    gap = r1 - r2
    strength = (r1 + r2) / 28 * 0.55
    if suited:
        strength += 0.07
    if gap == 1:
        strength += 0.05
    return min(1.0, strength)


def bot_decision(player, community, need, pot, min_raise):
    style = player.style or DEFAULT_STYLE
    if community:
        strength = best_hand(player.hole + community)[0] / 8
        fold_threshold = 0.2 + style['tightness']
    else:
        strength = preflop_strength(player.hole)
        fold_threshold = 0.32 + style['tightness']

    need = min(need, player.chips)
    if need > 0:
        pressure = min(0.2, (need / max(pot, 1)) * 0.15)
        fold_threshold += pressure

    bluff = random.random() < style['bluff']
    raise_chance = max(0.05, 0.35 + style['aggression'])

    if need == 0:
        if strength > 0.6 and random.random() < raise_chance and player.chips > min_raise:
            return ('raise', min(player.chips, min_raise + int(pot * 0.5)))
        return ('call', 0)
    if strength < fold_threshold and not bluff:
        return ('fold', 0)
    if strength > 0.65 and random.random() < raise_chance and player.chips > need:
        return ('raise', min(player.chips, need + min_raise + int(pot * 0.4)))
    return ('call', need)


def human_action(p, players, community, need, pot):
    print('\n' + render_table(players, community, pot, p))
    print(f"콜금액: {need}")
    while True:
        cmd = input("행동 (f=폴드, c=콜/체크, r 금액=레이즈): ").strip().lower()
        if cmd == 'f':
            return ('fold', 0)
        if cmd == 'c':
            return ('call', need)
        if cmd.startswith('r'):
            parts = cmd.split()
            try:
                amt = int(parts[1]) if len(parts) > 1 else need + 20
            except ValueError:
                print("잘못된 입력입니다.")
                continue
            if amt <= need:
                print("레이즈 금액은 콜금액보다 커야 합니다.")
                continue
            return ('raise', amt)
        print("잘못된 입력입니다.")
