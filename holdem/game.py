import random

from .betting import betting_round, next_active
from .cards import make_deck
from .display import render_row
from .evaluator import HAND_NAMES, best_hand
from .player import post_blind


def build_side_pots(players):
    levels = sorted(set(p.total_bet for p in players if p.total_bet > 0))
    pots = []
    prev = 0
    for level in levels:
        layer = level - prev
        contributors = [p for p in players if p.total_bet >= level]
        eligible = [p for p in contributors if not p.folded]
        if not eligible:
            eligible = [p for p in players if not p.folded]
        pots.append((layer * len(contributors), eligible))
        prev = level
    return pots


def showdown(players, community, dealer_idx):
    total_pot = sum(p.total_bet for p in players)
    active = [p for p in players if not p.folded]
    if len(active) == 1:
        active[0].chips += total_pot
        print(f"\n{active[0].name} 승리! (모두 폴드) +{total_pot}")
        return {'reached_showdown': False, 'scores': {}, 'winners': [active[0]]}

    print(f"\n=== 쇼다운 ===\n{render_row(community)}\n")
    scores = {}
    for p in active:
        scores[p] = best_hand(p.hole + community)
        print(f"{p.name} ({HAND_NAMES[scores[p][0]]})")
        print(render_row(p.hole))

    n = len(players)
    seat_order = [(dealer_idx + 1 + i) % n for i in range(n)]

    all_winners = []
    pots = build_side_pots(players)
    for i, (amount, eligible) in enumerate(pots):
        if amount == 0:
            continue
        best_score = max(scores[p] for p in eligible)
        winners = [p for p in eligible if scores[p] == best_score]
        winners.sort(key=lambda w: seat_order.index(players.index(w)))
        all_winners.extend(w for w in winners if w not in all_winners)
        share, remainder = divmod(amount, len(winners))
        for j, w in enumerate(winners):
            w.chips += share + (remainder if j == 0 else 0)
        label = '메인팟' if i == 0 else f'사이드팟{i}'
        print(f"{label} {amount}: {', '.join(w.name for w in winners)} 승리 (+{share}{' +잔돈' if remainder else ''})")

    return {'reached_showdown': True, 'scores': scores, 'winners': all_winners}


def play_hand(players, dealer_idx, small_blind, big_blind):
    human = next((p for p in players if p.is_human), None)

    for p in players:
        p.hole, p.bet, p.total_bet, p.folded, p.all_in = [], 0, 0, False, False
    deck = make_deck()
    random.shuffle(deck)

    sb_idx = next_active(players, dealer_idx)
    bb_idx = next_active(players, sb_idx)
    pot = post_blind(players[sb_idx], small_blind) + post_blind(players[bb_idx], big_blind)
    print(f"\n===== 새 핸드 (딜러: {players[dealer_idx].name}) =====")
    print(f"{players[sb_idx].name} 스몰블라인드 {small_blind} / {players[bb_idx].name} 빅블라인드 {big_blind}")

    for p in players:
        p.hole = [deck.pop(), deck.pop()]
    for p in players:
        if p.is_human:
            print(f"{p.name} 카드:\n{render_row(p.hole)}")

    community = []
    start = next_active(players, bb_idx)
    pot = betting_round(players, community, pot, start, big_blind)

    for count in (3, 1, 1):
        if sum(not p.folded for p in players) <= 1:
            break
        deck.pop()
        community += [deck.pop() for _ in range(count)]
        print(f"\n커뮤니티 카드:\n{render_row(community)}")
        for p in players:
            p.bet = 0
        start = next_active(players, dealer_idx)
        pot = betting_round(players, community, pot, start, big_blind)

    result = showdown(players, community, dealer_idx)

    if human is None:
        return None
    return {
        'human_won': human in result['winners'],
        'reached_showdown': result['reached_showdown'],
        'human_folded': human.folded,
        'human_hand_category': result['scores'][human][0] if human in result['scores'] else None,
        'human_busted': human.chips == 0,
    }
