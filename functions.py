import random # 랜덤 라이브러리 불러오기
import tkinter as tk # 티컨 라이브러리 불러오기
from tkinter import ttk # 테마 불러오기
from tkinter import messagebox as msg # 메시지 박스 불러오기
import ctypes # 윈도우 API 사용
import time # 시간 라이브러리 불러오기
import win32gui # 윈도우 API 사용
import threading # 스레드 라이브러리 불러오기
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QLabel, QCheckBox, QPushButton, QGridLayout, QMessageBox # PyQt5 라이브러리 불러오기
from PyQt5.QtGui import QFont # 폰트 불러오기
import sys # 시스템 라이브러리 불러오기
import os # 운영체제 라이브러리 불러오기

from package.setting import *

def shuffle_and_distribute_cards(): # 카드 섞고 나눠주기
    su = list(suspects.keys()) # 용의자 카드
    wp = list(weapons) # 도구 카드
    lo = list(locs.keys()) # 장소 카드
    random.shuffle(su) # 용의자 카드 섞기
    random.shuffle(wp) # 도구 카드 섞기
    random.shuffle(lo) # 장소 카드 섞기
    case_envelope = { # 사건봉투
        'suspect': su.pop(), # 용의자 카드
        'weapon': wp.pop(), # 도구 카드
        'location': lo.pop() # 장소 카드
    }
    all_cards = list(su) + list(wp) + list(lo)  # 모든 카드를 합칩니다.
    random.shuffle(all_cards)  # 카드를 섞습니다.
    player_cards = {} # 플레이어 카드를 저장할 딕셔너리 생성
    for i in range(0, PLAYER): # 4명의 플레이어에게 카드 나눠주기
        player_cards[list(suspects.keys())[i]] = all_cards[i * PLAYER : (i + 1) * PLAYER]
        print(list(suspects.keys())[i], "카드:", player_cards[list(suspects.keys())[i]]) # 플레이어 카드 출력
    last_cards = all_cards[PLAYER * PLAYER:] # 남은 카드
    print("사건봉투:", case_envelope, "남은 카드:", last_cards) # 사건봉투와 남은 카드 출력
    return case_envelope, player_cards, last_cards # 사건봉투, 플레이어 카드, 남은 카드 반환

def auto_close_msgbox(delay=2): # 메시지 박스 자동 닫기 함수
    time.sleep(delay)
    try: # try문을 사용하여 예외 처리
        win = win32gui.FindWindow(None, "알림") # 창을 찾습니다.
        ctypes.windll.user32.PostMessageA(win, 0x0010, 0, 0) # 창을 닫습니다.
    except Exception as e: print(e) # 예외 처리 

def show_message(title, message): # 메시지 표시 함수
    threading.Thread(target=auto_close_msgbox).start() # 자동 닫기 스레드 시작
    if title == "경고": # 경고
        msg.showwarning(title, message)
        return True
    elif title == "실패": # 실패
        msg.showerror(title, message)
        return True
    elif title == "예/아니오": # 예/아니오
        return msg.askyesno(title, message)
    else: # 알림, 취소
        msg.showinfo(title, message)
        return True
    
def brighten_color(color, isBrigther): # 색상을 밝게 만드는 함수
    if isBrigther == True: # 밝은 모드인 경우
        brightened_color = [min(int(channel * 255 + 0.6 * 255), 255) for channel in color] # 각 색상 채널의 값을 증가시켜 색상을 밝게 만듭니다.
        return brightened_color # 밝은 색상을 반환합니다.
    else: return color

