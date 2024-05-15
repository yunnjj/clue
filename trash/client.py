# client.py
import pygame
import socket
import threading


# 서버 주소와 포트 설정
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8000

# 클라이언트 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
    print("서버에 연결되었습니다.")
except socket.error as e:
    print(f"서버에 연결할 수 없습니다: {e}")
    exit()

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
GRAY = (200, 200, 200)
ROOM_NAME = ["침실", "욕실", "서제", "부엌", "식당", "거실", "마당", "차고", "게임룸"]
ROOM_SIZE = [(6, 6), (1, 2), (4, 4), (4, 5), (6, 6), (7, 5), (6, 6), (4, 3), (2, 4), (2, 4), (5, 6), (5, 6), (4, 3)] # 방의 크기 설정
ROOM_POS = [(0, 2), (6, 6), (6, 0), (10, 1), (14, 2), (13, 8), (14, 13), (8, 17), (6, 16), (12, 16), (1, 14), (1, 8), (8, 10) ]
ROOM_WALL_POS = [((0, 2), (6, 2)), ((6, 0), (6, 3)), ((6, 4), (6, 5)), ((6, 6), (7, 6)),((7, 6), (7, 8)), ((7, 8), (0, 8)),
        ((10, 0), (10, 4)), ((10, 4), (9, 4)), ((8, 4), (6, 4)), 
        ((10, 1), (14, 1)), ((14, 1), (14, 6)), ((14, 6), (9, 6)), ((10, 6), (10, 5)),
        ((9, 6), (9, 8)), ((14, 2), (20, 2)), ((20, 8), (18, 8)), ((16, 8), (13, 8)), ((14, 7), (14, 8)),
        ((13, 8), (13, 10)), ((13, 11), (13, 13)), ((13, 13), (20, 13)),
        ((14, 13), (14, 14)), ((14, 15), (14, 20)), ((14, 19), (20, 19)),
        ((6, 20), (6, 16)), ((6, 16), (8, 16)), ((8, 16), (8, 17)), ((8, 17), (9, 17)), ((11, 17), (12, 17)), ((12, 17), (12, 16)), ((12, 16), (14, 16)),
        ((1, 8), (1, 20)), ((1, 14), (6, 14)), ((6, 15), (6, 12)), # 방 8번
        ((6, 8), (6, 11)), ((8, 10), (10, 10)), ((11, 10), (12, 10)), ((12, 10), (12, 11)), ((12, 12), (12, 13)), ((12, 13), (11, 13)), ((10, 13), (8, 13)), ((8, 13), (8, 12)),
        ((8, 11), (8, 10)), # 시작점 방
]

square_size = 30
window_size = (square_size * 40, square_size * 24) # 창 크기 설정
player_size = square_size // 5
thickness = 2
wall_position = (square_size, square_size, square_size * 20, square_size * 20)
room_names = ROOM_NAME
room_names.insert(1, "") # 이름 빈 방
room_names.insert(8, "") # 이름 빈 방
room_names.insert(9, "") # 이름 빈 방
room_names.insert(12, "시작장소") # 시작 장소
rooms = [(wall_position[0] + x * square_size, wall_position[1] + y * square_size, w * square_size, h * square_size) for (x, y), (w, h) in zip(ROOM_POS, ROOM_SIZE)] # 방의 위치와 크기를 결합
room_walls = [((x[0][0]*square_size + wall_position[0], x[0][1]*square_size + wall_position[1]), # 방 벽 설정
                (x[1][0]*square_size + wall_position[0], x[1][1]*square_size + wall_position[1])) for x in ROOM_WALL_POS]
room_shortcut_location = ((0, 2), (14, 2), (5, 19), (14, 18)) # 방의 통로 위치 설정
grid_bonus_location = ((8, 5), (10, 6), (9, 13), (12, 12), (11, 15)) # 보너스카드 위치 설정
grid_bonus = [(wall_position[0] + x * square_size, wall_position[1] + y * square_size) for x, y in grid_bonus_location] #`grid_bonus_location` 위치에 보너스카드 추가
card_position = (wall_position[0] + wall_position[2] + 1 * square_size, wall_position[1], 4 * square_size, 5 * square_size) # 카드 위치 설정
button_position = (wall_position[0] + 21 * square_size, wall_position[1] + 18 * square_size, 4 * square_size, 2 * square_size) # 버튼 위치 설정

# pygame 초기화
pygame.init()

