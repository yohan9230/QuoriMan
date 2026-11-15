from enum import Enum
# -----------------------------------------------------
# 변수

## 미로 크기
maze_size = 1

## 수평 벽 리스트 (maze_size+1 * maze_size), True: 벽 있음
HORIZONTAL_WALL_LIST = []
## 수직 벽 리스트 (maze_size * maze_size+1), True: 벽 있음
VERTICAL_WALL_LIST = []

# -----------------------------------------------------
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

## 방향
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

## 수평/수직
class Orientation(Enum):
    horizontal = 0
    vertical = 1

# -----------------------------------------------------
# 수평/수직 벽 정보 리스트 관련 함수들

## 수평 벽 정보 리스트 만드는 함수
def make_horizontal_wall_list():
    """수평 벽 존재 여부 정보 담는 2차원 리스트"""
    for i in range(maze_size+1):
        row = []
        for j in range(maze_size):
            row.append(True)
        HORIZONTAL_WALL_LIST.append(row)

## 수평 벽 정보 출력 함수
def print_horizontal_wall_list():
    """수평 벽 리스트 출력 함수"""
    for i in range(maze_size+1):
        for j in range(maze_size):
            print(HORIZONTAL_WALL_LIST[i][j], end = " ")
        print("")

## 수직 벽 정보 리스트 만드는 함수
def make_vertical_wall_list():
    """수직 벽 존재 여부 정보 담는 2차원 리스트"""
    for i in range(maze_size):
        row = []
        for j in range(maze_size+1):
            row.append(True)
        VERTICAL_WALL_LIST.append(row)

## 수직 벽 정보 출력 함수
def print_vertical_wall_list():
    """수직 벽 리스트 출력 함수"""
    for i in range(maze_size):
        for j in range(maze_size+1):
            print(VERTICAL_WALL_LIST[i][j], end = " ")
        print("")


## 벽 존재 여부 판단 함수
def is_there_wall(row:int, col:int, dir:Direction):
    """미로의 [row, col]칸에서, dir방향에 벽이 있는지 판단하는 함수"""
    if row < 0 or row > maze_size-1:
        raise ValueError("조회 불가능한 미로 행 번호")
    if col < 0 or col > maze_size-1:
        raise ValueError("조회 불가능한 미로 열 번호")
    match dir:
        case Direction.UP:
            return HORIZONTAL_WALL_LIST[row][col]
        case Direction.DOWN:
            return HORIZONTAL_WALL_LIST[row+1][col]
        case Direction.LEFT:
            return VERTICAL_WALL_LIST[row][col]
        case Direction.RIGHT:
            return VERTICAL_WALL_LIST[row][col+1]
        case _:
            raise ValueError("벽 조회에 불가능한 방향 조회")

## 벽 수정 함수
def change_wall(row:int, col:int, dir:Direction, change:bool):
    """미로의 [row, col]칸에서, dir방향의 벽을 변경하는 함수"""
    if row < 0 or row > maze_size-1:
        raise ValueError("조회 불가능한 미로 행 번호")
    if col < 0 or col > maze_size-1:
        raise ValueError("조회 불가능한 미로 열 번호")
    match dir:
        case Direction.UP:
            HORIZONTAL_WALL_LIST[row][col] = change
        case Direction.DOWN:
            HORIZONTAL_WALL_LIST[row+1][col] = change
        case Direction.LEFT:
            VERTICAL_WALL_LIST[row][col] = change
        case Direction.RIGHT:
            VERTICAL_WALL_LIST[row][col+1] = change
        case _:
            raise ValueError("벽 조회에 불가능한 방향 조회")


# -----------------------------------------------------

## 미로 출력 함수
def print_maze():
    """미로 출력 함수"""
    for row in range(maze_size):
        # 수평 벽 출력(칸의 위쪽 벽 유무 조회)
        for col in range(maze_size):
            print(PILLAR, end = "")
            if is_there_wall(row, col, Direction.UP) == True:
                print(HORIZONTAL_WALL, end = "")
            else:
                print(HORIZONTAL_WALL_EMPTY, end = "")
        print(PILLAR)
        # 수직 벽 출력(칸의 왼쪽 벽 유무 조회)
        for col in range(maze_size):
            if is_there_wall(row, col, Direction.LEFT) == True:
                print(VERTICAL_WALL, end = "")
            else:
                print(VERTICAL_WALL_EMPTY, end = "")
            print(CELL, end = "")
        # 행의 가장 마지막 수직 벽 출력(마지막 칸의 오른쪽 벽 유무 조회)
        if is_there_wall(row, maze_size-1, Direction.RIGHT) == True:
            print(VERTICAL_WALL)
        else:
            print(VERTICAL_WALL_EMPTY)
    # 가장 마지막 수평 벽 출력
    for col in range(maze_size):
        print(PILLAR, end = "")
        if is_there_wall(maze_size-1, col, Direction.DOWN) == True:
            print(HORIZONTAL_WALL, end = "")
        else:
            print(HORIZONTAL_WALL_EMPTY, end = "")
    print(PILLAR)
        
# -----------------------------------------------------
# 여기서부터 실행 코드

maze_size = int(input("미로 크기를 입력하세요: "))

# 미로 크기 0 이하 예외 처리
if maze_size <= 0:
    raise ValueError("maze_size 값은 0이하 일수 없습니다. 변수값을 수정해주세요.")

make_horizontal_wall_list()
make_vertical_wall_list()

print_maze()