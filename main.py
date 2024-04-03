import pygame
import random

pygame.init() # pygame 초기화

window_size = (1000, 600) # 창 크기 설정
square_size = 25  # 기본 사각형 크기 설정
window = pygame.display.set_mode(window_size) # `window_size` 크기의 창 생성
pygame.display.set_caption("Map") # 창 제목 설정
background_color = (255, 255, 255) # 창 배경색 설정
window.fill(background_color) # 창 배경색으로 채우기
wall_color = (0, 0, 0)  # 벽의 색상 설정
wall_position = pygame.Rect(window_size[0] / 2 - square_size * 19, 
window_size [1] / 2 - square_size * 10, 20 * square_size, 20 * square_size) # 벽의 위치 설정
grid_color = (200, 200, 200)  # 그리드 색상

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
random.shuffle(bonus_cards_list) # 카드를 섞습니다.

rooms = [     # 방의 위치와 크기 설정
    (wall_position[0] + 0 * square_size, wall_position[1] + 2 * square_size, 6 * square_size, 6 * square_size),  # Room 1
    (wall_position[0] + 6 * square_size, wall_position[1] + 6 * square_size, 1 * square_size, 2 * square_size),  # Room 1.1
    (wall_position[0] + 6 * square_size, wall_position[1] + 0 * square_size, 4 * square_size, 4 * square_size),  # Room 2
    (wall_position[0] + 10 * square_size, wall_position[1] + 1 * square_size, 4 * square_size, 5 * square_size),  # Room 3
    (wall_position[0] + 14 * square_size, wall_position[1] + 2 * square_size, 6 * square_size, 6 * square_size),  # Room 4
    (wall_position[0] + 13 * square_size, wall_position[1] + 8 * square_size, 7 * square_size, 5 * square_size),  # Room 5
    (wall_position[0] + 14 * square_size, wall_position[1] + 13 * square_size, 6 * square_size, 6 * square_size),  # Room 6
    (wall_position[0] + 8 * square_size, wall_position[1] + 17 * square_size, 4 * square_size, 3 * square_size),  # Room 7(outside)
    (wall_position[0] + 6 * square_size, wall_position[1] + 16 * square_size, 2 * square_size, 4 * square_size),  # Room 7.1(outside)
    (wall_position[0] + 12 * square_size, wall_position[1] + 16 * square_size, 2 * square_size, 4 * square_size),  # Room 7.2(outside)
    (wall_position[0] + 1 * square_size, wall_position[1] + 14 * square_size, 5 * square_size, 6 * square_size),  # Room 8
    (wall_position[0] + 1 * square_size, wall_position[1] + 8 * square_size, 5 * square_size, 6 * square_size),  # Room 9
    (wall_position[0] + 8 * square_size, wall_position[1] + 10 * square_size, 4 * square_size, 3 * square_size),  # Room start
]
room_walls = [    # 방의 벽 설정
    # 방 1번
    ((rooms[0][0], rooms[0][1]), (rooms[0][0] + rooms[0][2], rooms[0][1])),
    ((rooms[0][0] + rooms[0][2], rooms[0][1]), (rooms[0][0] + rooms[0][2], rooms[0][1] + square_size)),
    ((rooms[0][0] + rooms[0][2], rooms[0][1] + square_size * 2), (rooms[0][0] + rooms[0][2], rooms[0][1] + square_size * 3)),
    ((rooms[0][0] + rooms[0][2], rooms[0][1] + square_size * 4), (rooms[0][0] + rooms[0][2] + square_size, rooms[0][1] + square_size * 4)),
    ((rooms[0][0] + rooms[0][2] + rooms[1][2], rooms[0][1] + rooms[0][3] - rooms[1][3]), (rooms[0][0] + rooms[0][2] + rooms[1][2], rooms[0][1] + rooms[0][3])),
    ((rooms[0][0] + rooms[0][2] + rooms[1][2], rooms[0][1] + rooms[0][3]), (rooms[0][0], rooms[0][1] + rooms[0][3])),
    # 방 2번
    ((rooms[2][0], rooms[2][1]), (rooms[2][0], rooms[2][1] + square_size * 2)),
    ((rooms[2][0] + square_size * 4, rooms[2][1]), (rooms[2][0] + square_size * 4, rooms[2][1] + square_size * 4)),
    ((rooms[2][0], rooms[2][1] + square_size * 4), (rooms[2][0] + square_size * 2, rooms[2][1] + square_size * 4)),
    ((rooms[2][0] + square_size * 3, rooms[2][1] + square_size * 4), (rooms[2][0] + square_size * 4, rooms[2][1] + square_size * 4)),
    # 방 3번
    ((rooms[3][0], rooms[3][1]), (rooms[3][0] + square_size * 4, rooms[3][1])),
    ((rooms[3][0] + square_size * 4, rooms[3][1]), (rooms[3][0] + square_size * 4, rooms[3][1] + square_size * 5)),
    ((rooms[3][0], rooms[3][1] + square_size * 5), (rooms[3][0] + square_size * 4, rooms[3][1] + square_size * 5)),
    ((rooms[3][0], rooms[3][1] + square_size * 5), (rooms[3][0], rooms[3][1] + square_size * 4)),
    # 방 1,2,3 앞 복도
    ((rooms[3][0], rooms[3][1] + square_size * 5), (rooms[3][0], rooms[3][1] + square_size * 4)),
    ((rooms[3][0], rooms[3][1] + square_size * 5), (rooms[3][0] - square_size, rooms[3][1] + square_size * 5)),
    ((rooms[3][0] - square_size, rooms[3][1] + square_size * 5), (rooms[3][0] - square_size, rooms[3][1] + square_size * 7)),
    # 방 4번
    ((rooms[4][0], rooms[4][1]), (rooms[4][0] + rooms[4][2], rooms[4][1])),
    ((rooms[4][0] + rooms[4][2], rooms[4][1] + square_size * 6), (rooms[4][0] + rooms[4][2] - square_size * 2, rooms[4][1] + square_size * 6)),
    ((rooms[4][0] + rooms[4][2] - square_size * 4, rooms[4][1] + square_size * 6), (rooms[4][0] + rooms[4][2] - square_size * 7, rooms[4][1] + square_size * 6)),
    ((rooms[4][0] + rooms[4][2] - square_size * 6, rooms[4][1] + square_size * 6), (rooms[4][0] + rooms[4][2] - square_size * 6, rooms[4][1] + square_size * 5)),
    # 방 5번
    ((rooms[5][0], rooms[5][1]), (rooms[5][0], rooms[5][1] + square_size * 2)),
    ((rooms[5][0], rooms[5][1] + square_size * 3), (rooms[5][0], rooms[5][1] + square_size * 5)),
    ((rooms[5][0], rooms[5][1] + square_size * 5), (rooms[5][0] + square_size * 7, rooms[5][1] + square_size * 5)),
    # 방 6번
    ((rooms[6][0], rooms[6][1]), (rooms[6][0] , rooms[6][1] + square_size * 1)),
    ((rooms[6][0] , rooms[6][1] + square_size * 2), (rooms[6][0] , rooms[6][1] + square_size * 7)),
    ((rooms[6][0] , rooms[6][1] + square_size * 6), (rooms[6][0] + square_size * 6, rooms[6][1] + square_size * 6)),
    # 방 7번 (바깥) 구현
    ((rooms[8][0], rooms[8][1]), (rooms[8][0], rooms[8][1] + square_size * 4)),
    ((rooms[8][0], rooms[8][1]), (rooms[8][0] + square_size * 2, rooms[8][1])),
    ((rooms[8][0] + square_size * 2, rooms[8][1]), (rooms[7][0], rooms[7][1])),
    ((rooms[7][0], rooms[7][1]), (rooms[7][0] + square_size * 1, rooms[7][1])),
    ((rooms[7][0] + square_size * 3, rooms[7][1]), (rooms[7][0] + square_size * 4, rooms[7][1])),
    ((rooms[9][0], rooms[9][1]), (rooms[9][0], rooms[9][1] + square_size * 1)),
    ((rooms[9][0], rooms[9][1]), (rooms[9][0] + square_size * 2, rooms[9][1])),
    # 방 8번
    ((rooms[10][0], rooms[10][1]), (rooms[10][0], rooms[10][1] + square_size * 6)),
    ((rooms[10][0], rooms[10][1]), (rooms[10][0] + square_size * 5, rooms[10][1])),
    ((rooms[10][0] + square_size * 5, rooms[10][1] - square_size * 2), (rooms[10][0] + square_size * 5, rooms[10][1] + square_size * 1)),
    # 방 9번
    ((rooms[11][0], rooms[11][1]), (rooms[11][0], rooms[11][1] + square_size * 6)),
    ((rooms[11][0] + square_size * 5, rooms[11][1]), (rooms[11][0] + square_size * 5, rooms[11][1] + square_size * 3)),
    # 시작점 방
    ((rooms[12][0], rooms[12][1]), (rooms[12][0], rooms[12][1] + square_size * 1)),
    ((rooms[12][0], rooms[12][1] + square_size * 2), (rooms[12][0], rooms[12][1] + square_size * 3)),
    ((rooms[12][0], rooms[12][1] + square_size * 3), (rooms[12][0] + square_size * 2, rooms[12][1] + square_size * 3)),
    ((rooms[12][0] + square_size * 3, rooms[12][1] + square_size * 3), (rooms[12][0] + square_size * 4, rooms[12][1] + square_size * 3)),
    ((rooms[12][0], rooms[12][1]), (rooms[12][0] + square_size * 2, rooms[12][1])),
    ((rooms[12][0] + square_size * 3, rooms[12][1]), (rooms[12][0] + square_size * 4, rooms[12][1])),
    ((rooms[12][0] + square_size * 4, rooms[12][1]), (rooms[12][0] + square_size * 4, rooms[12][1] + square_size * 1)),
    ((rooms[12][0] + square_size * 4, rooms[12][1] + square_size * 2), (rooms[12][0] + square_size * 4, rooms[12][1] + square_size * 3))
    # 필요한 만큼 방 벽을 추가
]

