# 설정 가능한 변수들
## 미로 크기
maze_size = 3

# 상수

## 미로의 수평 벽
HORIZONTAL_WALL = "--" 
## 미로의 수평 벽(비어있음)
HORIZONTAL_WALL_EMPTY = "  "

## 미로의 수직 벽
VERTICAL_WALL = "|"
## 미로의 수직 벽(비어있음)
VERTICAL_WALL_EMPTY = " "

## 미로 수평/수직 벽의 교차점 = 기둥
PILLAR = "+" 

## 벽 사이 빈 칸. 공백 2칸.
CELL = "  " 

# -----------------------------------------------------

# 수평 벽 리스트 (maze_size+1 * maze_size), True: 벽 있음
HORIZONTAL_WALL_LIST = []
for i in range(maze_size+1):
    row = []
    for j in range(maze_size):
        row.append(True)
    HORIZONTAL_WALL_LIST.append(row)

# 수평 벽 리스트 출력 함수
def print_horizontal_wall_list():
    for i in range(maze_size+1):
        for j in range(maze_size):
            print(HORIZONTAL_WALL_LIST[i][j], end = " ")
        print("")

# 수평 벽 여부 판단 함수
def is_there_horizontal_wall(row:int, col:int):
    """[row, col]에 벽이 있는지 판단하는 함수"""
    return HORIZONTAL_WALL_LIST[row][col]

# 수직 벽 리스트 (maze_size * maze_size+1), True: 벽 있음
VERTICAL_WALL_LIST = []
for i in range(maze_size):
    row = []
    for j in range(maze_size+1):
        row.append(True)
    VERTICAL_WALL_LIST.append(row)

# 수직 벽 리스트 출력 함수
def print_vertical_wall_list():
    for i in range(maze_size):
        for j in range(maze_size+1):
            print(VERTICAL_WALL_LIST[i][j], end = " ")
        print("")

# 수직 벽 여부 판단 함수
def is_there_vertical_wall(row:int, col:int):
    """[row, col]에 벽이 있는지 판단하는 함수"""
    return VERTICAL_WALL_LIST[row][col]

# -----------------------------------------------------
# 수평/수직 벽 출력 함수 정의

def print_horizontal_wall(row_num:int):
    """- row_num: 0 ~ maze_size-1
    - row_num 번째 수평 벽을 출력하는 함수
    - maze_size와 동일한 칸수가 되도록 벽을 세움"""
    
    if row_num < 0 or row_num > maze_size-1:
        raise ValueError("잘못된 수평 벽 번호")
    
    for i in range(maze_size):
        print(PILLAR, end = "")
        if HORIZONTAL_WALL_LIST[row_num][i] == True:
            print(HORIZONTAL_WALL, end = "")
        else: 
            print(HORIZONTAL_WALL_EMPTY, end = "")
    print(PILLAR)

def print_vertical_wall(row_num:int):
    """- row_num: 0 ~ maze_size-1
    - 수직 벽 출력하는 함수
    - maze_size와 동일한 칸수가 되도록 벽을 세움"""
    for i in range(maze_size):
        if VERTICAL_WALL_LIST[row_num][i] == True:
            print(VERTICAL_WALL, end = "")
        else:
            print(VERTICAL_WALL_EMPTY, end = "")
        print(CELL, end = "")
    print(VERTICAL_WALL)

# -----------------------------------------------------
# 여기서부터 실행 코드

# 미로 크기 0 이하 예외 처리
if maze_size <= 0:
    raise ValueError("maze_size 값은 0이하 일수 없습니다. 변수값을 수정해주세요.")

# 현재 출력중인 행 번호
# print_horizontal_wall()
# for row in range (maze_size):
#     print_vertical_wall()
#     print_horizontal_wall()