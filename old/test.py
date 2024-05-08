import pygame as pg
import random
from matplotlib import colors
import tkinter as tk
from tkinter import messagebox as msg
import ctypes
import time
import win32gui
import socket
import threading

BLACK = (0, 0, 0, 255) # 검은색
WHITE = (255, 255, 255, 255) # 흰색
BLUE = (0, 0, 255, 255) # 파란색
PURPLE = (128, 0, 128, 255) # 보라색
RED = (255, 0, 0, 255) # 빨간색
YELLOW = (255, 255, 0, 255) # 노란색
GREEN = (0, 128, 0, 255) # 초록색
GRAY = (200, 200, 200, 255) # 회색

square_size = 30  # 기본 사각형 크기 설정
window_size = (square_size * 40, square_size * 24) # 창 크기 설정
background_color = WHITE # 창 배경색 설정
wall_color = BLACK # 벽의 색상 설정

window_size = (square_size * 40, square_size * 24) # 창 크기 설정
background_color = WHITE # 창 배경색 설정
wall_color = BLACK # 벽의 색상 설정
wall_pos = pg.Rect(window_size[0] / 2 - square_size * 19, window_size [1] / 2 - square_size * 10, 20 * square_size, 20 * square_size) # 벽의 위치 설정

grid_color = GRAY  # 그리드 색상
thickness = square_size // 10 # 선 두께 설정
window = pg.display.set_mode(window_size) # `window_size` 크기의 창 생성
pg.display.set_caption("CLUE - board game") # 창 제목 설정
window.fill(background_color) # 창 배경색으로 채우기

suspects = { # 용의자카드
        "피콕": BLUE,
        "플럼": PURPLE,
        "스칼렛": RED,
        "머스타드": YELLOW,
        "그린": GREEN,
        "화이트": WHITE
}
weapons = ["파이프", "밧줄", "단검", "렌치", "권총", "촛대"]  # 도구카드
locs = ["침실", "욕실", "서제", "부엌", "식당", "거실", "마당", "차고", "게임룸"]  # 장소카드
room_names = locs.copy() # 방 이름 설정
room_names.insert(1, "") # 이름 빈 방
room_names.insert(8, "") # 이름 빈 방
room_names.insert(9, "") # 이름 빈 방
room_names.insert(12, "시작점") # 시작점 방
bonus_cards = { # 보너스카드
        "차례를 한 번 더 진행합니다." : "지금 사용하거나 필요할 때 사용합니다.",
        "원하는 장소로 이동합니다." : "지금 사용합니다.",
        "카드 엿보기" : "누군가 다른 사람에게 추리 카드를 보여줄 때 그 카드를 볼 수 있습니다. 필요할 때 사용합니다.",
        "나온 주사위에 6을 더할 수 있습니다." : "지금 사용하거나 필요할 때 사용합니다.",
        "다른 사람의 카드 한 장을 공개합니다." : "한 사람을 정해 이 카드를 보여주면, 그 사람은 자기 카드 중 한 장을 모두에게 보여주어야 합니다. 지금 사용합니다.",
        "한 번 더 추리합니다." : "자기 말이나 다른 사람의 말 또는 토큰을 이용하지 않고 원하는 장소, 사람, 도구를 정해 추리할 수 있습니다. 지금 사용합니다."
}
bonus_cards_list = [card for card in bonus_cards for _ in range(2)] # 각 카드를 원하는 수만큼 복제합니다.
bonus_cards_list.extend(["원하는 장소로 이동합니다."]) # 보너스카드 목록에 추가
room_size = [ # 방의 크기 설정
    (6, 6),  # Room 1
    (1, 2),  # Room 1.1
    (4, 4),  # Room 2s
    (4, 5),  # Room 3
    (6, 6),  # Room 4
    (7, 5),  # Room 5
    (6, 6),  # Room 6
    (4, 3),  # Room 7(outside)
    (2, 4),  # Room 7.1(outside)
    (2, 4),  # Room 7.2(outside)
    (5, 6),  # Room 8
    (5, 6),  # Room 9
    (4, 3),  # Room start
]
room_pos = [ # 방의 위치 설정
    (0, 2),  # Room 1
    (6, 6),  # Room 1.1
    (6, 0),  # Room 2
    (10, 1),  # Room 3
    (14, 2),  # Room 4
    (13, 8),  # Room 5
    (14, 13),  # Room 6
    (8, 17),  # Room 7(outside)
    (6, 16),  # Room 7.1(outside)
    (12, 16),  # Room 7.2(outside)
    (1, 14),  # Room 8
    (1, 8),  # Room 9
    (8, 10),  # Room start
]
rooms = [(wall_pos[0] + x * square_size, wall_pos[1] + y * square_size, w * square_size, h * square_size) for (x, y), (w, h) in zip(room_pos, room_size)] # 방의 위치와 크기를 결합
room_walls_pos = [ # 방 벽 위치 설정
        ((0, 2), (6, 2)),
        ((6, 0), (6, 3)),
        ((6, 4), (6, 5)),
        ((6, 6), (7, 6)),
        ((7, 6), (7, 8)),
        ((7, 8), (0, 8)), # 방 1번
        ((10, 0), (10, 4)),
        ((10, 4), (9, 4)),
        ((8, 4), (6, 4)), # 방 2번
        ((10, 1), (14, 1)),
        ((14, 1), (14, 6)),
        ((14, 6), (9, 6)),
        ((10, 6), (10, 5)), # 방 3번
        ((9, 6), (9, 8)), # 방 1,2,3 앞 복도
        ((14, 2), (20, 2)),
        ((20, 8), (18, 8)),
        ((16, 8), (13, 8)),
        ((14, 7), (14, 8)), # 방 4번
        ((13, 8), (13, 10)),    
        ((13, 11), (13, 13)),
        ((13, 13), (20, 13)), # 방 5번  
        ((14, 13), (14, 14)),
        ((14, 15), (14, 20)),
        ((14, 19), (20, 19)), # 방 6번
        ((6, 20), (6, 16)),
        ((6, 16), (8, 16)),
        ((8, 16), (8, 17)),
        ((8, 17), (9, 17)),
        ((11, 17), (12, 17)),
        ((12, 17), (12, 16)),
        ((12, 16), (14, 16)), # 방 7번 (바깥) 구현
        ((1, 8), (1, 20)),
        ((1, 14), (6, 14)),
        ((6, 15), (6, 12)), # 방 8번
        ((6, 8), (6, 11)), # 방 9번
        ((8, 10), (10, 10)),
        ((11, 10), (12, 10)),
        ((12, 10), (12, 11)),
        ((12, 12), (12, 13)),
        ((12, 13), (11, 13)),
        ((10, 13), (8, 13)),
        ((8, 13), (8, 12)),
        ((8, 11), (8, 10)), # 시작점 방
]
room_walls = [((x[0][0]*square_size + wall_pos[0], x[0][1]*square_size + wall_pos[1]), # 방 벽 설정
                (x[1][0]*square_size + wall_pos[0], x[1][1]*square_size + wall_pos[1])) for x in room_walls_pos]
