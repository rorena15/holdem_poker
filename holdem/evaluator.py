from itertools import combinations

HAND_NAMES = {
    8: '스트레이트 플러시', 7: '포카드', 6: '풀하우스', 5: '플러시',
    4: '스트레이트', 3: '트리플', 2: '투페어', 1: '원페어', 0: '하이카드',
}


def hand_rank(cards5):
    ranks = sorted((c[0] for c in cards5), reverse=True)
    suits = [c[1] for c in cards5]
    is_flush = len(set(suits)) == 1
    uniq = sorted(set(ranks), reverse=True)
    is_straight, straight_high = False, None
    if len(uniq) == 5:
        if uniq[0] - uniq[4] == 4:
            is_straight, straight_high = True, uniq[0]
        elif uniq == [14, 5, 4, 3, 2]:
            is_straight, straight_high = True, 5

    counts = {}
    for r in ranks:
        counts[r] = counts.get(r, 0) + 1
    groups = sorted(counts.items(), key=lambda x: (-x[1], -x[0]))
    g_ranks = [g[0] for g in groups]
    g_counts = [g[1] for g in groups]

    if is_straight and is_flush:
        return (8, straight_high)
    if g_counts[0] == 4:
        return (7, g_ranks[0], g_ranks[1])
    if g_counts[0] == 3 and g_counts[1] == 2:
        return (6, g_ranks[0], g_ranks[1])
    if is_flush:
        return (5, *ranks)
    if is_straight:
        return (4, straight_high)
    if g_counts[0] == 3:
        return (3, g_ranks[0], *g_ranks[1:])
    if g_counts[0] == 2 and g_counts[1] == 2:
        hi, lo = max(g_ranks[0], g_ranks[1]), min(g_ranks[0], g_ranks[1])
        return (2, hi, lo, g_ranks[2])
    if g_counts[0] == 2:
        return (1, g_ranks[0], *g_ranks[1:])
    return (0, *ranks)


def best_hand(cards7):
    return max(hand_rank(list(c)) for c in combinations(cards7, 5))
