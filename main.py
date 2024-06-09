import pygame as pg # 파이게임 라이브러리 불러오기
import os # 운영체제 라이브러리 불러오기

pg.init() # pygame 초기화
from package.setting import * # setting.py 파일에서 모든 변수 및 함수 불러오기
from package.functions import * # functions.py 파일에서 모든 함수 불러오기
os.system('cls') # 콘솔 화면 지우기

def main():
    pg.init()
    dice1 = 0
    dice2 = 0
    cnt = 0
    grid = set()
    font = pg.font.SysFont('malgungothic', square_size * 2 // 3)
    case_envelope, player_cards, last_cards = shuffle_and_distribute_cards()
    add_rooms_to_grid(grid)
    dice_btn_pos = wall_pos[0] + 27 * square_size, wall_pos[1] + 17 * square_size, 4 * square_size, 2 * square_size
    clue_notes_btn_pos = [
        (wall_pos[0] + 21 * square_size, wall_pos[1] + 19.5 * square_size, 4 * square_size, 2 * square_size),
        (wall_pos[0] + 25 * square_size, wall_pos[1] + 19.5 * square_size, 4 * square_size, 2 * square_size),
        (wall_pos[0] + 29 * square_size, wall_pos[1] + 19.5 * square_size, 4 * square_size, 2 * square_size),
        (wall_pos[0] + 33 * square_size, wall_pos[1] + 19.5 * square_size, 4 * square_size, 2 * square_size),
    ]

    players = list(suspects.keys())
    player_pos = {
        players[0]: (8, 10), players[1]: (11, 10),
        players[2]: (8, 12), players[3]: (11, 12)
    }
    isOutStartRoom = {
        players[0]: False, players[1]: False,
        players[2]: False, players[3]: False
    }
    cur_room_loc = {
        players[0]: room_names[rooms.index(rooms[12])], players[1]: room_names[rooms.index(rooms[12])],
        players[2]: room_names[rooms.index(rooms[12])], players[3]: room_names[rooms.index(rooms[12])]
    }
    
    draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, dice_btn_pos, clue_notes_btn_pos, None, case_envelope, player_cards)
    pg.display.flip()
    
    running = True
    previous_dice1 = None
    previous_dice2 = None
    notMoved = False
                     
    while running:
        global isLosed
        main_theme.set_volume(0.18)
        if main_theme.get_num_channels() == 0:
            main_theme.play(-1)
        for event in pg.event.get():
            cur_player = players[cnt % PLAYER]
            if all(isLosed.values()):
                main_theme.stop()
                if lose_sound.get_num_channels() == 0:
                    lose_sound.play(-1)
                print("모든 플레이어가 패배함")
                show_message("알림", "모든 플레이어가 패배하여 게임이 종료되었습니다.\n사건 봉투를 공개합니다.")
                end_screen(True, case_envelope, cur_player)
            if isLosed[cur_player] is True:
                print()
                print(cur_player, "이/가 이미 패배함. 다음 차례로 넘어감")
                show_message("알림", f"{cur_player}님, 이미 패배하셨습니다.\n다음 차례로 넘어갑니다.")
                cnt += 1
                continue
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (gmrule_btn_pos[0] <= x <= gmrule_btn_pos[0] + gmrule_btn_pos[2] 
                    and gmrule_btn_pos[1] <= y <= gmrule_btn_pos[1] + gmrule_btn_pos[3]):
                    show_game_rules()
                for i, btn_pos in enumerate(clue_notes_btn_pos):
                    if (btn_pos[0] <= x <= btn_pos[0] + btn_pos[2] 
                        and btn_pos[1] <= y <= btn_pos[1] + btn_pos[3]):
                        show_clue_notes(players[i])
            if notMoved:
                player_pos, dice1, dice2, previous_dice1, previous_dice2 = do_dice_roll(previous_dice1, previous_dice2, dice1, dice2, player_pos)
                draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, dice_btn_pos, clue_notes_btn_pos, cur_player, case_envelope, player_cards)
                other_players_poss = {player[0]: (player[1][0], player[1][1]) for player in player_pos.items() if player[0] != cur_player}
                new_pos, reason = move_player(cur_player, player_pos[cur_player], dice1, dice2, other_players_poss, isOutStartRoom, cur_room_loc, case_envelope, player_cards)
                if new_pos != player_pos[cur_player] and reason is not None:
                    previous_dice1 = None
                    previous_dice2 = None
                    notMoved = False
                else:
                    previous_dice1 = dice1
                    previous_dice2 = dice2
                    notMoved = True
                player_pos[cur_player] = new_pos
                draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, dice_btn_pos, clue_notes_btn_pos, cur_player, case_envelope, player_cards)
            else:
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if handle_dice_click(x, y, dice_btn_pos):
                        main_theme.set_volume(0.12)
                        player_pos, dice1, dice2, previous_dice1, previous_dice2 = do_dice_roll(previous_dice1, previous_dice2, dice1, dice2, player_pos)
                        draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, dice_btn_pos, clue_notes_btn_pos, cur_player, case_envelope, player_cards)
                        other_players_poss = {player[0]: (player[1][0], player[1][1]) for player in player_pos.items() if player[0] != cur_player}
                        new_pos, reason = move_player(cur_player, player_pos[cur_player], dice1, dice2, other_players_poss, isOutStartRoom, cur_room_loc, case_envelope, player_cards)
                        if new_pos == player_pos[cur_player] and reason is None:
                            previous_dice1 = dice1
                            previous_dice2 = dice2
                            notMoved = True       
                        else:
                            previous_dice1 = None
                            previous_dice2 = None     
                            cnt += 1
                            notMoved = False      
                        player_pos[cur_player] = new_pos
                        draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, dice_btn_pos, clue_notes_btn_pos, cur_player, case_envelope, player_cards)
    pg.quit()

def draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, btn_pos, clue_notes_btn_pos, cur_player, case_envelope, player_cards):
    window.fill(bg_color)
    window.blit(cluedo_logo, (wall_pos[0] + 21 * square_size, wall_pos[1]))
    add_walls_to_grid(grid, grid_color, thickness)
    draw_wall(thickness)
    draw_room_walls(room_walls, thickness)
    draw_room_names(font)
    if cur_player is not None:
        draw_card(list(player_cards[cur_player]), 1, cur_player, case_envelope)
        draw_card(list(case_envelope.values()), 2, cur_player, case_envelope)
    create_and_draw_players(player_pos, False)
    draw_dice(dice1, dice2)
    draw_btn(btn_pos, "주사위 굴리기", font, thickness)
    for i, pos in enumerate(clue_notes_btn_pos):
        draw_btn(pos, f"노트 {i+1}", font, thickness)
    draw_btn((btn_pos[0] + 6 * square_size, btn_pos[1], btn_pos[2], btn_pos[3]), "게임 규칙", font, thickness)
    pg.display.flip()

if __name__ == "__main__":
    main()