room_shortcut_loc = ((0, 2), (14, 2), (5, 19), (14, 18)) # 방의 통로 위치 설정
grid_bonus_loc = ((8, 5), (10, 6), (9, 13), (12, 12), (11, 15)) # 보너스카드 위치 설정
grid_bonus = [(wall_pos[0] + x * square_size, wall_pos[1] + y * square_size) for x, y in grid_bonus_loc] #`grid_bonus_loc` 위치에 보너스카드 추가

def auto_close_msgbox(delay=2): # 메시지 박스 자동 닫기 함수
    time.sleep(delay)
    try: # try문을 사용하여 예외 처리
        win = win32gui.FindWindow(None, "알림" or "경고" or "오류" or "취소" or "실패" or "정보")
        ctypes.windll.user32.PostMessageA(win, 0x0010, 0, 0)
    except Exception as e: print(e) # 예외 처리 
def show_message(title, message): # 메시지 표시 함수
    threading.Thread(target=auto_close_msgbox).start()
    if title == "경고": # 경고
        tk.messagebox.showwarning(title, message)
        return True
    elif title == "오류" or title == "실패": # 오류, 실패
        tk.messagebox.showerror(title, message)
        return True
    elif title == "정보": # 정보
        return tk.messagebox.askquestion(title, message)
    else: # 알림, 취소
        tk.messagebox.showinfo(title, message)
        return True
def brighten_color(color, isBrigther): # 색상을 밝게 만드는 함수
    if isBrigther == True: # 밝은 모드인 경우
        brightened_color = [min(int(channel * 255 + 0.6 * 255), 255) for channel in color] # 각 색상 채널의 값을 증가시켜 색상을 밝게 만듭니다.
        return brightened_color # 밝은 색상을 반환합니다.
    else: return color