grid = set() # 그리드 설정
for room in rooms: # 방을 그리드에 추가
    room = pygame.Rect(*room)
    for x in range(room.left, room.right, square_size):
        for y in range(room.top, room.bottom, square_size): grid.add((x, y))

for x in range(wall_position.left, wall_position.right, square_size): # 벽 안에 그리드 추가
    for y in range(wall_position.top, wall_position.bottom, square_size):
        rect = pygame.Rect(x, y, square_size, square_size)
        if (x, y) in grid: pygame.draw.rect(window, background_color, rect) # 배경색으로 그리드를 그림
        else: pygame.draw.rect(window, grid_color, rect, 1) # 그리드 색상으로 그리드를 그림

pygame.draw.rect(window, wall_color, wall_position, 2) # 벽 그리기

for wall in room_walls: # 방 벽 그리기
    pygame.draw.line(window, wall_color, wall[0], wall[1], 2) # 각 방 벽에 대해

# 방의 위치에 방 이름을 표시
font = pygame.font.SysFont('malgungothic', 15)
room_names = locations.copy() # 복사
room_names.insert(1, "") # 이름 빈 방
room_names.insert(8, "") # 이름 빈 방
room_names.insert(9, "") # 이름 빈 방
room_names.insert(12, "시작점") # 시작점 방
if len(rooms) >= len(room_names): # 방의 수가 방 이름의 수보다 많거나 같은 경우
     for i, room in enumerate(rooms): # 각 방에 대해 
        print("room : ", room, i, room_names[i]) # 방 위치, 방 이름 출력
        text = font.render(room_names[i], True, wall_color) # 방 이름 생성
        window.blit(text, (room[0] + 5, room[1] + 5)) # 방 이름 표시

