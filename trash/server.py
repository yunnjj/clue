# server.py
import socket
import threading
import random
from collections import defaultdict
from time import sleep

# 게임 설정
NUM_PLAYERS = 4
SUSPECTS = {"피콕": "BLUE", "플럼": "PURPLE", "스칼렛": "RED", "머스타드": "YELLOW", "그린": "GREEN", "화이트": "WHITE"}
WEAPONS = ["파이프", "밧줄", "단검", "렌치", "권총", "촛대"]
ROOMS = ['마당', '거실', '식당', '부엌', '서재', '욕실', '침실', '게임룸', '차고']
STARTROOM = ['시작장소']
# STARTPOS = [(0, 0), (0, 24), (24, 0), (24, 24)]
BONUS = {"차례를 한 번 더 진행합니다." : "지금 사용하거나 필요할 때 사용합니다.",
      "원하는 장소로 이동합니다." : "지금 사용합니다.",
      "카드 엿보기" : "누군가 다른 사람에게 추리 카드를 보여줄 때 그 카드를 볼 수 있습니다. 필요할 때 사용합니다.",
      "나온 주사위에 6을 더할 수 있습니다." : "지금 사용하거나 필요할 때 사용합니다.",
      "다른 사람의 카드 한 장을 공개합니다." : "한 사람을 정해 이 카드를 보여주면, 그 사람은 자기 카드 중 한 장을 모두에게 보여주어야 합니다. 지금 사용합니다.",
      "한 번 더 추리합니다." : "자기 말이나 다른 사람의 말 또는 토큰을 이용하지 않고 원하는 장소, 사람, 도구를 정해 추리할 수 있습니다. 지금 사용합니다."
}
bonus_cards = [card for card in BONUS.keys() for _ in range(2)] # 각 카드를 원하는 수만큼 복제합니다.
bonus_cards.extend(["원하는 장소로 이동합니다."]) # 보너스카드 목록에 추가
random.shuffle(bonus_cards) # 보너스카드 섞기
case_file = [random.choice(list(SUSPECTS.keys())), random.choice(WEAPONS), random.choice(ROOMS)] # 사건 파일 생성

# 서버 설정
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8000
MAX_CONNECTIONS = 5

# 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
server_socket.listen(MAX_CONNECTIONS)
print(f"서버가 {SERVER_ADDRESS}:{SERVER_PORT}에서 실행 중입니다.")

# 클라이언트 연결 대기
print(f"서버 시작, {NUM_PLAYERS}명의 플레이어 연결 대기 중...")
clients = []
player_cards = defaultdict(list)
suspects = random.sample(list(SUSPECTS.keys())[:4], NUM_PLAYERS) # 플레이어 순서 랜덤화
print(f"플레이어: {', '.join(suspects)}")
for i in range(NUM_PLAYERS-3):
   client_socket, addr = server_socket.accept()
   print(f"{suspects[i]} 연결됨: {addr}")
   clients.append(client_socket)

print("모든 플레이어 연결됨, 게임 시작!")

# 카드 분배
all_cards = list(SUSPECTS.keys()) + WEAPONS + ROOMS # 모든 카드
random.shuffle(all_cards) # 카드 섞기
for i, client in enumerate(clients):  # 각 플레이어에게 카드 분배
   cards = [all_cards.pop() for _ in range(NUM_PLAYERS)]  # 한 번에 4장의 카드를 뽑음
   player_cards[i].extend(cards)  # 카드 분배
   print(f"{suspects[i]}에게 카드 {', '.join(cards)} 분배")

# 사건 파일 생성
case_file = [random.choice(list(SUSPECTS.keys())), random.choice(WEAPONS), random.choice(ROOMS)]
print(f"사건 파일: {', '.join(case_file)}")

def handle_client(client_socket, player_id): 
   print(suspects, player_id)
   print(f"{suspects[player_id]} 이/가 연결되었습니다.")
   clients.append(client_socket)

   # 플레이어 이름, 색상, 카드 정보 전송 한번에
   player_info = f"player_info|{suspects[player_id]}:{SUSPECTS[suspects[player_id]]}:{','.join(player_cards[player_id])}"
   print(player_info)
   client_socket.send(player_info.encode())
   while True:
      try:
         data = client_socket.recv(1024)
         if data:  
            message = data.decode()  # 데이터를 디코딩
            if message == "dice": # 주사위 굴리기
               dice1 = random.randint(1, 6)
               dice2 = random.randint(1, 6)
               client_socket.send(f"dice:{dice1},{dice2}".encode())
         else: break
      except: break
   print(f"{suspects[player_id]} 이/가 연결을 종료했습니다.")
   clients.remove(client_socket)
   client_socket.close()
   
# 클라이언트 연결 대기
threads = []
while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    player_id = len(clients) - 2  # 새로운 player_id는 clients 리스트의 마지막 인덱스
    client_thread = threading.Thread(target=handle_client, args=(client_socket, player_id))
    client_thread.start()
    threads.append(client_thread)

server_socket.close()