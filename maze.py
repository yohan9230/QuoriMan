from enum import IntEnum, Enum

# 방향
class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

# 수평/수직
class Orientation(Enum):
    horizontal = 0
    vertical = 1

# 미로 클래스
class Maze:
    # 미로의 수평 벽
    HORIZONTAL_WALL = "--" 
    # 미로의 수평 벽(비어있음)
    HORIZONTAL_WALL_EMPTY = "  "
    # 미로의 수직 벽
    VERTICAL_WALL = "|"
    # 미로의 수직 벽(비어있음)
    VERTICAL_WALL_EMPTY = " "
    # 미로 수평/수직 벽의 교차점 = 기둥
    PILLAR = "+" 
    # 벽 사이 빈 칸. 공백 2칸.
    CELL = "  " 
    # 시작 위치
    STARTCELL = "<>"
    
    def __init__(self, maze_size:int):
        if maze_size <= 0:
            raise ValueError("maze_size 값은 0이하 일수 없습니다. 변수값을 수정해주세요.")
        self.maze_size = maze_size
        # 수평 벽 리스트 (maze_size+1 * maze_size), True: 벽 있음
        self.HORIZONTAL_WALL_LIST = []
        # 수직 벽 리스트 (maze_size * maze_size+1), True: 벽 있음
        self.VERTICAL_WALL_LIST = []
        
        self.make_horizontal_wall_list()
        self.make_vertical_wall_list()

    ## 수평 벽 정보 리스트 만드는 함수
    def make_horizontal_wall_list(self):
        """수평 벽 존재 여부 정보 담는 2차원 리스트"""
        # 기존에 수평 벽 리스트가 있을 수 있으므로 초기화
        self.HORIZONTAL_WALL_LIST.clear()
        for i in range(self.maze_size+1):
            row = []
            for j in range(self.maze_size):
                row.append(True)
            self.HORIZONTAL_WALL_LIST.append(row)

    ## 수평 벽 정보 출력 함수
    def print_horizontal_wall_list(self):
        """수평 벽 리스트 출력 함수"""
        for i in range(self.maze_size+1):
            for j in range(self.maze_size):
                print(self.HORIZONTAL_WALL_LIST[i][j], end = " ")
            print("")

    ## 수직 벽 정보 리스트 만드는 함수
    def make_vertical_wall_list(self):
        """수직 벽 존재 여부 정보 담는 2차원 리스트"""
        # 기존에 수직 벽 리스트가 있을 수 있으므로 초기화
        self.VERTICAL_WALL_LIST.clear()
        for i in range(self.maze_size):
            row = []
            for j in range(self.maze_size+1):
                row.append(True)
            self.VERTICAL_WALL_LIST.append(row)

    ## 수직 벽 정보 출력 함수
    def print_vertical_wall_list(self):
        """수직 벽 리스트 출력 함수"""
        for i in range(self.maze_size):
            for j in range(self.maze_size+1):
                print(self.VERTICAL_WALL_LIST[i][j], end = " ")
            print("")

    ## 벽 존재 여부 판단 함수
    def is_there_wall(self, row:int, col:int, dir:Direction):
        """row, col 위치에서, dir 방향에 벽이 있는지 확인하여 반환함"""
        if self.out_of_maze(row, col) == True:
            raise ValueError
        match dir:
            case Direction.UP:
                return self.HORIZONTAL_WALL_LIST[row][col]
            case Direction.DOWN:
                return self.HORIZONTAL_WALL_LIST[row+1][col]
            case Direction.LEFT:
                return self.VERTICAL_WALL_LIST[row][col]
            case Direction.RIGHT:
                return self.VERTICAL_WALL_LIST[row][col+1]
            case _:
                raise ValueError("벽 조회에 불가능한 방향 조회")

    ## 벽 수정 함수
    def change_wall(self, row:int, col:int, dir:Direction, change:bool):
        """미로의 [row, col]칸에서, dir방향의 벽을 변경하는 함수"""
        if self.out_of_maze(row, col) == True:
            raise ValueError("잘못된 위치: 미로 밖")
        match dir:
            case Direction.UP:
                self.HORIZONTAL_WALL_LIST[row][col] = change
            case Direction.DOWN:
                self.HORIZONTAL_WALL_LIST[row+1][col] = change
            case Direction.LEFT:
                self.VERTICAL_WALL_LIST[row][col] = change
            case Direction.RIGHT:
                self.VERTICAL_WALL_LIST[row][col+1] = change
            case _:
                raise ValueError("벽 조회에 불가능한 방향 조회")
    
    ## 미로 출력 함수
    def print_maze(self, start_row:int = None, start_col:int = None):
        """미로 출력 함수"""
        for row in range(self.maze_size):
            # 수평 벽 출력(칸의 위쪽 벽 유무 조회)
            for col in range(self.maze_size):
                print(self.PILLAR, end = "")
                if self.is_there_wall(row, col, Direction.UP) == True:
                    print(self.HORIZONTAL_WALL, end = "")
                else:
                    print(self.HORIZONTAL_WALL_EMPTY, end = "")
            print(self.PILLAR)
            # 수직 벽 출력(칸의 왼쪽 벽 유무 조회)
            for col in range(self.maze_size):
                if self.is_there_wall(row, col, Direction.LEFT) == True:
                    print(self.VERTICAL_WALL, end = "")
                else:
                    print(self.VERTICAL_WALL_EMPTY, end = "")
                # 시작 위치인 경우에만 시작 위치 표시
                if (row == start_row) and (col == start_col):
                    print(self.STARTCELL, end = "")
                else:
                    # 시작 위치가 아닌 칸에는 공백 출력
                    print(self.CELL, end = "")
            # 행의 가장 마지막 수직 벽 출력(마지막 칸의 오른쪽 벽 유무 조회)
            if self.is_there_wall(row, self.maze_size-1, Direction.RIGHT) == True:
                print(self.VERTICAL_WALL)
            else:
                print(self.VERTICAL_WALL_EMPTY)
        # 가장 마지막 수평 벽 출력
        for col in range(self.maze_size):
            print(self.PILLAR, end = "")
            if self.is_there_wall(self.maze_size-1, col, Direction.DOWN) == True:
                print(self.HORIZONTAL_WALL, end = "")
            else:
                print(self.HORIZONTAL_WALL_EMPTY, end = "")
        print(self.PILLAR)

    ## 미로 밖 좌표인지 확인하는 함수
    def out_of_maze(self, row, col):
        if row < 0 or row > self.maze_size-1 or col < 0 or col > self.maze_size-1:
            return True
        return False

# 직접 실행할때만 동작하는 실행코드
if __name__ == "__main__":
    maze1 = Maze(int(input("미로 크기를 입력하세요: ")))
    maze1.print_maze()