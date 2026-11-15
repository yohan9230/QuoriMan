# 설정 가능한 변수들
## 미로 크기
maze_size = 3

# 상수
## 미로 세로/가로 벽의 교차점
PILLAR = "+" 
## 미로의 세로 벽
VERTICAL_WALL = "|"
## 미로의 가로 벽
HORIZONTAL_WALL = "--" 
## 벽 사이 빈 칸. 공백 2칸.
CELL = "  " 

# 가로 벽 리스트 (maze_size * maze_size+1), True: 벽 있음
VERTICAL_WALL_LIST = []
for i in range(maze_size):
    row = []
    for j in range(maze_size+1):
        row.append(True)
    VERTICAL_WALL_LIST.append(row)

# 가로 벽 리스트 출력 함수
def print_vertical_wall_list():
    for i in range(maze_size):
        for j in range(maze_size+1):
            print(VERTICAL_WALL_LIST[i][j], end = " ")
        print("")

# 세로 벽 리스트 (maze_size+1 * maze_size), True: 벽 있음
HORIZONTAL_WALL_LIST = []
for i in range(maze_size+1):
    row = []
    for j in range(maze_size):
        row.append(True)
    HORIZONTAL_WALL_LIST.append(row)

# 세로 벽 리스트 출력 함수
def print_horizontal_wall_list():
    for i in range(maze_size+1):
        for j in range(maze_size):
            print(HORIZONTAL_WALL_LIST[i][j], end = " ")
        print("")


def print_horizontal_wall(int col):
    """- 가로 줄 출력하는 함수
    - maze_size와 동일한 칸수가 되도록 벽을 세움"""
    for i in range(maze_size+1):
        print(PILLAR, end = "")
        if (i != maze_size):
            print(HORIZONTAL_WALL, end = "")
        else:
            print("")

def print_vertical_wall():
    """- 세로 벽 출력하는 함수
    - maze_size와 동일한 칸수가 되도록 벽을 세움"""
    for i in range(maze_size+1):
        print(VERTICAL_WALL, end = "")
        if (i != maze_size):
            print(CELL, end = "")
        else:
           print("")

# 미로 크기 0 이하 예외 처리
if maze_size <= 0:
    raise ValueError("maze_size 값은 0이하 일수 없습니다. 변수값을 수정해주세요.")

# 현재 출력중인 행 번호
# print_horizontal_wall()
# for row in range (maze_size):
#     print_vertical_wall()
#     print_horizontal_wall()