def add_rooms_to_grid(rooms, square_size, grid): # 방을 그리드에 추가하는 함수
    for room in rooms: # 각 방에 대해
        room = pygame.Rect(*room) # 방의 위치 및 크기를 가져옵니다.
        for x in range(room.left, room.right, square_size): # 방의 좌우 범위에 대해
            for y in range(room.top, room.bottom, square_size): grid.add((x, y)) # 방의 각 좌표를 그리드에 추가

def add_walls_to_grid(wall_position, square_size, grid, window, background_color, grid_color, thickness): # 벽을 그리드에 추가하는 함수
    font = pygame.font.Font(None, square_size) # 폰트 객체 생성
    question_mark = font.render("?", True, RED) # "?" 문자를 Surface 객체로 변환
    for x in range(wall_position[0], wall_position[2] + 1, square_size): # 벽의 각 좌표에 대해
        for y in range(wall_position[1], wall_position[3] + 1, square_size): # 벽의 각 좌표에 대해
            rect = pygame.Rect(x, y, square_size, square_size) # 사각형 생성
            if (x, y) in grid: pygame.draw.rect(window, background_color, rect) # 그리드에 있는 경우 배경색으로 채우기
            else: # 그리드에 없는 경우
                if (rect[0], rect[1]) in grid_bonus: # 보너스카드 위치에 있는 경우
                    pygame.draw.rect(window, WHITE, rect) # 보너스카드 위치에 연한 빨간색으로 채우기
                    text_rect = question_mark.get_rect(center=(rect[0] + square_size // 2, rect[1] + 1 + square_size // 2)) # "?" 표시의 중심 위치 설정
                    window.blit(question_mark, text_rect) # 보너스카드 위치에 "?" 표시
                pygame.draw.rect(window, grid_color, rect, thickness // 2) # 그리드에 없는 경우 그리드 색상으로 선 그리기
    pygame.display.update()

def draw_wall(window, wall_color, wall_position, thickness): # 벽 그리기
    pygame.draw.rect(window, wall_color, wall_position, thickness)
    pygame.display.update()

def draw_room_walls(window, wall_color, room_walls, thickness): # 방 벽 그리기
    for wall in room_walls: pygame.draw.line(window, wall_color, wall[0], wall[1], thickness) # 각 방 벽에 대해 선 그리기
    pygame.display.update()

def draw_room_names(window, font, square_size, rooms, room_names): # 방 이름 그리기
    if len(rooms) >= len(room_names): # 방의 수가 방 이름의 수보다 많거나 같은 경우
        for i, room in enumerate(rooms): # 각 방에 대해
            font = pygame.font.SysFont('malgungothic', square_size * 2 // 3) # 폰트 설정
            text = font.render(room_names[i], True, GRAY) # 방 이름을 Surface 객체로 변환
            text_rect = text.get_rect(center=(room[0] + room[2] // 2, room[1] + room[3] // 2)) # 방 이름의 중심 위치 설정
            window.blit(text, text_rect) # 방 이름 표시
    pygame.display.update()

def draw_cards(window, font, card_position, cards = " , , , "): # 카드 그리기
    font = pygame.font.SysFont('malgungothic', square_size // 7 * 5) # 폰트 설정
    cards = cards.split(",") # 카드를 쉼표로 분리
    for i, card in enumerate(cards): # 각 카드에 대해
        pygame.draw.rect(window, WHITE, (card_position[0] + i * (card_position[2] + square_size / 2), card_position[1], card_position[2], card_position[3])) # 카드의 배경색 설정
        pygame.draw.rect(window, BLACK, (card_position[0] + i * (card_position[2] + square_size / 2), card_position[1], card_position[2], card_position[3]), thickness) # 카드의 외곽선 그리기
        text = font.render(card, True, BLACK)
        text_rect = text.get_rect(center=(card_position[0] + i * (card_position[2] + square_size / 2) + card_position[2] // 2, card_position[1] + card_position[3] // 2))
        window.blit(text, text_rect)
    pygame.display.update()

def draw_button(window, color, position, text, font, thickness): # 버튼 그리기
    font = pygame.font.SysFont('malgungothic', square_size // 2) # 폰트 설정
    pygame.draw.rect(window, color, position, thickness)
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(position[0] + position[2] // 2, position[1] + position[3] // 2))
    window.blit(text, text_rect)
    pygame.display.update()

def draw_dice(window, dice1 = 0, dice2 = 0): # 주사위 그리기
    dice1_position = wall_position[0] + 21 * square_size, wall_position[1] + 15 * square_size, 2 * square_size, 2 * square_size # 주사위 위치 및 크기 설정
    dice2_position = wall_position[0] + 24 * square_size, wall_position[1] + 15 * square_size, 2 * square_size, 2 * square_size # 주사위 위치 및 크기 설정
    pygame.draw.rect(window, WHITE, dice1_position) # 주사위 1의 배경색 설정
    pygame.draw.rect(window, WHITE, dice2_position) # 주사위 2의 배경색 설정
    pygame.draw.rect(window, BLACK, dice1_position, thickness) # 주사위 1의 외곽선 그리기
    pygame.draw.rect(window, BLACK, dice2_position, thickness) # 주사위 2의 외곽선 그리기
    dice_font = pygame.font.SysFont('malgungothic', square_size) # 주사위 폰트 설정
    dice1_text = dice_font.render(str(dice1), True, BLACK) # 주사위 1의 결과
    dice2_text = dice_font.render(str(dice2), True, BLACK) # 주사위 2의 결과
    window.blit(dice1_text, ((dice1_position[0] + square_size) - square_size / 4, (dice1_position[1] + square_size / 4))) # 주사위 1의 결과 표시
    window.blit(dice2_text, ((dice2_position[0] + square_size) - square_size / 4, (dice2_position[1] + square_size / 4))) # 주사위 2의 결과 표시
    pygame.display.update()

def create_player(square_size, player_size, player_name, loc): # 플레이어 생성
    print(player_name, "위치:", loc)
    x, y = (wall_position[0] + loc[0] * square_size) + (square_size - player_size) // 2, (wall_position[1] + loc[1] * square_size) + (square_size - player_size) // 2 # 플레이어의 위치 설정
    return x, y

def brighten_color(color, isBrigther): # 색상을 밝게 만드는 함수
    if isBrigther == True: # 밝은 모드인 경우
        brightened_color = [min(int(channel * 255 + 0.6 * 255), 255) for channel in color] # 각 색상 채널의 값을 증가시켜 색상을 밝게 만듭니다.
        return brightened_color # 밝은 색상을 반환합니다.
    else: return color

def draw_player(window, player, player_size, color, isBrigther): # 플레이어 그리기
    print("플레이어:", player[0], "위치:", player[1], "색상:", color)
    color = brighten_color(color, isBrigther) # 플레이어 색상 설정
    pygame.draw.rect(window, color, (player[0], player[1], player_size, player_size)) # 플레이어 그리기
    pygame.display.flip()
    return player

class Client:
    def __init__(self, client_socket):
        pygame.display.set_caption("클루 게임")
        self.window = pygame.display.set_mode(window_size)
        self.window.fill(WHITE)
        self.grid = set()
        self.client_socket = client_socket
        self.client_thread = ClientThread(client_socket, self)
        self.client_thread.start()
        add_rooms_to_grid(rooms, square_size, self.grid)
        add_walls_to_grid(wall_position, square_size, self.grid, self.window, WHITE, GRAY, thickness)
        draw_wall(self.window, BLACK, wall_position, thickness)
        draw_room_walls(self.window, BLACK, room_walls, thickness)
        draw_room_names(self.window, None, square_size, rooms, room_names)
        draw_cards(self.window, None, card_position)
        draw_button(self.window, BLACK, button_position, "주사위", None, thickness)
        draw_dice(self.window)
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if button_position[0] <= x <= button_position[0] + button_position[2] and button_position[1] <= y <= button_position[1] + button_position[3]: # 주사위 버튼을 클릭한 경우
                        self.client_socket.send("dice".encode()) # 주사위 정보를 서버에 전송
                        print("주사위 클릭")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        break

class ClientThread(threading.Thread):
    def __init__(self, client_socket, client):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client = client
        self.name = ""
        self.cards = ""

    def run(self):
        while True:
            received_data = self.client_socket.recv(1024)
            if received_data:
                message = received_data.decode()
                if "player_info" in message:
                    self.name, self.color, self.cards = message.split("|")[1].split(":")
                    print("플레이어 정보:", self.name, self.color, self.cards)
                    self.playerloc = create_player(square_size, player_size, self.name, (10, 10))
                    draw_player(self.client.window, self.playerloc, player_size, self.color, False)
                    draw_cards(self.client.window, None, card_position, self.cards)
                if "dice" in message:
                    dice1, dice2 = message.split(":")[1].split(",")
                    print("주사위 :", dice1, dice2)
                    draw_dice(client.window, int(dice1), int(dice2))

if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
    client = Client(client_socket)
    client.run()
    client_socket.close()
    print("연결 종료")