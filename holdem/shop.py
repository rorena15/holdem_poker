from .quests import REBUY_CHIPS, REBUY_COST


def open_shop(coins):
    gained = 0
    while True:
        print(f"\n=== 상점 === 보유 코인: {coins}")
        print(f"1) 칩 {REBUY_CHIPS}개 구매 ({REBUY_COST}코인)")
        print("b) 나가기")
        cmd = input("선택: ").strip().lower()
        if cmd == '1':
            if coins < REBUY_COST:
                print("코인이 부족합니다.")
                continue
            coins -= REBUY_COST
            gained += REBUY_CHIPS
            print(f"칩 {REBUY_CHIPS}개를 구매했습니다. (이번 방문 누적 {gained})")
            continue
        if cmd == 'b':
            return coins, gained
        print("잘못된 입력입니다.")


def offer_rebuy(coins):
    if coins < REBUY_COST:
        print(f"\n파산했습니다! 코인이 부족해 리바이인할 수 없습니다. (보유 코인: {coins}, 필요 코인: {REBUY_COST})")
        return coins, 0
    print(f"\n파산했습니다! 코인 {REBUY_COST}개로 칩 {REBUY_CHIPS}개를 리바이인 하시겠습니까? (보유 코인: {coins})")
    cmd = input("리바이인 하시겠습니까? (y/n): ").strip().lower()
    if cmd == 'y':
        return coins - REBUY_COST, REBUY_CHIPS
    return coins, 0