player_size = 12 # 플레이어 크기
loc = (square_size - player_size) / 2 # 플레이어 위치

# 플레이어
player1_position = (rooms[12][0] + loc, rooms[12][1] + loc)
player1 = {"position": player1_position, "color": suspects["피콕"], "name": list(suspects.keys())[0]}
player2_position = (rooms[12][0] + loc + square_size * 3, rooms[12][1] + loc)
player2 = {"position": player2_position, "color": suspects["플럼"], "name": list(suspects.keys())[1]}
player3_position = (rooms[12][0] + loc, rooms[12][1] + square_size * 2 + loc)
player3 = {"position": player3_position, "color": suspects["스칼렛"], "name": list(suspects.keys())[2]}
player4_position = (rooms[12][0] + loc + square_size * 3, rooms[12][1] + square_size * 2 + loc)
player4 = {"position": player4_position, "color": suspects["머스타드"], "name": list(suspects.keys())[3]}

# 기존 플레이어 그리기
pygame.draw.rect(window, suspects["피콕"], pygame.Rect(player1_position[0], player1_position[1], player_size, player_size))
pygame.draw.rect(window, suspects["플럼"], pygame.Rect(player2_position[0], player2_position[1], player_size, player_size))
pygame.draw.rect(window, suspects["스칼렛"], pygame.Rect(player3_position[0], player3_position[1], player_size, player_size))
pygame.draw.rect(window, suspects["머스타드"], pygame.Rect(player4_position[0], player4_position[1], player_size, player_size))
print("player1 : ", player1)
print("player2 : ", player2)
print("player3 : ", player3)
print("player4 : ", player4)

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

num_cards = 4  # 각 플레이어에게 나눠줄 카드의 수
all_cards = list(su) + list(weapons) + list(locations)  # 모든 카드를 합칩니다.
random.shuffle(all_cards)  # 카드를 섞습니다.

# 각 플레이어에게 카드를 나눠줍니다.
player1_cards = all_cards[:num_cards]
player2_cards = all_cards[num_cards:num_cards * 2]
player3_cards = all_cards[num_cards * 2:num_cards * 3]
player4_cards = all_cards[num_cards * 3:num_cards * 4]
last_cards = all_cards[num_cards * 4:] #남은카드
print("all_cards : ", all_cards)
print("player1_cards : ", player1_cards)
print("player2_cards : ", player2_cards)
print("player3_cards : ", player3_cards)
print("player4_cards : ", player4_cards)
print("last_cards : ", last_cards) # 남은 카드
print("bonus_cards_list : ", bonus_cards_list) # 보너스 카드
print("case envelope : ", case_envelope) # 사건봉투