def draw_card(cards, start_height, cur_player, case_envelope, lastShowing = False, Lose = False): # 카드 그리기
    small_font = pg.font.SysFont('malgungothic', 15)  # 작은 폰트 설정
    text1 = small_font.render("현재 플레이어", True, wall_color) # 현재 플레이어
    text1_rect = text1.get_rect(center=(card_pos[0] + card_width * 8, card_pos[1] +  3 * square_size)) # 현재 플레이어 위치 설정
    text2 = card_font.render(cur_player, True, suspects[cur_player]) # 플레이어 이름 설정
    text2_rect = text2.get_rect(center=(card_pos[0] + card_width * 8, text1_rect.bottom + text2.get_height() / 2)) # 플레이어 이름 위치 설정
    if suspects[cur_player] == YELLOW: # 현재 플레이어가 머스타드인 경우 (노랑색인 경우)
        text3 = card_font.render(cur_player, True, BLACK)  # 글씨 그림자 설정
        text3_rect = text3.get_rect(center=(card_pos[0] + card_width * 8 + 2, text1_rect.bottom + text3.get_height() / 2 + 2))
    
    p = [None] * PLAYER # 플레이어
    p_rect = [None] * PLAYER # 플레이어 위치
    for i in range(PLAYER): # 각 플레이어에 대해
        p[i] = small_font.render(list(suspects.keys())[i], True, suspects[list(suspects.keys())[i]] if cur_player == list(suspects.keys())[i] else wall_color)
        p_rect[i] = p[i].get_rect(center=(card_pos[0] + card_width * 8, card_pos[1] + (i-1) * square_size)) # 플레이어 위치 설정
    if lastShowing is False: # 아직 때가 아님
        for i in range(PLAYER): window.blit(p[i], p_rect[i]) # 플레이어 순서 출력
        window.blit(text1, text1_rect) # 플레이어 순서 출력
        if suspects[cur_player] == YELLOW: window.blit(text3, text3_rect)
        window.blit(text2, text2_rect) # 플레이어 이름 출력

    for i, card in enumerate(cards): # 각 카드에 대해
        row = i // 4
        col = i % 4 # 행 및 열 설정
        if lastShowing is not True:
            e_card_width, e_card_height = card_width * 2, card_height * 5
            e_card_font = pg.font.SysFont('malgungothic', square_size) # 폰트 설정
            x = card_pos[0] + col * (e_card_width + square_size // 2) # x 좌표 설정
            y = card_pos[1] + row * (e_card_height + square_size // 4) + start_height * (e_card_height + square_size // 4) # 시작 높이에 따라 y 좌표 설정
            if len(card) > 5: card = card[:5] + "..." # 카드 이름이 5글자를 넘어가면 ...으로 표시
            if card in case_envelope.values(): card = "???"
        else: # 승리/패배하고 사건 봉투를 열었을 때, 화면 가운데에 사건 봉투 세장 공개
            e_card_width, e_card_height = card_width * 4, card_height * 10
            e_card_font = pg.font.SysFont('malgungothic', square_size * 2) # 폰트 설정
            x = square_size * 15 / 2 + col * (e_card_width + square_size // 2) # x 좌표 설정
            y = square_size * 6 + row * (e_card_height + square_size // 4) + start_height * (e_card_height + square_size // 4) # 시작 높이에 따라 y 좌표 설정
        pg.draw.rect(window, brighten_color(WHITE, False), (x, y, e_card_width, e_card_height))
        pg.draw.rect(window, wall_color, (x, y, e_card_width, e_card_height), border_thickness) # 카드 테두리 그리기
        text = e_card_font.render(card, True, wall_color) # 카드 이름 설정
        text_rect = text.get_rect(center=(x + e_card_width / 2, y + e_card_height / 2)) # 텍스트 위치 설정
        window.blit(text, text_rect)
    if lastShowing is True:
        message = "승리하셨습니다!" if Lose is False else "패배하셨습니다!" # 승리/패배 메시지
        text_title = e_card_font.render(message, True, wall_color)
        text_title_rect = text_title.get_rect(center=(x - e_card_width / 2, y + e_card_height * 5 / 4))
        window.blit(text_title, text_title_rect)

def add_rooms_to_grid(grid): # 방을 그리드에 추가하는 함수
    for room in rooms: # 각 방에 대해
        room = pg.Rect(*room) # 방의 위치 및 크기를 가져옵니다.
        for x in range(room.left, room.right, square_size): # 방의 좌우 범위에 대해
            for y in range(room.top, room.bottom, square_size): grid.add((x, y)) # 방의 각 좌표를 그리드에 추가

def add_walls_to_grid(grid, grid_color, thickness): # 벽을 그리드에 추가하는 함수
    #font = pg.font.Font(None, square_size) # 폰트 객체 생성
    # question_mark = font.render("?", True, RED) # "?" 문자를 Surface 객체로 변환
    for x in range(wall_pos.left, wall_pos.right, square_size): # 벽의 각 좌표에 대해
        for y in range(wall_pos.top, wall_pos.bottom, square_size): # 벽의 각 좌표에 대해
            rect = pg.Rect(x, y, square_size, square_size) # 사각형 생성
            if (x, y) in grid: pg.draw.rect(window, LIGHT_GRAY, rect) # 그리드에 있는 경우 회색으로 채우기 
            else: # 그리드에 없는 경우
                # if (rect[0], rect[1]) in grid_bonus: # 보너스카드 위치에 있는 경우
                #     pg.draw.rect(window, brighten_color(RED, True), rect) # 보너스카드 위치에 연한 빨간색으로 채우기
                #     window.blit(question_mark, (rect[0] + square_size / 4, rect[1] + square_size / 4)) # 보너스카드 위치에 "?" 표시
                pg.draw.rect(window, grid_color, rect, thickness // 2) # 그리드에 없는 경우 그리드 색상으로 선 그리기

def draw_wall(thickness): # 벽 그리기
    pg.draw.rect(window, wall_color, wall_pos, thickness) 

def draw_room_walls(room_walls, thickness): # 방 벽 그리기
    for wall in room_walls: pg.draw.line(window, wall_color, wall[0], wall[1], thickness) # 각 방 벽에 대해 선 그리기

def draw_room_names(font): # 방 이름 그리기
    if len(rooms) >= len(room_names): # 방의 수가 방 이름의 수보다 많거나 같은 경우
        for i, room in enumerate(rooms): # 각 방에 대해
            text = font.render(room_names[i], True, DARK_GRAY) # 방 이름 설정
            text_rect = text.get_rect(center=(room[0] + square_size * (6 if len(room_names[i]) == 3 else 4) / 5, room[1] + square_size * 2 / 5))
            window.blit(text, text_rect)

def create_player(player_name, loc): # 플레이어 생성
    x, y = (loc[0] - 6) * square_size + (square_size - player_size) / 2 , (loc[1] - 6) * square_size + (square_size - player_size) / 2 # x 좌표 및 y 좌표 설정
    player = (player_name, pg.Rect(rooms[1][0] + x, rooms[1][1] + y, player_size, player_size))
    return player

def draw_player(player, isBrigther, soundPlay): # 플레이어 그리기
    color = brighten_color(suspects[player[0]], isBrigther) # 플레이어 색상 설정
    pg.draw.rect(window, color, player[1]) 
    pg.display.flip()
    if soundPlay is True: move_sound.play() # 이동하는 소리 재생
    return player

def create_and_draw_players(player_pos, soundPlay): # 플레이어 생성 및 그리기
    players = [create_player(player_name, loc) for player_name, loc in player_pos.items()] # 플레이어 생성
    for player in players: draw_player(player, False, soundPlay) # 플레이어 그리기

def roll_dice(): # 주사위 굴리기
    pg.display.flip() # 창 업데이트
    dice = random.randint(1, 6) # 주사위 굴리기
    return dice

def draw_dice(dice1, dice2): # 주사위 그리기
    dice1_pos = wall_pos[0] + 21 * square_size, wall_pos[1] + 17 * square_size, 2 * square_size, 2 * square_size # 주사위 위치 및 크기 설정
    dice2_pos = wall_pos[0] + 24 * square_size, wall_pos[1] + 17 * square_size, 2 * square_size, 2 * square_size # 주사위 위치 및 크기 설정
    pg.draw.rect(window, WHITE, dice1_pos) # 주사위 1의 배경색 설정
    pg.draw.rect(window, WHITE, dice2_pos) # 주사위 2의 배경색 설정
    pg.draw.rect(window, wall_color, dice1_pos, thickness) # 주사위 1의 외곽선 그리기
    pg.draw.rect(window, wall_color, dice2_pos, thickness) # 주사위 2의 외곽선 그리기
    dice_font = pg.font.SysFont('malgungothic', square_size) # 주사위 폰트 설정
    dice1_text = dice_font.render(str(dice1), True, wall_color) # 주사위 1의 결과
    dice2_text = dice_font.render(str(dice2), True, wall_color) # 주사위 2의 결과
    window.blit(dice1_text, ((dice1_pos[0] + square_size) - square_size / 4, (dice1_pos[1] + square_size / 4))) # 주사위 1의 결과 표시
    window.blit(dice2_text, ((dice2_pos[0] + square_size) - square_size / 4, (dice2_pos[1] + square_size / 4))) # 주사위 2의 결과 표시

def draw_btn(pos, text, font, thickness): # 버튼 그리기
    font = pg.font.SysFont('malgungothic', square_size // 2) # 폰트 설정
    pg.draw.rect(window, wall_color, pos, thickness) # 버튼 외곽선 그리기
    text = font.render(text, True, BLACK)
    text_rect = text.get_rect(center=(pos[0] + square_size * 2, pos[1] + square_size * 1))
    window.blit(text, text_rect)

def show_game_rules(): # 게임 규칙 표시
    show_game_rule_sound.play() # 게임 규칙 소리 재생
    gr_Location = os.getcwd() + "\\txt\\game_rule.txt" # 게임 규칙 파일 경로
    game_rule = open(gr_Location, "r", encoding="utf-8") # 게임 규칙 파일 열기
    app = QApplication(sys.argv) # 어플리케이션 생성

    window = QWidget() # 창 생성
    window.setWindowTitle("게임 규칙") # 창 제목 설정
    window.setFixedSize(900, 500) # 창 크기 설정 

    layout = QVBoxLayout() # 레이아웃 생성
    text = QTextEdit() # 텍스트 생성
    text.setReadOnly(True) # 텍스트 읽기 전용 설정
    text.setPlainText(game_rule.read()) # 텍스트 설정
    font = QFont("맑은 고딕", 12) # 폰트 설정
    text.setFont(font) # 폰트 설정
    layout.addWidget(text) # 레이아웃에 텍스트 추가
    button = QPushButton("닫기") # 버튼 생성
    button.clicked.connect(window.close) # 버튼 클릭 시 창 닫기 
    layout.addWidget(button) # 레이아웃에 버튼 추가

    window.setLayout(layout) # 창에 레이아웃 설정
    window.show() # 창 표시
    app.exec_() # 어플리케이션 실행

class ClueNotebook(QWidget):
    def __init__(self, player_name):
        super().__init__()
        self.player_name = player_name
        self.categories = {
            '누가?': ['그린', '머스타드', '피콕', '플럼', '스칼렛', '화이트'],
            '무엇으로?': ['렌치', '촛대', '단검', '권총', '파이프', '밧줄'],
            '어디에서?': ['욕실', '서재', '게임룸', '차고', '침실', '거실', '부엌', '마당', '식당']
        }
        self.notes = {category: [QCheckBox(item) for item in items] for category, items in self.categories.items()}
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(f"{self.player_name}'s Clue Notebook")
        layout = QVBoxLayout()

        for category, items in self.notes.items():
            layout.addWidget(QLabel(category))
            grid = QGridLayout()
            for row, checkbox in enumerate(items):
                grid.addWidget(checkbox, row // 3, row % 3)
            layout.addLayout(grid)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_notes)
        load_button = QPushButton('Load')
        load_button.clicked.connect(self.load_notes)
        layout.addWidget(save_button)
        layout.addWidget(load_button)

        self.setLayout(layout)

    def save_notes(self):
        try:
            with open(f"{self.player_name}_clue_notebook.txt", "w") as file:
                for category, items in self.notes.items():
                    file.write(f"{category}\n")
                    for checkbox in items:
                        file.write(f"{checkbox.text()}: {checkbox.isChecked()}\n")
            QMessageBox.information(self, "Saved", "Notebook saved successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred while saving: {e}")

    def load_notes(self):
        try:
            with open(f"{self.player_name}_clue_notebook.txt", "r") as file:
                current_category = None
                for line in file:
                    line = line.strip()
                    if line in self.categories:
                        current_category = line
                    elif current_category:
                        item, value = line.split(": ")
                        index = self.categories[current_category].index(item)
                        self.notes[current_category][index].setChecked(value == 'True')
            QMessageBox.information(self, "Loaded", "Notebook loaded successfully.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Warning", "No saved notebook found.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred while loading: {e}")

def show_clue_notes(player_name):
    players = ['Player 1', 'Player 2', 'Player 3', 'Player 4']
    app = QApplication(sys.argv)
    notebook = ClueNotebook(player_name)
    notebook.show()
    app.exec_()

def handle_dice_click(x, y, btn_pos): # 클릭한 위치 처리
    if btn_pos[0] <= x <= btn_pos[0] + btn_pos[2] and btn_pos[1] <= y <= btn_pos[1] + btn_pos[3]: # 버튼을 클릭한 경우
        roll_dice_sound.play() # 주사위 굴리는 소리 재생
        return True
    
def outStartRoom(new_pos, room, isOutStartRoom, cur_player): # 시작점 방을 나가는 경우
    room_x_start, room_y_start, width, height = room  # 방의 위치 및 크기 설정
    room_x_end = room_x_start + width # 방의 끝 위치 설정
    room_y_end = room_y_start + height # 방의 끝 위치 설정
    room_x_start, room_x_end = room_x_start / square_size - 1, room_x_end / square_size - 1 # 방의 시작 및 끝 위치 보정
    room_y_start, room_y_end = room_y_start / square_size - 2, room_y_end / square_size - 2 # 방의 시작 및 끝 위치 보정
    if (room_x_start <= (new_pos[0] + player_size / 20) <= room_x_end and room_y_start < (new_pos[1] + player_size / 20) 
        <= room_y_end and isOutStartRoom[cur_player]) is False: return False # 시작점 방을 나가지 않은 경우
    else: return True # 시작점 방을 나간 경우

def handle_room_entry(new_pos, cur_player, isOutStartRoom, other_players_pos, cur_room_loc, case_envelope): # 방에 들어가는 경우
    for room in rooms: # 각 방에 대해
        x_start, y_start, width, height = room # 방의 위치 및 크기
        x_end = x_start + width # 방의 끝 위치
        y_end = y_start + height # 방의 끝 위치
        x_start, x_end = x_start / square_size - 1, x_end / square_size - 1 # 방의 시작 및 끝 위치 보정
        y_start, y_end = y_start / square_size - 2, y_end / square_size - 2 # 방의 시작 및 끝 위치 보정
        if isOutStartRoom[cur_player] is True : # 시작점 방을 나간 경우
            if x_start <= (new_pos[0] + player_size / 20) <= x_end and y_start < (new_pos[1] + player_size / 20) <= y_end: # 방에 들어온 경우
                print(cur_player, "이/가", cur_room_loc[cur_player], "에서", room_names[rooms.index(room)], "방에 들어옴")
                enter_room_sound.play() # 방에 들어가는 소리 재생
                cur_room_loc[cur_player] = room_names[rooms.index(room)] # 현재 방 위치 설정
                while True: # 다른 플레이어가 있거나 방의 통로 위치인 경우
                    new_pos = (random.randint(int(x_start), int(x_end) - 1), random.randint(int(y_start), int(y_end) - 1))
                    if new_pos not in other_players_pos.values() and new_pos not in room_shortcut_pos: break
                if hasReasoned[cur_player] is True and cur_room_loc[cur_player] == "시작점": # 추리를 했고 시작점 방에 있는 경우
                    show_message("알림", "최종 추리를 실행합니다.")
                    if final_reasoning(cur_player, case_envelope) is False: 
                        isLosed[cur_player] = True
                        cur_room_loc[cur_player] = "바깥"
                        return 0, -1
    return new_pos

def do_dice_roll(previous_dice1, previous_dice2, dice1, dice2, player_pos): # 주사위 굴리기
    if previous_dice1 is None and previous_dice2 is None:  # 이전 주사위 결과가 없는 경우
        dice1 = roll_dice()  # 주사위를 굴립니다.
        dice2 = roll_dice()  # 주사위를 굴립니다.
    else: # 이전 주사위 결과가 있는 경우
        dice1 = previous_dice1  # 이전 주사위 결과를 사용합니다.
        dice2 = previous_dice2  # 이전 주사위 결과를 사용합니다.
        previous_dice1 = None  # 이전 주사위 결과를 초기화합니다.
        previous_dice2 = None  # 이전 주사위 결과를 초기화합니다.
    return player_pos, dice1, dice2, previous_dice1, previous_dice2

def move_player(cur_player, player_pos, dice1, dice2, other_players_poss, isOutStartRoom, cur_room_loc, case_envelope, player_cards) : # 플레이어 이동
    def exit_room(cur_player, new_pos, dice_roll): # 방을 나가는 경우
        print("방을 나감")
        cur_room_loc[cur_player] = "복도" # 현재 방 위치를 복도로 설정
        player_pos = new_pos # 플레이어 위치를 새로운 위치로 설정
        dice_roll -= 1 # 주사위 결과를 1 감소시킵니다.
        draw_player(create_player(cur_player, new_pos), True, True) # 플레이어 그리기
        exit_room_sound.play() # 방을 나가는 소리 재생
        return player_pos, dice_roll # 플레이어 위치 및 주사위 결과 반환
    reason = None # 이동 사유(추리), 이동하지 않고 추리만 했을때 이동하지 않은 경우 때문에 무한 루프에 빠지는 것을 방지하기 위해 추가
    new_poss = [player_pos]  # 이동한 모든 좌표를 저장하는 리스트
    new_pos = player_pos  # 새로운 위치
    old_pos = player_pos # 이전 위치
    dice_roll = dice1 + dice2 # 주사위 결과
    cur_dir = None # 현재 방향
    will_start_pos = 0,0 # 시작하는 위치
    player_room_loc = cur_room_loc[cur_player] # 현재 방 위치
    for room in rooms: # 각 방에 대해
        x_start, y_start, width, height = room # 방의 위치 및 크기
        x_end = x_start + width # 방의 끝 위치
        y_end = y_start + height # 방의 끝 위치
        x_start, x_end = x_start / square_size - 1, x_end / square_size - 1 # 방의 시작 및 끝 위치 보정
        y_start, y_end = y_start / square_size - 2, y_end / square_size - 2 # 방의 시작 및 끝 위치 보정
        if isOutStartRoom[cur_player] is True: # 시작점 방을 나간 경우
            if x_start <= (new_pos[0] + player_size / 20) <= x_end and y_start < (new_pos[1] + player_size / 20) <= y_end: # 방에 들어온 경우
                player_room_loc = room_names[rooms.index(room)] # 현재 방 위치 설정
    room_transitions = { # 방 사이 이동
        "부엌": {"next_room": "식당", "new_pos": (random.randint(13, 19), random.randint(8, 12))},
        "식당": {"next_room": "부엌", "new_pos": (random.randint(14, 19), random.randint(2, 7))},
        "침실": {"next_room": "욕실", "new_pos": (random.randint(6, 9), random.randint(0, 3))},
        "욕실": {"next_room": "침실", "new_pos": (random.randint(0, 5), random.randint(2, 7))}
    }
    print() # 줄바꿈
    print(cur_player, "차례, 현재 방 위치 :", player_room_loc) # 현재 방 위치 출력
    if new_pos == (0, -1): return player_pos, False # 이동하지 않은 경우
    if cur_room_loc[cur_player] != "복도": # 현재 방이 복도가 아닌 경우
        if isOutStartRoom[cur_player] is True and cur_room_loc[cur_player] == player_room_loc: # 시작점 방을 나갔고 현재 방이 그대로인 경우 (다른 방 이동을 위한)
            cur_room = cur_room_loc[cur_player] # 현재 방 설정
            if cur_room in room_transitions: # 현재 방이 방 사이 이동 목록에 있는 경우
                if show_message("예/아니오", "이 방에서 다른 방으로 이동하시겠습니까?"): # 다른 방으로 이동하는 경우
                    print("다른 방으로 이동할 수 있음")
                    cur_room_loc[cur_player] = room_transitions[cur_room]["next_room"] # 다음 방으로 이동
                    new_pos = room_transitions[cur_room]["new_pos"] # 새로운 위치 설정
                    while new_pos in other_players_poss.values(): # 다른 플레이어가 있는 경우
                        new_pos = room_transitions[cur_room]["new_pos"]
                        if new_pos not in other_players_poss.values(): break # 다른 플레이어가 없는 경우 이동
                    player_pos = new_pos # 플레이어 위치 설정
                    dice_roll = 0 # 주사위 결과 초기화
                    walking_sound.play() # 걷는 소리 재생
                else:  # 다른 방으로 이동하지 않는 경우
                    print("다른 방으로 이동하지 않음")
                    if show_message("예/아니오", "이 방에서 나가시겠습니까?"):
                        new_pos = room_door_pos[cur_room_loc[cur_player]] # 방의 문 위치로 이동
                        if new_pos in other_players_poss.values(): # 다른 플레이어가 있는 경우
                            if cur_room_loc[cur_player] == "마당": # 마당인 경우 (마당은 입구가 2칸 넓이)
                                if (10, 16) in other_players_poss.values() or (9, 16) in other_players_poss.values(): # 다른 플레이어가 있는 경우
                                    print("다른 플레이어가 막고 있음. 이동할 수 없는 위치", new_pos, other_players_poss)
                                    show_message("실패", "다른 플레이어가 가로막고 있습니다.\n이동할 수 없는 위치입니다.")
                                    dice_roll = 0 # 주사위 결과 초기화
                                else: player_pos, dice_roll = exit_room(cur_player, new_pos, dice_roll) # 방을 나가는 경우
                            else: # 마당이 아닌 경우
                                print("다른 플레이어가 막고 있음. 이동할 수 없는 위치", new_pos, other_players_poss)
                                show_message("실패", "다른 플레이어가 가로막고 있습니다.\n이동할 수 없는 위치입니다.")
                                dice_roll = 0  # 주사위 결과 초기화
                        else: player_pos, dice_roll = exit_room(cur_player, new_pos, dice_roll) # 방을 나가는 경우
                    else : # 취소, 방을 나가지 않는 경우
                        print("방을 나가지 않음")
                        dice_roll = 0 # 주사위 결과 초기화
                        if hasReasoned[cur_player] is True: # 한 방에서 연속으로 추리를 한 경우
                            print("한 방에서 연속으로 추리를 할 수 없음") 
                            show_message("경고", "한 방에서 연속으로 추리를 할 수 없습니다.")
                            return player_pos, False # 플레이어 위치 및 이동 여부 반환
            else: # 나가는 경우
                if show_message("예/아니오", "이 방에서 나가시겠습니까?"): # 방을 나가는 경우
                    new_pos = room_door_pos[cur_room_loc[cur_player]] # 방의 문 위치로 이동
                    if new_pos in other_players_poss.values(): # 다른 플레이어가 있는 경우
                        print("다른 플레이어가 막고 있음. 이동할 수 없는 위치", new_pos, other_players_poss)
                        show_message("실패", "다른 플레이어가 가로막고 있습니다.\n이동할 수 없는 위치입니다.")
                        dice_roll = 0 # 주사위 결과 초기화
                    else: player_pos, dice_roll = exit_room(cur_player, new_pos, dice_roll) # 방을 나가는 경우
                else: # 취소, 방을 나가지 않는 경우
                    print("방을 나가지 않음")
                    if hasReasoned[cur_player] is True: # 한 방에서 연속으로 추리를 한 경우
                        print("한 방에서 연속으로 추리를 할 수 없음")
                        show_message("경고", "한 방에서 연속으로 추리를 할 수 없습니다.")
                        return player_pos, False # 플레이어 위치 및 이동 여부 반환
                    dice_roll = 0

    if isOutStartRoom[cur_player] is False and cur_room_loc[cur_player] == "시작점": # 시작점 방에 나간적이 없고 현재 방이 시작점인 경우
        while True:
            event = pg.event.wait() # 이벤트 대기
            if event.type == pg.KEYDOWN: # 키를 누른 경우
                if event.key == pg.K_UP: # 위쪽 방향키를 누른 경우
                    pos = (int(start_room_door_pos[1][0] * square_size + wall_pos[0] + square_size / 2), 
                           int(start_room_door_pos[1][1] * square_size + wall_pos[1] + square_size / 2)) # 위치 설정
                    if (window.get_at(pos) == BLUE or window.get_at(pos) == RED or 
                        window.get_at(pos) == YELLOW or window.get_at(pos) == PURPLE): # 다른 플레이어가 있는 경우
                        print("다른 플레이어가 이미 있음. 이동할 수 없는 위치")
                        show_message("실패", "다른 플레이어가 있습니다.\n이동할 수 없는 위치입니다.")
                        continue
                    pg.draw.rect(window, WHITE, ((2 * will_start_pos[0] + square_size - player_size - 5) / 2, 
                        (2 * will_start_pos[1] + square_size - player_size - 5) / 2, player_size + 5, player_size + 5)) # 플레이어 이동 전 위치 하얀색으로 채우기
                    will_start_pos = wall_pos[0] + start_room_door_pos[1][0] * square_size, wall_pos[1] + start_room_door_pos[1][1] * square_size # 이동할 위치 설정
                    player_pos = start_room_door_pos[1]
                    draw_player(create_player(cur_player, start_room_door_pos[1]), True, True) # 플레이어 그리기
                elif event.key == pg.K_DOWN: # 아래쪽 방향키를 누른 경우
                    pos = (int(start_room_door_pos[3][0] * square_size + wall_pos[0] + square_size / 2), 
                           int(start_room_door_pos[3][1] * square_size + wall_pos[1] + square_size / 2)) # 위치 설정
                    if (window.get_at(pos) == BLUE or window.get_at(pos) == RED or 
                        window.get_at(pos) == YELLOW or window.get_at(pos) == PURPLE): # 다른 플레이어가 있는 경우 
                        print("다른 플레이어가 이미 있음. 이동할 수 없는 위치")
                        show_message("실패", "다른 플레이어가 있습니다.\n이동할 수 없는 위치입니다.")
                        continue
                    pg.draw.rect(window, WHITE, ((2 * will_start_pos[0] + square_size - player_size - 5) / 2, 
                        (2 * will_start_pos[1] + square_size - player_size - 5) / 2, player_size + 5, player_size + 5)) # 플레이어 이동 전 위치 하얀색으로 채우기
                    will_start_pos = wall_pos[0] + start_room_door_pos[3][0] * square_size, wall_pos[1] + start_room_door_pos[3][1] * square_size # 이동할 위치 설정
                    player_pos = start_room_door_pos[3]
                    draw_player(create_player(cur_player, start_room_door_pos[3]), True, True) # 플레이어 그리기
                elif event.key == pg.K_LEFT: # 왼쪽 방향키를 누른 경우
                    pos = (int(start_room_door_pos[0][0] * square_size + wall_pos[0] + square_size / 2), 
                           int(start_room_door_pos[0][1] * square_size + wall_pos[1] + square_size / 2)) # 위치 설정
                    if (window.get_at(pos) == BLUE or window.get_at(pos) == RED or 
                        window.get_at(pos) == YELLOW or window.get_at(pos) == PURPLE): # 다른 플레이어가 있는 경우
                        print("다른 플레이어가 이미 있음. 이동할 수 없는 위치")
                        show_message("실패", "다른 플레이어가 있습니다.\n이동할 수 없는 위치입니다.")
                        continue
                    pg.draw.rect(window, WHITE, ((2 * will_start_pos[0] + square_size - player_size - 5) / 2, 
                        (2 * will_start_pos[1] + square_size - player_size - 5) / 2, player_size + 5, player_size + 5)) # 플레이어 이동 전 위치 하얀색으로 채우기
                    will_start_pos = wall_pos[0] + start_room_door_pos[0][0] * square_size, wall_pos[1] + start_room_door_pos[0][1] * square_size # 이동할 위치 설정
                    player_pos = start_room_door_pos[0]
                    draw_player(create_player(cur_player, start_room_door_pos[0]), True, True) # 플레이어 그리기
                elif event.key == pg.K_RIGHT: # 오른쪽 방향키를 누른 경우
                    pos = (int(start_room_door_pos[2][0] * square_size + wall_pos[0] + square_size / 2), 
                           int(start_room_door_pos[2][1] * square_size + wall_pos[1] + square_size / 2)) # 위치 설정
                    if (window.get_at(pos) == BLUE or window.get_at(pos) == RED or 
                        window.get_at(pos) == YELLOW or window.get_at(pos) == PURPLE): # 다른 플레이어가 있는 경우
                        print("다른 플레이어가 이미 있음. 이동할 수 없는 위치")
                        show_message("실패", "다른 플레이어가 있습니다.\n이동할 수 없는 위치입니다.")
                        continue
                    pg.draw.rect(window, WHITE, ((2 * will_start_pos[0] + square_size - player_size - 5) / 2, 
                        (2 * will_start_pos[1] + square_size - player_size - 5) / 2, player_size + 5, player_size + 5)) # 플레이어 이동 전 위치 하얀색으로 채우기
                    will_start_pos = wall_pos[0] + start_room_door_pos[2][0] * square_size, wall_pos[1] + start_room_door_pos[2][1] * square_size # 이동할 위치 설정
                    player_pos = start_room_door_pos[2] 
                    draw_player(create_player(cur_player, start_room_door_pos[2]), True, True) # 플레이어 그리기
                elif event.key == pg.K_ESCAPE or event.type == pg.QUIT: exit() # 게임 종료
                elif event.key == pg.K_RETURN: # 엔터 키를 누른 경우
                    if will_start_pos == (0, 0): # 이동할 위치가 없는 경우
                        show_message("경고", "이동할 위치를 선택해주세요.")
                        print("경고, 이동할 위치를 선택")
                        continue # 다시 선택
                    print(cur_player, "이/가 이동을", will_start_pos, "에서 시작함") 
                    put_player_sound.play() # 플레이어 이동 소리 재생
                    isOutStartRoom[cur_player] = True # 시작점 방을 나간 경우
                    cur_room_loc[cur_player] = "복도" # 현재 방 위치를 복도로 설정
                    new_poss.append(player_pos) # 이동한 위치 추가
                    dice_roll -= 1 # 주사위 결과 1 감소
                    break
    print("주사위 결과 :", dice1, "+", dice2, "=", dice1 + dice2)
    while dice_roll > 0: # 주사위를 모두 사용할 때까지
        event = pg.event.wait()
        if event.type == pg.KEYDOWN: # 키를 누른 경우
            if event.key == pg.K_UP: # 위쪽 방향키를 누른 경우
                new_pos = player_pos[0], player_pos[1] - 1
                cur_dir = "위쪽"
            elif event.key == pg.K_DOWN: # 아래쪽 방향키를 누른 경우
                new_pos = player_pos[0], player_pos[1] + 1
                cur_dir = "아래쪽"
            elif event.key == pg.K_LEFT: # 왼쪽 방향키를 누른 경우
                new_pos = player_pos[0] - 1, player_pos[1]
                cur_dir = "왼쪽"
            elif event.key == pg.K_RIGHT: # 오른쪽 방향키를 누른 경우
                new_pos = player_pos[0] + 1, player_pos[1]
                cur_dir = "오른쪽"
            elif event.key == pg.K_ESCAPE or event.type == pg.QUIT: exit() # 게임 종료
            elif event.key == pg.K_RETURN: # 엔터 키를 누른 경우
                print(cur_player, "는 아직", dice_roll, "칸 이동하지 않았음")
                if dice_roll == dice1 + dice2: # 주사위를 모두 사용하지 않은 경우
                    show_message("경고", "한 칸 이상 이동해야합니다.")
                    print("경고, 한 칸 이상 이동해야함")
                    continue 
                if show_message("예/아니오", "아직 " + str(dice_roll) + "칸 이동하지 않았습니다. 정말 끝내시겠습니까?"): # Yes/No 대화상자를 표시합니다.
                    print(cur_player, "이/가 이동을 일찍 끝냄", old_pos, " -> ", player_pos)
                    move_sound.play() # 이동하는 소리 재생
                    return player_pos, None # 플레이어 위치 및 이동 사유 반환
                else: # No를 누른 경우
                    print("취소, 계속 진행함")
                    continue
            else: continue # 다른 키를 누른 경우
            mid_pos = ((player_pos[0] + new_pos[0]) / 2, (player_pos[1] + new_pos[1]) / 2) # 중간 위치
            mid = (int(mid_pos[0]*square_size + wall_pos[0] + square_size / 2), 
                   int(mid_pos[1]*square_size + wall_pos[1] + square_size / 2)) # 중간 위치(벽 판별 위해)
            if window.get_at(mid) == BLACK: # 벽이 있는 경우
                print("이동 불가,", cur_dir, "에 벽이 있음, 위치 :", new_pos)
                show_message("실패", cur_dir + "에 벽이 있어 이동할 수 없습니다. 다시 선택해주세요.")
                player_pos = new_poss[-1] # 마지막으로 성공한 위치로 돌아갑니다.
            else: # 벽이 없는 경우
                enter_room = handle_room_entry(new_pos, cur_player, isOutStartRoom, other_players_poss, cur_room_loc, case_envelope) # 방에 들어가는 경우
                if new_pos in other_players_poss.values(): # 다른 플레이어가 있는 경우 
                    print("이동 불가, 다른 플레이어가 있음, 위치 :", new_pos)
                    show_message("실패", "다른 플레이어가 있어 이동할 수 없습니다. 다시 선택해주세요.")
                    player_pos = new_poss[-1]  # 마지막으로 성공한 위치로 돌아갑니다.
                    continue
                elif (isOutStartRoom[cur_player] is True and cur_room_loc[cur_player] == "시작점" 
                      and enter_room != new_pos and hasReasoned[cur_player] is False): # 시작점 방을 나가고 추리 없이 다시 들어가는 경우
                    print("이동 불가, 추리를 먼저 해야함")
                    show_message("경고", "시작점 방을 나가고 다시 들어가려면 추리를 먼저 해야합니다.")
                    cur_room_loc[cur_player] = "복도"
                    player_pos = new_poss[-1] # 마지막으로 성공한 위치로 돌아갑니다.
                    continue
                elif enter_room != new_pos: # 방에 들어가는 경우
                    new_poss.append(enter_room) # 새로운 위치를 리스트에 추가
                    player_pos = enter_room # 플레이어 위치를 새로운 위치로 설정
                    dice_roll = 0 # 주사위 결과 초기화
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
                else: # 이동 가능한 경우
                    draw_player(create_player(cur_player, new_pos), True, True) # 플레이어 그리기
                    new_poss.append(new_pos)  # 새로운 위치를 리스트에 추가
                    player_pos = new_pos
                    dice_roll -= 1
    if dice_roll == 0: # 주사위를 모두 사용한 경우
        print(cur_player, "위치 이동", old_pos, " -> ", player_pos, "이동 후 위치 :", cur_room_loc[cur_player])
        if (cur_room_loc[cur_player] != "시작점" and isOutStartRoom[cur_player] is True and 
            cur_room_loc[cur_player] != "복도" and cur_room_loc[cur_player] != "바깥"): # 시작점 방을 나간 경우
            reason = reasoning(cur_player, cur_room_loc, player_cards) # 추리
            if reason is None: # 추리를 하지 않은 경우
                print("추리를 하지 않음. 다음 차례.")
                show_message("알림", "추리를 하지 않아 다음 차례로 넘어갑니다.")
            elif reason is True:
                print("추리를 함. 다음 차례.")
                show_message("알림", "추리를 하여 다음 차례로 넘어갑니다.")
                hasReasoned[cur_player] = True # 추리를 했음
            return player_pos, reason
    return player_pos, reason

def draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, btn_pos, cur_player, case_envelope, player_cards): # 모든 것 그리기
    window.fill(bg_color) # 창 배경색으로 채우기
    window.blit(cluedo_logo, (wall_pos[0] + 21 * square_size, wall_pos[1])) # 로고 그리기
    add_walls_to_grid(grid, grid_color, thickness) # 벽을 그리드에 추가
    draw_wall(thickness) # 벽 그리기
    draw_room_walls(room_walls, thickness) # 방 벽 그리기
    draw_room_names(font) # 방 이름 그리기
    if cur_player is not None: 
        draw_card(list(player_cards[cur_player]), 1, cur_player, case_envelope) # 플레이어 카드 그리기
        #draw_card(bonus_cards_list, 4) # 보너스 카드 그리기
        draw_card(list(case_envelope.values()), 2, cur_player, case_envelope) # 사건봉투 카드 그리기
    create_and_draw_players(player_pos, False) # 플레이어 생성 및 그리기
    draw_dice(dice1, dice2) # 주사위 그리기
    draw_btn(btn_pos, "주사위 굴리기", font, thickness) # 주사위 굴리기 버튼 그리기
    draw_btn((btn_pos[0] + 6 * square_size, btn_pos[1], btn_pos[2], btn_pos[3]), "게임 규칙", font, thickness) # 게임 규칙 버튼 그리기
    pg.display.flip() # 창 업데이트

def reasoning(cur_player, cur_room_loc, player_cards): # 추리
    print("추리 시작!")
    def make_guess(): # 추리하기
        bachim1 = "이" # 받침
        bachim2 = "을" # 받침
        nonHas = True # 아무도 가지고 있지 않은 경우
        reasoning_sound.play() # 추리 소리 재생
        selected_suspect = suspect_var.get() # 선택한 용의자
        selected_weapon = weapon_var.get() # 선택한 무기
        selected_room = cur_room_loc[cur_player] # 선택한 방 (현재 방)
        if not selected_suspect or not selected_weapon: # 선택한 용의자 또는 무기가 없는 경우
            msg.showwarning("경고", "모든 항목을 선택하세요.")
            return
        print(f"추리 : 용의자 - {selected_suspect}, 무기 - {selected_weapon}, 장소 - {selected_room}")
        if (ord(selected_suspect[-1]) - ord("가")) % 28 == 0: bachim1 = "가" # 받침이 없는 경우
        if (ord(selected_weapon[-1]) - ord("가")) % 28 == 0: bachim2 = "를" # 받침이 없는 경우
        msg.showinfo("추리", f"{selected_suspect}{bachim1} {selected_weapon}{bachim2} 이용해,\n{selected_room}에서 범행을 저질렀다고 추리해봅니다.")
        for player in player_cards.keys(): # 다른 플레이어가 가지고 있는 카드
            if player != cur_player: # 현재 플레이어가 아닌 경우
                if (selected_suspect in player_cards[player] or  # 선택한 용의자 또는 무기 또는 방이 다른 플레이어가 가지고 있는 경우
                    selected_weapon in player_cards[player] or 
                    selected_room in player_cards[player]):
                    nonHas = False # 아무도 가지고 있지 않은 경우가 아님
                    print(player, "이/가 가지고 있는 카드:", player_cards[player]) # 다른 플레이어가 가지고 있는 카드 출력
                    while True: # 무작위로 카드 선택
                        card = random.choice(player_cards[player]) # 무작위로 카드 선택
                        if card in [selected_suspect, selected_weapon, selected_room]: break # 선택한 카드가 아닌 경우 다시 선택
                    if (ord(player[-1]) - ord("가")) % 28 == 0: bachim1 = "가" # 받침이 없는 경우
                    else : bachim1 = "이"
                    if (ord(card[-1]) - ord("가")) % 28 == 0: bachim2 = "를" # 받침이 없는 경우
                    else : bachim2 = "을"
                    msg.showinfo("카드", f"{player}{bachim1} {card}{bachim2} 가지고 있습니다.") # 다른 플레이어가 가지고 있는 카드 출력
        if nonHas: msg.showinfo("카드", "다른 플레이어 카드를 전부 확인했지만 . . .\n아무도 가지고 있지 않습니다.") # 아무도 가지고 있지 않은 경우
        root.destroy()
    app_width, app_height = 300, 100
    root = tk.Tk()
    root.title("추리")
    windows_width = root.winfo_screenwidth()
    windows_height = root.winfo_screenheight()
    center_width = (windows_width / 2) - (app_width / 2)
    center_height = (windows_height / 2) - (app_height / 2)
    root.geometry(f"{app_width}x{app_height}+{int(center_width)}+{int(center_height)}")
    
    main_theme.set_volume(0.06) # 메인 테마 볼륨 설정
    eval(f"ambient_{locs[cur_room_loc[cur_player]]}").play(-1) # 현재 방의 배경음악 재생
    tk.Label(root, text="용의자 선택").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(root, text="살인 도구 선택").grid(row=1, column=0, padx=10, pady=5)
    suspects_list = list(suspects.keys()) # 용의자 목록
    weapons_list = list(weapons) # 무기 목록
    suspect_var = tk.StringVar() # 용의자 변수
    weapon_var = tk.StringVar() # 무기 변수
    suspect_menu = ttk.Combobox(root, textvariable=suspect_var, values=suspects_list, state="readonly") # 용의자 메뉴
    suspect_menu.grid(row=0, column=1, padx=10, pady=5) # 용의자 메뉴 그리기
    weapon_menu = ttk.Combobox(root, textvariable=weapon_var, values=weapons_list, state="readonly") # 무기 메뉴
    weapon_menu.grid(row=1, column=1, padx=10, pady=5) # 무기 메뉴 그리기

    tk.Button(root, text="추리하기", command=make_guess).grid(row=2, columnspan=2, pady=10) # 추리하기 버튼
    root.mainloop()
    if suspect_var.get() not in suspects or weapon_var.get() not in weapons: # 선택한 용의자 또는 무기가 없는 경우
        eval(f"ambient_{locs[cur_room_loc[cur_player]]}").fadeout(500) # 현재 방의 배경음악 정지
        return None # 선택한 용의자 또는 무기가 없는 경우
    else:
        eval(f"ambient_{locs[cur_room_loc[cur_player]]}").fadeout(500) # 현재 방의 배경음악 정지
        return True # 추리를 한 경우
    
def final_reasoning(cur_player, case_envelope): # 최종 추리
    print("최종 추리 시작!")
    main_theme.set_volume(0) # 메인 테마 볼륨 설정
    final_reasoning_sound.set_volume(0.2) # 최종 추리 소리 볼륨 설정
    final_reasoning_sound.play(-1) # 최종 추리 소리 재생
    def really_right(): # 확신 여부
        if show_message("예/아니오", "정말 확실합니까?\n실패하면 게임에서 제외됩니다."): make_guess() # 추리하기
        else: return
    def make_guess(): # 추리하기
        bachim1 = "이" # 받침
        bachim2 = "을" # 받침
        selected_suspect = suspect_var.get() # 선택한 용의자
        selected_weapon = weapon_var.get() # 선택한 무기
        selected_room = room_var.get() # 선택한 방
        if not selected_suspect or not selected_weapon or not selected_room: # 선택한 용의자, 무기, 방이 없는 경우
            msg.showwarning("경고", "모든 항목을 선택하세요.")
            return
        if (ord(selected_suspect[-1]) - ord("가")) % 28 == 0: bachim1 = "가"
        if (ord(selected_weapon[-1]) - ord("가")) % 28 == 0: bachim2 = "를"
        print(f"추리: 용의자 - {selected_suspect}, 무기 - {selected_weapon}, 장소 - {selected_room}")
        msg.showinfo("추리", f"{selected_suspect}{bachim1} {selected_weapon}{bachim2} 사용해,\n{selected_room}에서 범행을 저질렀다고 확신합니다.")
        root.destroy()
    app_width, app_height = 300, 150
    root = tk.Tk()
    root.title("최종 추리")
    windows_width = root.winfo_screenwidth()
    windows_height = root.winfo_screenheight()
    center_width = (windows_width / 2) - (app_width / 2)
    center_height = (windows_height / 2) - (app_height / 2)
    root.geometry(f"{app_width}x{app_height}+{int(center_width)}+{int(center_height)}")

    tk.Label(root, text="용의자 선택").grid(row=0, column=0, padx=10, pady=5) # 용의자 선택 레이블
    tk.Label(root, text="살인 도구 선택").grid(row=1, column=0, padx=10, pady=5) # 살인 도구 선택 레이블
    tk.Label(root, text="장소 선택").grid(row=2, column=0, padx=10, pady=5) # 장소 선택 레이블
    suspects_list = list(suspects.keys()) # 용의자 목록
    weapons_list = list(weapons) # 무기 목록
    rooms_list = list(locs.keys()) # 방 목록
    suspect_var = tk.StringVar() # 용의자 변수
    weapon_var = tk.StringVar() # 무기 변수
    room_var = tk.StringVar() # 방 변수
    suspect_menu = ttk.Combobox(root, textvariable=suspect_var, values=suspects_list, state="readonly") # 용의자 메뉴
    suspect_menu.grid(row=0, column=1, padx=10, pady=5) # 용의자 메뉴 그리기
    weapon_menu = ttk.Combobox(root, textvariable=weapon_var, values=weapons_list, state="readonly") # 무기 메뉴
    weapon_menu.grid(row=1, column=1, padx=10, pady=5) # 무기 메뉴 그리기
    room_menu = ttk.Combobox(root, textvariable=room_var, values=rooms_list, state="readonly") # 방 메뉴
    room_menu.grid(row=2, column=1, padx=10, pady=5) # 방 메뉴 그리기
    
    tk.Button(root, text="추리하기", command=really_right).grid(row=3, columnspan=2, pady=10)
    root.mainloop()
    # 추리 결과가 사건 봉투 내용과 일치하는 경우, 최종 추리 성공, 게임 승리, 해당 플레이어는 이제 게임에 참여 불가
    if suspect_var.get() == case_envelope["suspect"] and weapon_var.get() == case_envelope["weapon"] and room_var.get() == case_envelope["location"]: 
        final_reasoning_sound.stop() # 최종 추리 소리 정지
        win_sound.set_volume(0.2) # 승리 소리 볼륨 설정
        win_sound.play() # 승리 소리 재생
        print("최종 추리 성공, ", cur_player, "승리")
        show_message("승리", f"{cur_player}님, 최종 추리 성공으로 승리하셨습니다.")
        end_screen(False, case_envelope, cur_player) # 게임 종료 화면
    else: # 추리 결과가 사건 봉투 내용과 일치하지 않는 경우, 최종 추리 실패, 게임 패배, 해당 플레이어는 이제 게임에 참여 불가
        final_reasoning_sound.stop() # 최종 추리 소리 정지
        lose_sound.play() # 패배 소리 재생
        print("최종 추리 실패,", cur_player, "패배")
        show_message("패배", f"{cur_player}님, 최종 추리 실패로 패배하셨습니다.")
        lose_sound.stop() # 패배 소리 정지
        return False
    
def end_screen(Losed, case_envelope, cur_player): # 게임 종료 화면
    final_reasoning_sound.stop() # 최종 추리 소리 정지
    cluedo_logo = pg.image.load("images/cluedo_logo.png") # 클루 로고 이미지 로드
    cluedo_logo = pg.transform.scale(cluedo_logo, (12 * square_size, 4 * square_size))
    pg.draw.rect(window, WHITE, (0, 0, window_size[0], window_size[1])) # 창 하얀색으로 채우기
    window.blit(cluedo_logo, (wall_pos[0] + 13 * square_size, wall_pos[1] - square_size)) # 로고 그리기
    draw_card(list(case_envelope.values()), 0, cur_player, case_envelope, True, Losed) # 사건봉투 카드 그리기
    font = pg.font.SysFont('malgungothic', square_size) # 폰트 설정
    end_btn_pos = wall_pos[0] + 27 * square_size, wall_pos[1] + 17 * square_size, 4 * square_size, 2 * square_size # 버튼 위치 설정
    draw_btn(end_btn_pos, "게임 종료", font, thickness)
    pg.display.flip() # 창 업데이트
    event = pg.event.wait() # 이벤트를 기다립니다
    while True: # 무한 루프
        for event in pg.event.get(): # 이벤트를 가져옵니다
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos() # 마우스 위치를 가져옵니다
                if end_btn_pos[0] <= x <= end_btn_pos[0] + end_btn_pos[2] and end_btn_pos[1] <= y <= end_btn_pos[1] + end_btn_pos[3]: 
                    exit() # 게임 종료 버튼을 누른 경우