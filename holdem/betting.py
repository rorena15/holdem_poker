import random
import time

from .actions import bot_decision, human_action

THINK = True


def bot_think():
    if THINK:
        time.sleep(random.uniform(0.5, 1.5))


def next_active(players, idx):
    n = len(players)
    i = (idx + 1) % n
    while players[i].folded:
        i = (i + 1) % n
    return i


def betting_round(players, community, pot, start_idx, min_bet):
    n = len(players)
    order = [(start_idx + i) % n for i in range(n)]
    current_bet = max(p.bet for p in players)
    pending = [i for i in order if not players[i].folded and not players[i].all_in]

    while pending:
        i = pending.pop(0)
        p = players[i]
        active = [q for q in players if not q.folded]
        if len(active) <= 1:
            break
        need = current_bet - p.bet
        if p.is_human:
            action, amt = human_action(p, players, community, need, pot)
        else:
            print(f"{p.name} 생각 중...", end='', flush=True)
            bot_think()
            print('\r' + ' ' * 20 + '\r', end='')
            action, amt = bot_decision(p, community, need, pot, min_bet)

        if action == 'fold':
            p.folded = True
            if not p.is_human:
                print(f"{p.name}: 폴드")
        elif action == 'call':
            pay = min(need, p.chips)
            p.chips -= pay
            p.bet += pay
            p.total_bet += pay
            pot += pay
            if p.chips == 0:
                p.all_in = True
            if not p.is_human:
                print(f"{p.name}: {'체크' if pay == 0 else f'콜 {pay}'}")
        elif action == 'raise':
            pay = min(max(amt, need + min_bet), p.chips)
            p.chips -= pay
            p.bet += pay
            p.total_bet += pay
            pot += pay
            current_bet = max(current_bet, p.bet)
            if p.chips == 0:
                p.all_in = True
            if not p.is_human:
                print(f"{p.name}: 레이즈 {pay} (총 베팅 {p.bet})")
            pending = [j for j in order if j != i and not players[j].folded and not players[j].all_in]
    return pot