# 카드를 그리기 위한 설정
border_color = (0, 0, 0)  # 검은색

border_thickness = 2  # 테두리의 두께
font = pygame.font.SysFont('malgungothic', 15) # 폰트 설정
card_width, card_height = 100, 50  # 카드의 크기 설정
card_position = (window_size[0] / 2 + square_size * 2, window_size [1] / 2 - square_size * 10, card_width, card_height)  # 카드의 위치 설정

# 각 플레이어의 카드를 그리기
for i, card in enumerate(player1_cards): # 플레이어 1의 카드를 그립니다.
    pygame.draw.rect(window, border_color, (card_position[0] + i * card_width, card_position[1], card_width, card_height), border_thickness)
    text = font.render(card, True, wall_color)
    text_rect = text.get_rect(center=((card_position[0] * 2 + card_width) / 2 + i * card_width, card_position[1] + card_height / 2))
    window.blit(text, text_rect)

for i, card in enumerate(player2_cards): # 플레이어 2의 카드를 그립니다.
    pygame.draw.rect(window, border_color, (card_position[0] + i * card_width, card_position[1] + card_height, card_width, card_height), border_thickness)
    text = font.render(card, True, wall_color)
    text_rect = text.get_rect(center=((card_position[0] * 2 + card_width) / 2 + i * card_width, card_position[1] + card_height * 3 / 2))
    window.blit(text, text_rect)

for i, card in enumerate(player3_cards): # 플레이어 3의 카드를 그립니다.
    pygame.draw.rect(window, border_color, (card_position[0] + i * card_width, card_position[1] + card_height * 2, card_width, card_height), border_thickness)
    text = font.render(card, True, wall_color)
    text_rect = text.get_rect(center=((card_position[0] * 2 + card_width) / 2 + i * card_width, card_position[1] + card_height * 5 / 2))
    window.blit(text, text_rect)

for i, card in enumerate(player4_cards): # 플레이어 4의 카드를 그립니다.
    pygame.draw.rect(window, border_color, (card_position[0] + i * card_width, card_position[1] + card_height * 3, card_width, card_height), border_thickness)
    text = font.render(card, True, wall_color)
    text_rect = text.get_rect(center=((card_position[0] * 2 + card_width) / 2 + i * card_width, card_position[1] + card_height * 7 / 2))
    window.blit(text, text_rect)

for i, card in enumerate(all_cards[num_cards * 4:]): # 남은 카드를 그립니다.
    pygame.draw.rect(window, border_color, (card_position[0] + i * card_width, card_position[1] + card_height * 4, card_width, card_height), border_thickness)
    text = font.render(card, True, wall_color)
    text_rect = text.get_rect(center=((card_position[0] * 2 + card_width) / 2 + i * card_width, card_position[1] + card_height * 9 / 2))
    window.blit(text, text_rect)

for i, card in enumerate(bonus_cards_list): # 보너스 카드를 그립니다.
    pygame.draw.rect(window, border_color, (card_position[0] + (i if i < 4 else (i-4 if i < 8 else (i-8 if i < 12 else i - 12))) * card_width, card_position[1] + card_height * (5 if i < 4 else (6 if i < 8 else (7 if i < 12 else 8))), card_width, card_height), border_thickness)
    text = font.render(card[:5] + "...", True, wall_color)
    text_rect = text.get_rect(center=((card_position[0] * 2 + card_width) / 2 + (i if i < 4 else (i-4 if i < 8 else (i-8 if i < 12 else i - 12))) * card_width, card_position[1] + (card_height * (11 if i < 4 else (13 if i < 8 else (15 if i < 12 else 17))) / 2)))
    window.blit(text, text_rect)

for i, card in enumerate(case_envelope): # 사건봉투 카드를 그립니다.
    pygame.draw.rect(window, border_color, (card_position[0] + i * card_width, card_position[1] + card_height * 9, card_width, card_height), border_thickness)
    text = font.render("\'"+case_envelope[card]+"\'", True, wall_color)
    text_rect = text.get_rect(center=((card_position[0] * 2 + card_width) / 2 + i * card_width, card_position[1] + card_height * 19 / 2))
    window.blit(text, text_rect)

pygame.display.flip() # 창 업데이트

running = True
while running: # 게임이 실행 중인 동안
    for event in pygame.event.get(): # 각 이벤트에 대해
        if event.type == pygame.QUIT: # 종료 이벤트인 경우
            running = False 

pygame.quit() # pygame 종료