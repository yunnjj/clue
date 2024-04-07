import pygame
import random
import os
import time
import sys
from matplotlib import colors
import tkinter as tk
from tkinter import messagebox

square_size = 30  # 기본 사각형 크기 설정
window_size = (square_size * 40, square_size * 24) # 창 크기 설정
background_color = (255, 255, 255) # 창 배경색 설정
wall_color = (0, 0, 0)  # 벽의 색상 설정
wall_position = pygame.Rect(window_size[0] / 2 - square_size * 19, window_size [1] / 2 - square_size * 10, 20 * square_size, 20 * square_size) # 벽의 위치 설정
grid_color = (200, 200, 200)  # 그리드 색상
thickness = square_size // 10 # 선 두께 설정
window = pygame.display.set_mode(window_size) # `window_size` 크기의 창 생성
pygame.display.set_caption("CLUE - board game") # 창 제목 설정
window.fill(background_color) # 창 배경색으로 채우기

suspects = { # 용의자카드
        "피콕": "Blue",
        "플럼": "Purple",
        "스칼렛": "Red",
        "머스타드": "Yellow",
        "그린": "Green",
        "화이트": "White"
}
weapons = ["파이프", "밧줄", "단검", "렌치", "권총", "촛대"]  # 도구카드
locations = ["침실", "욕실", "서제", "부엌", "식당", "거실", "마당", "차고", "게임룸"]  # 장소카드
bonus_cards = { # 보너스카드
        "차례를 한 번 더 진행합니다." : "지금 사용하거나 필요할 때 사용합니다.",
        "원하는 장소로 이동합니다." : "지금 사용합니다.",
        "카드 엿보기" : "누군가 다른 사람에게 추리 카드를 보여줄 때 그 카드를 볼 수 있습니다. 필요할 때 사용합니다.",
        "나온 주사위에 6을 더할 수 있습니다." : "지금 사용하거나 필요할 때 사용합니다.",
        "다른 사람의 카드 한 장을 공개합니다." : "한 사람을 정해 이 카드를 보여주면, 그 사람은 자기 카드 중 한 장을 모두에게 보여주어야 합니다. 지금 사용합니다.",
        "한 번 더 추리합니다." : "자기 말이나 다른 사람의 말 또는 토큰을 이용하지 않고 원하는 장소, 사람, 도구를 정해 추리할 수 있습니다. 지금 사용합니다."
}
bonus_cards_list = [card for card in bonus_cards for _ in range(2)] # 각 카드를 원하는 수만큼 복제합니다.
bonus_cards_list.extend(["원하는 장소로 이동합니다."])

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
room_position = [ # 방의 위치 설정
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
rooms = [(wall_position[0] + x * square_size, wall_position[1] + y * square_size, w * square_size, h * square_size) for (x, y), (w, h) in zip(room_position, room_size)] # 방의 위치와 크기를 결합
room_walls_position = [ # 방 벽 위치 설정
        # 방 1번
        ((0, 2), (6, 2)),
        ((6, 0), (6, 3)),
        ((6, 4), (6, 5)),
        ((6, 6), (7, 6)),
        ((7, 6), (7, 8)),
        ((7, 8), (0, 8)),
        # 방 2번
        ((10, 0), (10, 4)),
        ((10, 4), (9, 4)),
        ((8, 4), (6, 4)),
        # 방 3번
        ((10, 1), (14, 1)),
        ((14, 1), (14, 6)),
        ((14, 6), (9, 6)),
        ((10, 6), (10, 5)),
        # 방 1,2,3 앞 복도
        ((9, 6), (9, 8)),
        # 방 4번
        ((14, 2), (20, 2)),
        ((20, 8), (18, 8)),
        ((16, 8), (13, 8)),
        ((14, 7), (14, 8)),
        # 방 5번
        ((13, 8), (13, 10)),    
        ((13, 11), (13, 13)),
        ((13, 13), (20, 13)),
        # 방 6번
        ((14, 13), (14, 14)),
        ((14, 15), (14, 20)),
        ((14, 19), (20, 19)),
        # 방 7번 (바깥) 구현
        ((6, 20), (6, 16)),
        ((6, 16), (8, 16)),
        ((8, 16), (8, 17)),
        ((8, 17), (9, 17)),
        ((11, 17), (12, 17)),
        ((12, 17), (12, 16)),
        ((12, 16), (14, 16)),
        # 방 8번
        ((1, 8), (1, 20)),
        ((1, 14), (6, 14)),
        ((6, 15), (6, 12)),
        # 방 9번 
        ((6, 8), (6, 11)),
        # 시작점 방
        ((8, 10), (10, 10)),
        ((11, 10), (12, 10)),
        ((12, 10), (12, 11)),
        ((12, 12), (12, 13)),
        ((12, 13), (11, 13)),
        ((10, 13), (8, 13)),
        ((8, 13), (8, 12)),
        ((8, 11), (8, 10)),
        # 필요한 만큼 방 벽을 추가
]
room_walls = [((x[0][0]*square_size + wall_position[0], x[0][1]*square_size + wall_position[1]),
                (x[1][0]*square_size + wall_position[0], x[1][1]*square_size + wall_position[1])) for x in room_walls_position] # 방 벽 설정
grid_bonus_location = ((8, 5), (10, 6), (9, 13), (12, 12), (11, 15)) # 보너스카드 위치 설정
grid_bonus = [(wall_position[0] + x * square_size, wall_position[1] + y * square_size) for x, y in grid_bonus_location] #`grid_bonus_location` 위치에 보너스카드 추가

def ask_move_confirmation():
    root = tk.Tk()
    root.withdraw()  # root 창을 숨깁니다.
    return messagebox.askyesno("이동 확인", "이동하시겠습니까?")  # Yes/No 대화상자를 표시합니다.
def brighten_color(color_name, isBrigther): # 색상을 밝게 만드는 함수
    if isBrigther == True: # 밝은 모드인 경우
        rgb_color = colors.to_rgb(color_name) # 색상을 RGB 형식으로 변환합니다.
        brightened_color = [min(int(channel * 255 + 0.6 * 255), 255) for channel in rgb_color] # 각 색상 채널의 값을 증가시켜 색상을 밝게 만듭니다.
        return brightened_color # 밝은 색상을 반환합니다.
    else: return [int(channel * 255) for channel in colors.to_rgb(color_name)] # 색상을 RGB 형식으로 변환합니다.
def draw_card(window, font, border_color, thickness, wall_color, card_position, card_width, card_height, square_size, cards, start_height): # 카드를 그리기 위한 함수
    if cards == bonus_cards_list:  # cards가 bonus_cards_list인 경우
        card_width *= 1.3  # 카드 너비를 1.3배로 증가
        card_height *= 1.3  # 카드 높이를 1.3배로 증가
        font = pygame.font.SysFont('malgungothic', square_size // 3 * 13 // 10) # 큰 폰트 설정
    for i, card in enumerate(cards): # 각 카드에 대해
        row = i // 4
        col = i % 4 # 행 및 열 설정
        x = card_position[0] + col * (card_width + square_size // 2) # x 좌표 설정
        y = card_position[1] + row * (card_height + square_size // 4) + start_height * (card_height + square_size // 4) # 시작 높이에 따라 y 좌표 설정
        pygame.draw.rect(window, border_color, (x, y, card_width, card_height), thickness)
        if len(card) > 5: card = card[:5] + "..." # 카드 이름이 5글자를 넘어가면 ...으로 표시
        text = font.render(card, True, wall_color) # 카드 이름 생성
        text_rect = text.get_rect(center=(x + card_width / 2, y + card_height / 2))
        window.blit(text, text_rect) # 카드 이름 표시
def add_rooms_to_grid(rooms, square_size, grid): # 방을 그리드에 추가하는 함수
    for room in rooms: # 각 방에 대해
        room = pygame.Rect(*room) # 방의 위치 및 크기를 가져옵니다.
        for x in range(room.left, room.right, square_size): # 방의 좌우 범위에 대해
            for y in range(room.top, room.bottom, square_size): grid.add((x, y)) # 방의 각 좌표를 그리드에 추가
def add_walls_to_grid(wall_position, square_size, grid, window, background_color, grid_color, thickness): # 벽을 그리드에 추가하는 함수
    font = pygame.font.Font(None, square_size) # 폰트 객체 생성
    question_mark = font.render("?", True, "red") # "?" 문자를 Surface 객체로 변환
    for x in range(wall_position.left, wall_position.right, square_size): # 벽의 각 좌표에 대해
        for y in range(wall_position.top, wall_position.bottom, square_size): # 벽의 각 좌표에 대해
            rect = pygame.Rect(x, y, square_size, square_size) # 사각형 생성
            if (x, y) in grid: pygame.draw.rect(window, background_color, rect) # 그리드에 있는 경우 배경색으로 채우기
            else: # 그리드에 없는 경우
                if (rect[0], rect[1]) in grid_bonus: window.blit(question_mark, (rect[0] + square_size / 4, rect[1] + square_size / 4)) # 보너스카드 위치에 "?" 표시
                pygame.draw.rect(window, grid_color, rect, thickness // 2) # 그리드에 없는 경우 그리드 색상으로 선 그리기
def draw_wall(window, wall_color, wall_position, thickness): # 벽 그리기
    pygame.draw.rect(window, wall_color, wall_position, thickness) 
def draw_room_walls(window, wall_color, room_walls, thickness): # 방 벽 그리기
    for wall in room_walls: pygame.draw.line(window, wall_color, wall[0], wall[1], thickness) # 각 방 벽에 대해 선 그리기
def draw_room_names(window, font, wall_color, square_size, rooms, room_names): # 방 이름 그리기
    if len(rooms) >= len(room_names): # 방의 수가 방 이름의 수보다 많거나 같은 경우
        for i, room in enumerate(rooms): # 각 방에 대해 
            text = font.render(room_names[i], True, wall_color) # 방 이름 생성
            window.blit(text, (room[0] + square_size / 10, room[1] + square_size / 10)) # 방 이름 표시
def create_player(rooms, square_size, player_size, player_name, loc): # 플레이어 생성
    print(player_name, "위치:", loc)
    x, y = (loc[0] - 6) * square_size + (square_size - player_size) / 2 , (loc[1] - 6) * square_size + (square_size - player_size) / 2 # x 좌표 및 y 좌표 설정
    player = (player_name, pygame.Rect(rooms[1][0] + x, rooms[1][1] + y, player_size, player_size))
    return player
def draw_player(window, player, isBrigther): # 플레이어 그리기
    color = brighten_color(suspects[player[0]], isBrigther)
    pygame.draw.rect(window, color, player[1])
    pygame.display.flip()
    return player
def create_and_draw_players(window, rooms, square_size, player_size, player_position): # 플레이어 생성 및 그리기
    players = [create_player(rooms, square_size, player_size, player_name, loc) for player_name, loc in player_position.items()]
    for player in players: draw_player(window, player, False) # 플레이어 그리기
def shuffle_and_distribute_cards(suspects, weapons, locations, num_cards): # 카드 섞고 나눠주기
    # 각 카드 세트를 섞습니다.
    su = list(suspects.keys())
    random.shuffle(su)
    random.shuffle(weapons)
    random.shuffle(locations)
    # 사건봉투를 생성하고 각 세트에서 한 장씩 뽑아 넣습니다.
    case_envelope = {
        'suspect': su.pop(),
        'tool': weapons.pop(),
        'place': locations.pop()
    }
    all_cards = list(su) + list(weapons) + list(locations)  # 모든 카드를 합칩니다.
    random.shuffle(all_cards)  # 카드를 섞습니다.
    # 각 플레이어에게 카드를 나눠줍니다.
    player_cards = {}
    for i in range(1, 5): 
        player_cards[list(suspects.keys())[i]] = all_cards[num_cards * (i - 1):num_cards * i] #플레이어에게 카드 나눠주기
        print(list(suspects.keys())[i - 1], "카드:", player_cards[list(suspects.keys())[i]])
    last_cards = all_cards[num_cards * 4:] # 남은 카드
    return case_envelope, player_cards, last_cards
def draw_dice(dice1, dice2): # 주사위 그리기
    dice1_position = wall_position[0] + 21 * square_size, wall_position[1] + 15 * square_size, 2 * square_size, 2 * square_size # 주사위 위치 및 크기 설정
    dice2_position = wall_position[0] + 24 * square_size, wall_position[1] + 15 * square_size, 2 * square_size, 2 * square_size # 주사위 위치 및 크기 설정
    pygame.draw.rect(window, background_color, dice1_position) # 주사위 1의 배경색 설정
    pygame.draw.rect(window, background_color, dice2_position) # 주사위 2의 배경색 설정
    pygame.draw.rect(window, wall_color, dice1_position, thickness) # 주사위 1의 외곽선 그리기
    pygame.draw.rect(window, wall_color, dice2_position, thickness) # 주사위 2의 외곽선 그리기
    dice_font = pygame.font.SysFont('malgungothic', square_size) # 주사위 폰트 설정
    dice1_text = dice_font.render(str(dice1), True, wall_color) # 주사위 1의 결과
    dice2_text = dice_font.render(str(dice2), True, wall_color) # 주사위 2의 결과
    window.blit(dice1_text, ((dice1_position[0] + square_size) - square_size / 4, (dice1_position[1] + square_size / 4))) # 주사위 1의 결과 표시
    window.blit(dice2_text, ((dice2_position[0] + square_size) - square_size / 4, (dice2_position[1] + square_size / 4))) # 주사위 2의 결과 표시
    pygame.display.flip() # 창 업데이트
    time.sleep(0.5) # 0.5초 대기
def roll_dice():
    dice = random.randint(1, 6)
    return dice
def move_player(current_player, player_size, player_position, dice1, dice2, other_players_positions, wall_positions):
    os.system('cls') # 화면 지우기
    new_position = player_position
    old_position = player_position
    dice_roll = dice1 + dice2
    old_dice_roll = dice1 + dice2
    print("이동 전 위치:", old_position)
    print("주사위 결과:", dice_roll)
    while dice_roll > 0:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print("위로 이동")
                new_position = player_position[0], player_position[1] - 1
            elif event.key == pygame.K_DOWN:
                print("아래로 이동")
                new_position = player_position[0], player_position[1] + 1
            elif event.key == pygame.K_LEFT:
                print("왼쪽으로 이동")
                new_position = player_position[0] - 1, player_position[1]
            elif event.key == pygame.K_RIGHT:
                print("오른쪽으로 이동")
                new_position = player_position[0] + 1, player_position[1]
            draw_player(window, create_player(rooms, square_size, player_size, current_player, new_position), True)
            player_position = new_position
            dice_roll -= 1
    # 정말 이동하겠냐고 콘솔창에 물어보기
    if ask_move_confirmation(): print("이동합니다.")
    else:
        print("이동하지 않습니다.")
        dice_roll = old_dice_roll
        player_position = old_position
    os.system('cls')        
    print(current_player, "위치 이동", old_position, " -> ", player_position)
    return player_position
def draw_all(font, card_font, border_color, border_thickness, wall_color, player_cards, card_position, card_width, card_height, square_size, rooms, grid, room_names, room_walls, all_cards, bonus_cards_list, case_envelope, thickness, player_size, player_position, dice1, dice2): # 모든 요소 그리기
    window.fill(background_color) # 창 배경색으로 채우기
    add_walls_to_grid(wall_position, square_size, grid, window, background_color, grid_color, thickness) # 벽을 그리드에 추가
    draw_wall(window, wall_color, wall_position, thickness) # 벽 그리기
    draw_room_walls(window, wall_color, room_walls, thickness) # 방 벽 그리기
    draw_room_names(window, font, wall_color, square_size, rooms, room_names) # 방 이름 그리기
    for i in range(4): # 각 플레이어에 대해
        draw_card(window, card_font, border_color, border_thickness, wall_color, card_position, card_width, card_height, square_size, list(player_cards.values())[i], i) # 플레이어 카드 그리기
    draw_card(window, card_font, border_color, border_thickness, wall_color, card_position, card_width, card_height, square_size, all_cards, 4) # 모든 카드 그리기
    draw_card(window, card_font, border_color, border_thickness, wall_color, card_position, card_width, card_height, square_size, bonus_cards_list, 4) # 보너스 카드 그리기
    draw_card(window, card_font, border_color, border_thickness, wall_color, card_position, card_width, card_height, square_size, list(case_envelope.values()), 10) # 사건봉투 카드 그리기
    create_and_draw_players(window, rooms, square_size, player_size, player_position) # 플레이어 생성 및 그리기
    draw_dice(dice1, dice2) # 주사위 그리기
    pygame.display.flip() # 창 업데이트

def main():
    pygame.init() # pygame 초기화
    dice1 = 0  # 주사위 초기값 설정
    dice2 = 0  # 주사위 초기값 설정
    dice_roll_cnt = 0 # 주사위 굴린 횟수
    grid = set() # 그리드 설정
    font = pygame.font.SysFont('malgungothic', square_size * 2 // 3)
    room_names = locations.copy() # 복사
    room_names.insert(1, "") # 이름 빈 방
    room_names.insert(8, "") # 이름 빈 방
    room_names.insert(9, "") # 이름 빈 방
    room_names.insert(12, "시작점") # 시작점 방
    add_rooms_to_grid(rooms, square_size, grid) # 방을 그리드에 추가
    num_cards = 4  # 각 플레이어에게 나눠줄 카드의 수 : 4명이므로 4장
    case_envelope, player_cards, all_cards = shuffle_and_distribute_cards(suspects, weapons, locations, num_cards) # 카드 섞고 나눠주기
    player_size = square_size / 3 # 플레이어 크기
    player_position = { # 각 플레이어의 초기 위치를 설정합니다.
        list(suspects.keys())[0] : (8, 10),
        list(suspects.keys())[1] : (11, 10),
        list(suspects.keys())[2] : (8, 12),
        list(suspects.keys())[3] : (11, 12),
    }
    card_position = wall_position[0] + wall_position[2] + 1 * square_size, wall_position[1] # 카드 위치 설정
    card_width = square_size * 2 # 카드 너비
    card_height = square_size # 카드 높이
    card_font = pygame.font.SysFont('malgungothic', square_size // 3) # 카드 폰트
    border_color = wall_color # 테두리 색상
    border_thickness = thickness # 테두리 두께
    # 모든 요소 그리기
    draw_all(font, card_font, border_color, border_thickness, wall_color, player_cards, card_position, card_width, card_height, square_size, rooms, grid, room_names, room_walls, all_cards, bonus_cards_list, case_envelope, thickness, player_size, player_position, dice1, dice2) 
    pygame.display.flip() # 창 업데이트

    running = True # 게임 실행 여부
    previous_dice1 = None  # 이전 주사위 결과를 저장하는 변수
    previous_dice2 = None  # 이전 주사위 결과를 저장하는 변수
    while running: # 게임이 실행 중인 동안
        for event in pygame.event.get(): # 각 이벤트에 대해
            if event.type == pygame.QUIT: # 종료 이벤트인 경우
                running = False
            elif event.type == pygame.KEYDOWN: # 키를 누른 이벤트인 경우
                if event.key == pygame.K_SPACE: # 스페이스바를 누른 경우
                    os.system('cls') # 화면 지우기
                    if previous_dice1 is None and previous_dice2 is None:  # 이전 주사위 결과가 없는 경우
                        dice1 = roll_dice()  # 주사위를 굴립니다.
                        dice2 = roll_dice()  # 주사위를 굴립니다.
                        dice_roll_cnt += 1 # 주사위 굴린 횟수 증가
                        current_player = list(player_position.keys())[dice_roll_cnt % 4 - 1] # 현재 플레이어를 결정합니다.
                    else: # 이전 주사위 결과가 있는 경우
                        dice1 = previous_dice1  # 이전 주사위 결과를 사용합니다.
                        dice2 = previous_dice2  # 이전 주사위 결과를 사용합니다.
                        previous_dice1 = None  # 이전 주사위 결과를 초기화합니다.
                        previous_dice2 = None  # 이전 주사위 결과를 초기화합니다.
                        dice_roll_cnt -= 1 # 주사위 굴린 횟수 감소
                    draw_all(font, card_font, border_color, border_thickness, wall_color, player_cards, card_position, card_width, card_height, square_size, rooms, grid, room_names, room_walls, all_cards, bonus_cards_list, case_envelope, thickness, player_size, player_position, dice1, dice2)
                    print("주사위 굴린 횟수:", dice_roll_cnt + 1, "주사위 결과:", dice1 + dice2) # 주사위 결과 출력
                    print("현재 플레이어:", current_player)
                    players = [(player[0], player[1]) for player in player_position.items() if player[0] == current_player] # 현재 플레이어의 좌표를 가져옵니다.
                    other_players_positions = {player[0]: (player[1][0], player[1][1]) for player in player_position.items() if player[0] != current_player} # 나머지 플레이어들의 좌표를 가져옵니다.    
                    new_position = move_player(current_player, player_size, player_position[current_player], dice1, dice2, other_players_positions, wall_position)
                    if new_position == player_position[current_player]:  # 이동하지 않은 경우
                        dice_roll_cnt -= 1 # 주사위 굴린 횟수를 감소시킵니다.
                        previous_dice1 = dice1 # 이전 주사위 결과를 저장합니다.
                        previous_dice2 = dice2 # 이전 주사위 결과를 저장합니다.                   
                    player_position[current_player] = new_position
                    draw_all(font, card_font, border_color, border_thickness, wall_color, player_cards, card_position, card_width, card_height, square_size, rooms, grid, room_names, room_walls, all_cards, bonus_cards_list, case_envelope, thickness, player_size, player_position, dice1, dice2)

    pygame.quit() # pygame 종료 

if __name__ == "__main__":
    main() # 메인 함수 실행








    