def draw_card(window, font, border_color, thickness, wall_color, card_pos, card_width, card_height, square_size, cards, start_height): # 카드를 그리기 위한 함수
    if cards == bonus_cards_list:  # cards가 bonus_cards_list인 경우
        card_width *= 1.3  # 카드 너비를 1.3배로 증가
        card_height *= 1.3  # 카드 높이를 1.3배로 증가
        font = pg.font.SysFont('malgungothic', square_size // 3 * 13 // 10) # 큰 폰트 설정
    for i, card in enumerate(cards): # 각 카드에 대해
        row = i // 4
        col = i % 4 # 행 및 열 설정
        x = card_pos[0] + col * (card_width + square_size // 2) # x 좌표 설정
        y = card_pos[1] + row * (card_height + square_size // 4) + start_height * (card_height + square_size // 4) # 시작 높이에 따라 y 좌표 설정
        pg.draw.rect(window, border_color, (x, y, card_width, card_height), thickness)
        if len(card) > 5: card = card[:5] + "..." # 카드 이름이 5글자를 넘어가면 ...으로 표시
        draw_text(window, card, font, wall_color, (x + card_width / 2, y + card_height / 2)) # 카드 이름 표시시
def add_rooms_to_grid(rooms, square_size, grid): # 방을 그리드에 추가하는 함수
    for room in rooms: # 각 방에 대해
        room = pg.Rect(*room) # 방의 위치 및 크기를 가져옵니다.
        for x in range(room.left, room.right, square_size): # 방의 좌우 범위에 대해
            for y in range(room.top, room.bottom, square_size): grid.add((x, y)) # 방의 각 좌표를 그리드에 추가
def shuffle_and_distribute_cards(suspects, weapons, locs, num_cards): # 카드 섞고 나눠주기
    su = list(suspects.keys()) # 용의자 카드
    random.shuffle(su) # 용의자 카드 섞기
    random.shuffle(weapons) # 도구 카드 섞기
    random.shuffle(locs) # 장소 카드 섞기
    case_envelope = { # 사건봉투
        'suspect': su.pop(), # 용의자 카드
        'tool': weapons.pop(), # 도구 카드
        'place': locs.pop() # 장소 카드
    }
    all_cards = list(su) + list(weapons) + list(locs)  # 모든 카드를 합칩니다.
    random.shuffle(all_cards)  # 카드를 섞습니다.
    player_cards = {} # 플레이어 카드를 저장할 딕셔너리 생성
    for i in range(1, 5): # 4명의 플레이어에게 카드 나눠주기
        player_cards[list(suspects.keys())[i]] = all_cards[num_cards * (i - 1):num_cards * i] #플레이어에게 카드 나눠주기
        print(list(suspects.keys())[i - 1], "카드:", player_cards[list(suspects.keys())[i]]) 
    last_cards = all_cards[num_cards * 4:] # 남은 카드
    return case_envelope, player_cards, last_cards
def add_walls_to_grid(wall_pos, square_size, grid, window, background_color, grid_color, thickness): # 벽을 그리드에 추가하는 함수
    font = pg.font.Font(None, square_size) # 폰트 객체 생성
    question_mark = font.render("?", True, RED) # "?" 문자를 Surface 객체로 변환
    for x in range(wall_pos.left, wall_pos.right, square_size): # 벽의 각 좌표에 대해
        for y in range(wall_pos.top, wall_pos.bottom, square_size): # 벽의 각 좌표에 대해
            rect = pg.Rect(x, y, square_size, square_size) # 사각형 생성
            if (x, y) in grid: pg.draw.rect(window, background_color, rect) # 그리드에 있는 경우 배경색으로 채우기
            else: # 그리드에 없는 경우
                if (rect[0], rect[1]) in grid_bonus: # 보너스카드 위치에 있는 경우
                    pg.draw.rect(window, brighten_color(RED, True), rect) # 보너스카드 위치에 연한 빨간색으로 채우기
                    window.blit(question_mark, (rect[0] + square_size / 4, rect[1] + square_size / 4)) # 보너스카드 위치에 "?" 표시
                pg.draw.rect(window, grid_color, rect, thickness // 2) # 그리드에 없는 경우 그리드 색상으로 선 그리기
def draw_wall(window, wall_color, wall_pos, thickness): # 벽 그리기
    pg.draw.rect(window, wall_color, wall_pos, thickness) 
def draw_room_walls(window, wall_color, room_walls, thickness): # 방 벽 그리기
    for wall in room_walls: pg.draw.line(window, wall_color, wall[0], wall[1], thickness) # 각 방 벽에 대해 선 그리기
def draw_room_names(window, font, wall_color, square_size, rooms, room_names): # 방 이름 그리기
    if len(rooms) >= len(room_names): # 방의 수가 방 이름의 수보다 많거나 같은 경우
        for i, room in enumerate(rooms): # 각 방에 대해
            draw_text(window, room_names[i], font, GRAY, (room[0] + square_size * (6 if len(room_names[i]) == 3 else 4) / 5, room[1] + square_size * 2 / 5)) # 방 이름 표시
def create_player(rooms, square_size, player_size, player_name, loc): # 플레이어 생성
    print(player_name, "위치:", loc)
    x, y = (loc[0] - 6) * square_size + (square_size - player_size) / 2 , (loc[1] - 6) * square_size + (square_size - player_size) / 2 # x 좌표 및 y 좌표 설정
    player = (player_name, pg.Rect(rooms[1][0] + x, rooms[1][1] + y, player_size, player_size))
    return player
def draw_player(window, player, isBrigther): # 플레이어 그리기
    color = brighten_color(suspects[player[0]], isBrigther) # 플레이어 색상 설정
    pg.draw.rect(window, color, player[1]) 
    pg.display.flip()
    return player
def create_and_draw_players(window, rooms, square_size, player_size, player_pos): # 플레이어 생성 및 그리기
    players = [create_player(rooms, square_size, player_size, player_name, loc) for player_name, loc in player_pos.items()] # 플레이어 생성
    for player in players: draw_player(window, player, False) # 플레이어 그리기
def roll_dice(): # 주사위 굴리기
    pg.display.flip() # 창 업데이트
    dice = random.randint(1, 6) # 주사위 굴리기
    return dice
def draw_dice(dice1, dice2): # 주사위 그리기
    dice1_pos = wall_pos[0] + 21 * square_size, wall_pos[1] + 15 * square_size, 2 * square_size, 2 * square_size # 주사위 위치 및 크기 설정
    dice2_pos = wall_pos[0] + 24 * square_size, wall_pos[1] + 15 * square_size, 2 * square_size, 2 * square_size # 주사위 위치 및 크기 설정
    pg.draw.rect(window, background_color, dice1_pos) # 주사위 1의 배경색 설정
    pg.draw.rect(window, background_color, dice2_pos) # 주사위 2의 배경색 설정
    pg.draw.rect(window, wall_color, dice1_pos, thickness) # 주사위 1의 외곽선 그리기
    pg.draw.rect(window, wall_color, dice2_pos, thickness) # 주사위 2의 외곽선 그리기
    dice_font = pg.font.SysFont('malgungothic', square_size) # 주사위 폰트 설정
    dice1_text = dice_font.render(str(dice1), True, wall_color) # 주사위 1의 결과
    dice2_text = dice_font.render(str(dice2), True, wall_color) # 주사위 2의 결과
    window.blit(dice1_text, ((dice1_pos[0] + square_size) - square_size / 4, (dice1_pos[1] + square_size / 4))) # 주사위 1의 결과 표시
    window.blit(dice2_text, ((dice2_pos[0] + square_size) - square_size / 4, (dice2_pos[1] + square_size / 4))) # 주사위 2의 결과 표시
def draw_button(window, color, pos, text, font, thickness): # 버튼 그리기
    font = pg.font.SysFont('malgungothic', square_size // 2) # 폰트 설정
    pg.draw.rect(window, color, pos, thickness)
    draw_text(window, text, font, BLACK, (pos[0] + square_size * 2, pos[1] + square_size * 1))
def draw_text(window, text, font, color, pos): # 텍스트 그리기
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=pos)
    window.blit(text, text_rect)
def handle_click(x, y, button_pos): # 클릭한 위치 처리
    print("클릭한 위치:", x, y)
    if button_pos[0] <= x <= button_pos[0] + button_pos[2] and button_pos[1] <= y <= button_pos[1] + button_pos[3]: # 버튼을 클릭한 경우
        return True
def outStartRoom(new_pos, room, isOutStartRoom, cur_player, player_size): # 시작점 방을 나가는 경우
    room_x_start, room_y_start, width, height = room  # 방의 위치 및 크기 설정
    room_x_end = room_x_start + width # 방의 끝 위치 설정
    room_y_end = room_y_start + height # 방의 끝 위치 설정
    room_x_start, room_x_end = room_x_start / square_size - 1, room_x_end / square_size - 1 # 방의 시작 및 끝 위치 보정
    room_y_start, room_y_end = room_y_start / square_size - 2, room_y_end / square_size - 2 # 방의 시작 및 끝 위치 보정
    if room_x_start <= (new_pos[0] + player_size / 20) <= room_x_end and room_y_start < (new_pos[1] + player_size / 20) <= room_y_end and isOutStartRoom[cur_player] is False: return False
    else: return True # 시작점 방을 나간 경우
def handle_room_entry(new_pos, rooms, cur_player, player_size, isOutStartRoom, other_players_poss): # 방에 들어가는 경우
    for room in rooms: # 각 방에 대해
        x_start, y_start, width, height = room # 방의 위치 및 크기
        x_end = x_start + width # 방의 끝 위치
        y_end = y_start + height # 방의 끝 위치
        x_start, x_end = x_start / square_size - 1, x_end / square_size - 1 # 방의 시작 및 끝 위치 보정
        y_start, y_end = y_start / square_size - 2, y_end / square_size - 2 # 방의 시작 및 끝 위치 보정
        if isOutStartRoom[cur_player] is True : # 시작점 방을 나간 경우
            if x_start <= (new_pos[0] + player_size / 20) <= x_end and y_start < (new_pos[1] + player_size / 20) <= y_end: # 방에 들어온 경우
                print(cur_player, "이/가", room_names[rooms.index(room)], "방에 들어왔습니다.")
                show_message("알림", cur_player + "이/가 " + room_names[rooms.index(room)] + "방에 들어왔습니다.")
                while True: # 다른 플레이어가 있거나 방의 통로 위치인 경우
                    new_pos = (random.randint(int(x_start), int(x_end) - 1), random.randint(int(y_start), int(y_end) - 1))
                    if new_pos not in other_players_poss.values() and new_pos not in room_shortcut_loc: break
    return new_pos
def do_dice_roll(previous_dice1, previous_dice2, dice1, dice2, dice_roll_cnt, player_pos): # 주사위 굴리기
    cur_player = None # 현재 플레이어를 저장하는 변수
    if previous_dice1 is None and previous_dice2 is None:  # 이전 주사위 결과가 없는 경우
        dice1 = roll_dice()  # 주사위를 굴립니다.
        dice2 = roll_dice()  # 주사위를 굴립니다.
        dice_roll_cnt += 1  # 주사위 굴린 횟수를 증가시킵니다.
    else: # 이전 주사위 결과가 있는 경우
        dice1 = previous_dice1  # 이전 주사위 결과를 사용합니다.
        dice2 = previous_dice2  # 이전 주사위 결과를 사용합니다.
        previous_dice1 = None  # 이전 주사위 결과를 초기화합니다.
        previous_dice2 = None  # 이전 주사위 결과를 초기화합니다.
    cur_player = list(player_pos.keys())[dice_roll_cnt % 4 - 1] # 현재 플레이어를 결정합니다.
    return cur_player, player_pos, dice1, dice2, previous_dice1, previous_dice2, dice_roll_cnt
def move_player(cur_player, player_size, player_pos, dice1, dice2, other_players_poss, isOutStartRoom): # 플레이어 이동
    #os.system('cls') # 화면 지우기
    new_poss = [player_pos]  # 이동한 모든 좌표를 저장하는 리스트
    new_pos = player_pos  # 새로운 위치
    old_pos = player_pos
    dice_roll = dice1 + dice2
    cur_dir = None
    print("이동 전 위치:", old_pos)
    print("주사위 결과:", dice_roll)
    while dice_roll > 0: # 주사위를 모두 사용할 때까지
        event = pg.event.wait()
        if event.type == pg.KEYDOWN: # 키를 누른 경우
            if event.key == pg.K_UP: # 위쪽 방향키를 누른 경우
                print("위로 이동")
                new_pos = player_pos[0], player_pos[1] - 1
                cur_dir = "위쪽"
            elif event.key == pg.K_DOWN: # 아래쪽 방향키를 누른 경우
                print("아래로 이동")
                new_pos = player_pos[0], player_pos[1] + 1
                cur_dir = "아래쪽"
            elif event.key == pg.K_LEFT: # 왼쪽 방향키를 누른 경우
                print("왼쪽으로 이동")
                new_pos = player_pos[0] - 1, player_pos[1]
                cur_dir = "왼쪽"
            elif event.key == pg.K_RIGHT: # 오른쪽 방향키를 누른 경우
                print("오른쪽으로 이동")
                new_pos = player_pos[0] + 1, player_pos[1]
                cur_dir = "오른쪽"
            elif event.key == pg.K_ESCAPE: # ESC 키를 누른 경우
                exit() # 게임 종료
            elif event.key == pg.K_RETURN: # 엔터 키를 누른 경우
                root = tk.Tk()
                print(cur_player, "는 아직", dice_roll, "칸 이동하지 않았음") 
                root.withdraw()  # root 창을 숨깁니다.
                if show_message("정보", "아직 " + str(dice_roll) + "칸 이동하지 않았습니다. 정말 끝내시겠습니까?"): # Yes/No 대화상자를 표시합니다.
                    show_message("알림", "이동을 끝냅니다.")
                    print(cur_player, "가 이동을 끝냄")
                    return player_pos
                else: # No를 누른 경우
                    show_message("취소", "계속 진행합니다.")
                    print("취소, 계속 진행함")
                    continue
            else: continue # 다른 키를 누른 경우
            mid_pos = ((player_pos[0] + new_pos[0]) / 2, (player_pos[1] + new_pos[1]) / 2) # 중간 위치
            mid = (int(mid_pos[0]*square_size + wall_pos[0] + square_size / 2), int(mid_pos[1]*square_size + wall_pos[1] + square_size / 2)) # 중간 위치(벽 판별 위해)
            print("현재 방향 : ", cur_dir, "중간 위치 :", mid_pos)
            if window.get_at(mid) == BLACK: # 벽이 있는 경우
                print("이동 불가,", cur_dir, "에 벽이 있음, 위치 :", new_pos)
                show_message("경고", cur_dir + "에 벽이 있어 이동할 수 없습니다. 다시 선택해주세요.")
                player_pos = new_poss[-1] # 마지막으로 성공한 위치로 돌아갑니다.
            else: # 벽이 없는 경우
                enter_room = handle_room_entry(new_pos, rooms, cur_player, player_size, isOutStartRoom, other_players_poss) # 방에 들어가는 경우
                if new_pos in other_players_poss.values(): # 다른 플레이어가 있는 경우 
                    print("이동 불가, 다른 플레이어가 있음, 위치 :", new_pos)
                    show_message("경고", "다른 플레이어가 있어 이동할 수 없습니다. 다시 선택해주세요.")
                    player_pos = new_poss[-1]  # 마지막으로 성공한 위치로 돌아갑니다.
                    continue
                elif enter_room != new_pos: # 방에 들어가는 경우
                    new_poss.append(enter_room)
                    player_pos = enter_room
                    dice_roll = 0
                elif new_pos[-1] == player_pos: # 이미 이동한 위치인 경우 1
                    print("이동 불가, 이미 이동한 위치:", new_pos)
                    show_message("실패", "이미 이동한 위치입니다. 다시 선택해주세요.")
                    player_pos = new_pos # 마지막으로 성공한 위치로 돌아갑니다.
                    continue
                elif new_pos in new_poss: # 이미 이동한 위치인 경우 2
                    print("이동 불가, 이미 이동한 위치:", new_pos)
                    show_message("실패", "이미 이동한 위치입니다. 다시 선택해주세요.")
                    player_pos = new_poss[-1]  # 마지막으로 성공한 위치로 돌아갑니다.
                    continue
                elif new_pos[0] < 0 or new_pos[0] > 19 or new_pos[1] < 0 or new_pos[1] > 19: # 보드를 벗어난 경우
                    print("오류, 보드를 벗어남, 위치 :", new_pos)
                    show_message("오류", "보드를 벗어난 위치입니다.")
                    exit()
                else: # 이동 가능한 경우
                    isOutStartRoom[cur_player] = outStartRoom(new_pos, rooms[12], isOutStartRoom, cur_player, player_size)
                    print(isOutStartRoom) 
                    draw_player(window, create_player(rooms, square_size, player_size, cur_player, new_pos), True) # 플레이어 그리기
                    new_poss.append(new_pos)  # 새로운 위치를 리스트에 추가
                    player_pos = new_pos
                    dice_roll -= 1
        if dice_roll == 0: # 주사위를 모두 사용한 경우
            print(cur_player, ":", player_pos, "으로 이동합니다.") 
            show_message("알림", (cur_player + "이/가 " + str(player_pos) + " 으로 이동합니다."))
            print(cur_player, "위치 이동", old_pos, " -> ", player_pos)
            return player_pos
def draw_all(font, card_font, border_color, border_thickness, wall_color, player_cards, card_pos, card_width, card_height, square_size, 
             rooms, grid, room_names, room_walls, all_cards, bonus_cards_list, case_envelope, thickness, player_size, player_pos, dice1, dice2, button_pos): # 모든 요소 그리기
    window.fill(background_color) # 창 배경색으로 채우기
    add_walls_to_grid(wall_pos, square_size, grid, window, background_color, grid_color, thickness) # 벽을 그리드에 추가
    draw_wall(window, wall_color, wall_pos, thickness) # 벽 그리기
    draw_room_walls(window, wall_color, room_walls, thickness) # 방 벽 그리기
    draw_room_names(window, font, wall_color, square_size, rooms, room_names) # 방 이름 그리기
    for i in range(4): # 각 플레이어에 대해
        draw_card(window, card_font, border_color, border_thickness, wall_color, card_pos, card_width, card_height, square_size, list(player_cards.values())[i], i) # 플레이어 카드 그리기
    draw_card(window, card_font, border_color, border_thickness, wall_color, card_pos, card_width, card_height, square_size, all_cards, 4) # 모든 카드 그리기
    draw_card(window, card_font, border_color, border_thickness, wall_color, card_pos, card_width, card_height, square_size, bonus_cards_list, 4) # 보너스 카드 그리기
    draw_card(window, card_font, border_color, border_thickness, wall_color, card_pos, card_width, card_height, square_size, list(case_envelope.values()), 10) # 사건봉투 카드 그리기
    create_and_draw_players(window, rooms, square_size, player_size, player_pos) # 플레이어 생성 및 그리기
    draw_dice(dice1, dice2) # 주사위 그리기
    draw_button(window, wall_color, button_pos, "주사위 굴리기", font, thickness) # 주사위 굴리기 버튼 그리기
    pg.display.flip() # 창 업데이트

def main(): # 메인 함수
    pg.init() # pg 초기화
    dice1 = 0  # 주사위 초기값 설정
    dice2 = 0  # 주사위 초기값 설정
    dice_roll_cnt = 0 # 주사위 굴린 횟수
    grid = set() # 그리드 설정
    font = pg.font.SysFont('malgungothic', square_size * 2 // 3) # 폰트 설정
    add_rooms_to_grid(rooms, square_size, grid) # 방을 그리드에 추가
    num_cards = 4  # 각 플레이어에게 나눠줄 카드의 수 : 4명이므로 4장
    case_envelope, player_cards, all_cards = shuffle_and_distribute_cards(suspects, weapons, locs, num_cards) # 카드 섞고 나눠주기
    player_size = square_size / 3 # 플레이어 크기
    player_pos = { # 각 플레이어의 초기 위치를 설정합니다.
        list(suspects.keys())[0] : (8, 10),
        list(suspects.keys())[1] : (11, 10),
        list(suspects.keys())[2] : (8, 12),
        list(suspects.keys())[3] : (11, 12),
    }
    card_pos = wall_pos[0] + wall_pos[2] + 1 * square_size, wall_pos[1] # 카드 위치 설정
    card_width = square_size * 2 # 카드 너비
    card_height = square_size # 카드 높이
    card_font = pg.font.SysFont('malgungothic', square_size // 3) # 카드 폰트
    border_color = wall_color # 테두리 색상
    border_thickness = thickness # 테두리 두께
    button_pos = wall_pos[0] + 21 * square_size, wall_pos[1] + 18 * square_size, 4 * square_size, 2 * square_size # 버튼 위치 설정
    isOutStartRoom = { # 시작점 방을 나갔는지 여부
        list(suspects.keys())[0]: False,
        list(suspects.keys())[1]: False,
        list(suspects.keys())[2]: False,
        list(suspects.keys())[3]: False,
    }
    draw_all(font, card_font, border_color, border_thickness, wall_color, player_cards, card_pos, card_width, card_height, square_size, # 모든 요소 그리기
             rooms, grid, room_names, room_walls, all_cards, bonus_cards_list, case_envelope, thickness, player_size, player_pos, dice1, dice2, button_pos)
    pg.display.flip() # 창 업데이트

    running = True # 게임 실행 여부
    previous_dice1 = None  # 이전 주사위 결과를 저장하는 변수
    previous_dice2 = None  # 이전 주사위 결과를 저장하는 변수
    notMoved = False # 이동하지 않은 경우
    while running: # 게임이 실행 중인 동안
        if notMoved: # 이동하지 않은 경우
            cur_player, player_pos, dice1, dice2, previous_dice1, previous_dice2, dice_roll_cnt = do_dice_roll(previous_dice1, previous_dice2, dice1, dice2, dice_roll_cnt, player_pos)
            draw_all(font, card_font, border_color, border_thickness, wall_color, player_cards, card_pos, card_width, card_height, square_size, # 모든 요소 그리기
                     rooms, grid, room_names, room_walls, all_cards, bonus_cards_list, case_envelope, thickness, player_size, player_pos, dice1, dice2, button_pos)
            other_players_poss = {player[0]: (player[1][0], player[1][1]) for player in player_pos.items() if player[0] != cur_player} # 나머지 플레이어들의 좌표를 가져옵니다.    
            new_pos = move_player(cur_player, player_size, player_pos[cur_player], dice1, dice2, other_players_poss, isOutStartRoom)
            if new_pos == player_pos[cur_player]:  # 이동하지 않은 경우
                previous_dice1 = dice1 # 이전 주사위 결과를 저장합니다.
                previous_dice2 = dice2 # 이전 주사위 결과를 저장합니다.
                notMoved = True       
            else: # 이동한 경우
                previous_dice1 = None # 이전 주사위 결과를 초기화합니다.
                previous_dice2 = None # 이전 주사위 결과를 초기화합니다.
                notMoved = False          
            player_pos[cur_player] = new_pos 
            draw_all(font, card_font, border_color, border_thickness, wall_color, player_cards, card_pos, card_width, card_height, square_size, 
                     rooms, grid, room_names, room_walls, all_cards, bonus_cards_list, case_envelope, thickness, player_size, player_pos, dice1, dice2, button_pos) # 모든 요소 그리기
        else: # 이동한 경우
            for event in pg.event.get(): # 각 이벤트에 대해
                if event.type == pg.QUIT: # 종료 이벤트인 경우
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE): # 마우스 버튼을 누른 경우 또는 스페이스바를 누른 경우
                    if event.type == pg.MOUSEBUTTONDOWN: x, y = event.pos  # 클릭한 위치를 가져옵니다.
                    if (event.type == pg.KEYDOWN and event.key == pg.K_SPACE) or handle_click(x, y, button_pos) : # 주사위 굴리기 버튼을 클릭했거나 스페이스바를 누른 경우
                        cur_player, player_pos, dice1, dice2, previous_dice1, previous_dice2, dice_roll_cnt = do_dice_roll(previous_dice1, previous_dice2, dice1, dice2, dice_roll_cnt, player_pos)
                        draw_all(font, card_font, border_color, border_thickness, wall_color, player_cards, card_pos, card_width, card_height, square_size, 
                                 rooms, grid, room_names, room_walls, all_cards, bonus_cards_list, case_envelope, thickness, player_size, player_pos, dice1, dice2, button_pos) # 모든 요소 그리기
                        other_players_poss = {player[0]: (player[1][0], player[1][1]) for player in player_pos.items() if player[0] != cur_player} # 나머지 플레이어들의 좌표를 가져옵니다.    
                        new_pos = move_player(cur_player, player_size, player_pos[cur_player], dice1, dice2, other_players_poss, isOutStartRoom)
                        if new_pos == player_pos[cur_player]:  # 이동하지 않은 경우
                            previous_dice1 = dice1 # 이전 주사위 결과를 저장합니다.
                            previous_dice2 = dice2 # 이전 주사위 결과를 저장합니다.
                            notMoved = True       
                        else: # 이동한 경우
                            previous_dice1 = None # 이전 주사위 결과를 초기화합니다.
                            previous_dice2 = None # 이전 주사위 결과를 초기화합니다.      
                            notMoved = False      
                        player_pos[cur_player] = new_pos 
                        draw_all(font, card_font, border_color, border_thickness, wall_color, player_cards, card_pos, card_width, card_height, square_size, 
                                 rooms, grid, room_names, room_walls, all_cards, bonus_cards_list, case_envelope, thickness, player_size, player_pos, dice1, dice2, button_pos) # 모든 요소 그리기

    pg.quit() # pg 종료 

if __name__ == "__main__":
    main() # 메인 함수 실행
