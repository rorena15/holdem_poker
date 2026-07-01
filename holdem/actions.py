import random

from .cards import cards_str
from .evaluator import best_hand


def bot_decision(player, community, need, pot, min_raise):
    cards = player.hole + community
    if len(cards) >= 5:
        strength = best_hand(cards)[0] / 8
    else:
        r1, r2 = sorted((c[0] for c in player.hole), reverse=True)
        pair_bonus = 0.35 if r1 == r2 else 0
        strength = min(1.0, (r1 + r2) / 28 + pair_bonus)
    need = min(need, player.chips)
    bluff = random.random() < 0.08

    if need == 0:
        if strength > 0.55 and random.random() < 0.4 and player.chips > min_raise:
            return ('raise', min(player.chips, min_raise + int(pot * 0.5)))
        return ('call', 0)
    if strength < 0.2 and not bluff:
        return ('fold', 0)
    if strength > 0.6 and random.random() < 0.4 and player.chips > need:
        return ('raise', min(player.chips, need + min_raise + int(pot * 0.4)))
    return ('call', need)


def human_action(p, community, need, pot):
    print(f"\n커뮤니티: {cards_str(community) if community else '(없음)'}  |  팟: {pot}")
    print(f"내 카드: {cards_str(p.hole)}  |  보유칩: {p.chips}  |  콜금액: {need}")
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
