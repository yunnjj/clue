import pygame
import random

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
        ((rooms[0][0], rooms[0][1]), (rooms[0][0] + square_size * 6, rooms[0][1])),
        ((rooms[0][0] + square_size * 6, rooms[0][1]), (rooms[0][0] + square_size * 6, rooms[0][1] + square_size)),
        ((rooms[0][0] + square_size * 6, rooms[0][1] + square_size * 2), (rooms[0][0] + square_size * 6, rooms[0][1] + square_size * 3)),
        ((rooms[0][0] + square_size * 6, rooms[0][1] + square_size * 4), (rooms[0][0] + square_size * 6 + square_size, rooms[0][1] + square_size * 4)),
        ((rooms[0][0] + square_size * 7, rooms[0][1] + square_size * 4), (rooms[0][0] + square_size * 6 + rooms[1][2], rooms[0][1] + square_size * 6)),
        ((rooms[0][0] + square_size * 7, rooms[0][1] + square_size * 6), (rooms[0][0], rooms[0][1] + square_size * 6)),
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

def draw_card(window, font, border_color, thickness, wall_color, card_position, card_width, card_height, square_size, cards, start_height): # 카드를 그리기 위한 함수
    for i, card in enumerate(cards):
        print("current :", i, card)
        row = i // 4
        col = i % 4
        x = card_position[0] + col * (card_width + square_size // 2)
        y = card_position[1] + row * (card_height + square_size // 4) + start_height * (card_height + square_size // 4)
        pygame.draw.rect(window, border_color, (x, y, card_width, card_height), thickness)   
        if len(card) > 5: card = card[:5] + "..." # 카드 이름이 5글자를 넘어가면 ...으로 표시
        text = font.render(card, True, wall_color)
        text_rect = text.get_rect(center=(x + card_width / 2, y + card_height / 2))
        window.blit(text, text_rect)
def add_rooms_to_grid(rooms, square_size, grid): # 방을 그리드에 추가하는 함수
    for room in rooms: 
        room = pygame.Rect(*room)
        for x in range(room.left, room.right, square_size):
            for y in range(room.top, room.bottom, square_size):
                grid.add((x, y))
def add_walls_to_grid(wall_position, square_size, grid, window, background_color, grid_color, thickness): # 벽을 그리드에 추가하는 함수
    for x in range(wall_position.left, wall_position.right, square_size):
        for y in range(wall_position.top, wall_position.bottom, square_size):
            rect = pygame.Rect(x, y, square_size, square_size)
            if (x, y) in grid: 
                pygame.draw.rect(window, background_color, rect)
            else: 
                pygame.draw.rect(window, grid_color, rect, thickness // 2)
def draw_wall(window, wall_color, wall_position, thickness): # 벽 그리기
    pygame.draw.rect(window, wall_color, wall_position, thickness) 
def draw_room_walls(window, wall_color, room_walls, thickness): # 방 벽 그리기
    for wall in room_walls:
        pygame.draw.line(window, wall_color, wall[0], wall[1], thickness) # 각 방 벽에 대해
def draw_room_names(window, font, wall_color, square_size, rooms, room_names): # 방 이름 그리기
    if len(rooms) >= len(room_names): # 방의 수가 방 이름의 수보다 많거나 같은 경우
        for i, room in enumerate(rooms): # 각 방에 대해 
            text = font.render(room_names[i], True, wall_color) # 방 이름 생성
            window.blit(text, (room[0] + square_size / 5, room[1] + square_size / 5)) # 방 이름 표시
def create_and_draw_player(window, suspects, rooms, square_size, player_size, loc, player_index): # 플레이어 생성 및 그리기
    player = (list(suspects.keys())[player_index], pygame.Rect(rooms[12][0] + loc + square_size * 3 * (player_index % 2), rooms[12][1] + square_size * 2 * (player_index // 2) + loc, player_size, player_size))
    pygame.draw.rect(window, suspects[player[0]], player[1])
    return player
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
    player1_cards = all_cards[:num_cards]
    player2_cards = all_cards[num_cards:num_cards * 2]
    player3_cards = all_cards[num_cards * 2:num_cards * 3]
    player4_cards = all_cards[num_cards * 3:num_cards * 4]
    last_cards = all_cards[num_cards * 4:] #남은카드

    return case_envelope, player1_cards, player2_cards, player3_cards, player4_cards, last_cards

def main():
    pygame.init() # pygame 초기화 
    
    grid = set() # 그리드 설정
    add_rooms_to_grid(rooms, square_size, grid) # 방을 그리드에 추가
    add_walls_to_grid(wall_position, square_size, grid, window, background_color, grid_color, thickness) # 벽을 그리드에 추가
    draw_wall(window, wall_color, wall_position, thickness) # 벽 그리기
    draw_room_walls(window, wall_color, room_walls, thickness) # 방 벽 그리기

    # 방의 위치에 방 이름을 표시
    font = pygame.font.SysFont('malgungothic', square_size * 2 // 3)
    room_names = locations.copy() # 복사
    room_names.insert(1, "") # 이름 빈 방
    room_names.insert(8, "") # 이름 빈 방
    room_names.insert(9, "") # 이름 빈 방
    room_names.insert(12, "시작점") # 시작점 방
    draw_room_names(window, font, wall_color, square_size, rooms, room_names) # 방 이름 그리기

    # 카드 섞고 나눠주기
    num_cards = 4  # 각 플레이어에게 나눠줄 카드의 수 : 4명이므로 4장
    case_envelope, player1_cards, player2_cards, player3_cards, player4_cards, all_cards = shuffle_and_distribute_cards(suspects, weapons, locations, num_cards)

    # 플레이어 생성 및 그리기
    player_size = 12 # 플레이어 크기
    loc = (square_size - player_size) / 2 # 플레이어 위치
    player1 = create_and_draw_player(window, suspects, rooms, square_size, player_size, loc, 0)
    player2 = create_and_draw_player(window, suspects, rooms, square_size, player_size, loc, 1)
    player3 = create_and_draw_player(window, suspects, rooms, square_size, player_size, loc, 2)
    player4 = create_and_draw_player(window, suspects, rooms, square_size, player_size, loc, 3)
    
    # 카드 그리기
    card_position = wall_position[0] + wall_position[2] + 1 * square_size, wall_position[1] + -1 * square_size
    card_width = square_size * 4 # 카드 너비
    card_height = square_size * 2 # 카드 높이
    border_color = wall_color
    border_thickness = thickness
    draw_card(window, font, border_color, border_thickness, wall_color, card_position, card_width, card_height, square_size, player1_cards, 0)
    draw_card(window, font, border_color, border_thickness, wall_color, card_position, card_width, card_height, square_size, player2_cards, 1)
    draw_card(window, font, border_color, border_thickness, wall_color, card_position, card_width, card_height, square_size, player3_cards, 2)
    draw_card(window, font, border_color, border_thickness, wall_color, card_position, card_width, card_height, square_size, player4_cards, 3)
    draw_card(window, font, border_color, border_thickness, wall_color, card_position, card_width, card_height, square_size, all_cards, 4)
    draw_card(window, font, border_color, border_thickness, wall_color, card_position, card_width, card_height, square_size, bonus_cards_list, 5)
    draw_card(window, font, border_color, border_thickness, wall_color, card_position, card_width, card_height, square_size, list(case_envelope.values()), 9)
   
    pygame.display.flip() # 창 업데이트

    running = True
    while running: # 게임이 실행 중인 동안
        for event in pygame.event.get(): # 각 이벤트에 대해
            if event.type == pygame.QUIT: # 종료 이벤트인 경우
                running = False  

    pygame.quit() # pygame 종료

if __name__ == "__main__":
    main() # 메인 함수 실행








    