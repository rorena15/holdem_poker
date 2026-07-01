from .cards import RANK_NAMES

WIDTH = 60


def render_card(card):
    if card is None:
        return ['.-----.', '|     |', '|     |', '|     |', "'-----'"]
    if card == 'back':
        return ['.-----.', '|# # #|', '| # # |', '|# # #|', "'-----'"]
    r, s = card
    name = RANK_NAMES[r]
    left = name.ljust(2)
    right = name.rjust(2)
    return [
        '.-----.',
        f'|{left}   |',
        f'|  {s}  |',
        f'|   {right}|',
        "'-----'",
    ]


def render_row(cards):
    if not cards:
        return ''
    arts = [render_card(c) for c in cards]
    return '\n'.join('  '.join(art[i] for art in arts) for i in range(5))


def center_block(text, width=WIDTH):
    lines = text.split('\n')
    maxw = max((len(l) for l in lines), default=0)
    pad = max((width - maxw) // 2, 0)
    return '\n'.join(' ' * pad + l for l in lines)


def player_tag(p):
    tag = f"{p.name}({p.chips})"
    if p.folded:
        tag += '[폴드]'
    elif p.all_in:
        tag += '[올인]'
    elif p.bet:
        tag += f'[{p.bet}]'
    return tag


def render_table(players, community, pot, viewer, quest=None, coins=None):
    others = [p for p in players if p is not viewer]
    backs = [None if p.folded else 'back' for p in others]

    lines = ['=' * WIDTH]
    if quest is not None:
        lines.append(f"코인: {coins}  |  퀘스트: {quest['desc']} ({quest['progress']}/{quest['target']}, 보상 {quest['reward']}코인)".center(WIDTH))
        lines.append('-' * WIDTH)
    lines.append(' '.join(player_tag(p) for p in others).center(WIDTH))
    lines.append(center_block(render_row(backs), WIDTH))
    lines.append('')
    lines.append('[ 커뮤니티 카드 ]'.center(WIDTH))
    board = community + [None] * (5 - len(community))
    lines.append(center_block(render_row(board), WIDTH))
    lines.append(f'팟: {pot}'.center(WIDTH))
    lines.append('-' * WIDTH)
    lines.append(f'[ 내 카드 ]  {viewer.name} ({viewer.chips}칩)'.center(WIDTH))
    lines.append(center_block(render_row(viewer.hole), WIDTH))
    lines.append('=' * WIDTH)
    return '\n'.join(lines)
