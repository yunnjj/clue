import pygame

# pygame 초기화
pygame.init()

# 창 크기 설정
window_size = (1000, 600)

# `window_size` 크기의 창 생성
window = pygame.display.set_mode(window_size)

# 창 제목 설정
pygame.display.set_caption("Map")

# 창 배경색 설정
background_color = (255, 255, 255)

# 창 배경색으로 채우기
window.fill(background_color)

# 크기 설정
square_size = 25  # 픽셀 크기의 정사각형

# 벽의 색상과 위치 설정
wall_color = (0, 0, 0)  # Black
wall_position = pygame.Rect(window_size[0] / 2 - square_size * 19 , window_size [1] / 2 - square_size * 10, 20 * square_size, 20 * square_size)  # x, y, width, height

# 그리드의 색상과 
grid_color = (200, 200, 200)  # Light gray

# 방의 위치와 크기 설정
rooms = [
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
    # 필요한 만큼 방을 추가
]

# 방의 벽 설정
room_walls = [
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

# 용의자: Peacock (Blue), Plum (Purple), Scarlet (Red), Mustard (Yellow), Green, White
suspects = {
    "Peacock": "Blue",
    "Plum": "Purple",
    "Scarlet": "Red",
    "Mustard": "Yellow",
    "Green": "Green",
    "White": "White"
}

# 무기: Candlestick, Dagger, Lead Pipe, Revolver, Rope, Wrench
weapons = {
    "Candlestick": "Candlestick",
    "Dagger": "Dagger",
    "Lead Pipe": "Lead Pipe",
    "Revolver": "Revolver",
    "Rope": "Rope",
    "Wrench": "Wrench"
}

# 방: ..

# 플레이어 크기 설정
player_size = 10

# 플레이어 위치 설정
loc = (square_size - player_size) / 2 # 플레이어 위치 조정
player_position = (rooms[12][0] + loc, rooms[12][1] + loc) # 시작 위치

# 플레이어 색상 설정
player_color = (0, 0, 255) # Blue


# 그리드 설정
grid = set()

# 방을 그리드에 추가
for room in rooms: # 각 방에 대해
    room = pygame.Rect(*room) # 방의 위치와 크기를 가져옴
    for x in range(room.left, room.right, square_size): # 방의 왼쪽부터 오른쪽까지
        for y in range(room.top, room.bottom, square_size): # 방의 위쪽부터 아래쪽까지
            grid.add((x, y)) # 그리드에 방을 추가
            print("room generated in : ", x, y)

# 벽 안에 그리드 추가
for x in range(wall_position.left, wall_position.right, square_size): # 벽의 왼쪽부터 오른쪽까지
    for y in range(wall_position.top, wall_position.bottom, square_size): # 벽의 위쪽부터 아래쪽까지
        rect = pygame.Rect(x, y, square_size, square_size) # 정사각형 생성
        if (x, y) in grid: # 그리드에 이미 있는 경우
            pygame.draw.rect(window, background_color, rect) # 배경색으로 채움
        else:
            pygame.draw.rect(window, grid_color, rect, 1) # 그리드 색상으로 그리드를 그림
            print("grid genereated in : ", x, y)

# 벽 그리기
pygame.draw.rect(window, wall_color, wall_position, 2) # 벽을 그림 

# 방 벽 그리기
for wall in room_walls: # 각 방 벽에 대해
    pygame.draw.line(window, wall_color, wall[0], wall[1], 2) # 방 벽을 그림

# 방의 위치에 방 이름을 표시
font = pygame.font.SysFont('malgungothic', 15) # 폰트 설정
room_names = ["침실", "", "욕실", "서제", "부엌", "식당", "거실", "마당", "", "", "차고", "게임룸", "시작점"]
if len(rooms) >= len(room_names):
     for i, room in enumerate(rooms): # 각 방에 대해
        text = font.render(room_names[i], True, wall_color) # 방 이름 생성
        window.blit(text, (room[0] + 5, room[1] + 5)) # 방 이름 표시

# 플레이어 그리기
player = pygame.Rect(player_position[0], player_position[1], player_size, player_size) # 플레이어 생성

# 플레이어 색상으로 플레이어를 그림
pygame.draw.rect(window, player_color, player)
print("player : ", player)

# 창 업데이트
pygame.display.flip() 

# 게임 루프
running = True
while running: # 게임이 실행 중인 동안
    for event in pygame.event.get(): # 각 이벤트에 대해
        if event.type == pygame.QUIT: # 종료 이벤트인 경우
            running = False 

# pygame 종료
pygame.quit()