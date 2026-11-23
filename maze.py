# 미로의 기본 틀을 만드는 소스 파일. n * n 격자를 생성함.
from enum import IntEnum

# 방향
class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

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
    
    DIR_ROW = [-1, 0, 1, 0]
    DIR_COL = [0, 1, 0, -1]
    
    def __init__(self, maze_size:int):
        if maze_size <= 0:
            raise ValueError("maze_size 값은 0이하 일수 없습니다. 변수값을 수정해주세요.")
        self.maze_size = maze_size
        # 수평 벽 리스트 (maze_size+1 * maze_size), True: 벽 있음
        self._horizontal_wall_list = []
        # 수직 벽 리스트 (maze_size * maze_size+1), True: 벽 있음
        self._vertical_wall_list = []
        
        # maze_generator가 미로의 생성 시작 위치를 저장할 것임.
        self.start_row = None
        self.start_col = None
        
        self.turn = 0
        
        self.make_horizontal_wall_list()
        self.make_vertical_wall_list()

    ## 수평 벽 정보 리스트 만드는 함수
    def make_horizontal_wall_list(self):
        """수평 벽 존재 여부 정보 담는 2차원 리스트"""
        for i in range(self.maze_size+1):
            row = []
            for j in range(self.maze_size):
                row.append(True)
            self._horizontal_wall_list.append(row)

    ## 수평 벽 정보 출력 함수
    def print_horizontal_wall_list(self):
        """수평 벽 리스트 출력 함수"""
        for i in range(self.maze_size+1):
            for j in range(self.maze_size):
                print(self._horizontal_wall_list[i][j], end = " ")
            print("")

    ## 수직 벽 정보 리스트 만드는 함수
    def make_vertical_wall_list(self):
        """수직 벽 존재 여부 정보 담는 2차원 리스트"""
        for i in range(self.maze_size):
            row = []
            for j in range(self.maze_size+1):
                row.append(True)
            self._vertical_wall_list.append(row)

    ## 수직 벽 정보 출력 함수
    def print_vertical_wall_list(self):
        """수직 벽 리스트 출력 함수"""
        for i in range(self.maze_size):
            for j in range(self.maze_size+1):
                print(self._vertical_wall_list[i][j], end = " ")
            print("")

    ## 벽 존재 여부 판단 함수
    def is_there_wall(self, row:int, col:int, d:Direction):
        """row, col 위치에서, d 방향에 벽이 있는지 확인하여 반환함"""
        if self.out_of_maze(row, col):
            raise ValueError("잘못된 위치: 미로 밖")
        match d:
            case Direction.UP:
                return self._horizontal_wall_list[row][col]
            case Direction.DOWN:
                return self._horizontal_wall_list[row+1][col]
            case Direction.LEFT:
                return self._vertical_wall_list[row][col]
            case Direction.RIGHT:
                return self._vertical_wall_list[row][col+1]
            case _:
                raise ValueError("벽 조회에 불가능한 방향 조회")

    ## 벽 수정 함수
    def change_wall(self, row:int, col:int, d:Direction, change:bool):
        """미로의 [row, col]칸에서, dir방향의 벽을 변경하는 함수"""
        if self.out_of_maze(row, col):
            raise ValueError("잘못된 위치: 미로 밖")
        match d:
            case Direction.UP:
                self._horizontal_wall_list[row][col] = change
            case Direction.DOWN:
                self._horizontal_wall_list[row+1][col] = change
            case Direction.LEFT:
                self._vertical_wall_list[row][col] = change
            case Direction.RIGHT:
                self._vertical_wall_list[row][col+1] = change
            case _:
                raise ValueError("벽 조회에 불가능한 방향 조회")
    
    ## 미로 출력 함수
    def print_maze(self, start_row:int = None, start_col:int = None):
        """미로 출력 함수"""
        for row in range(self.maze_size):
            # 수평 벽 출력(칸의 위쪽 벽 유무 조회)
            for col in range(self.maze_size):
                print(self.PILLAR, end = "")
                if self.is_there_wall(row, col, Direction.UP):
                    print(self.HORIZONTAL_WALL, end = "")
                else:
                    print(self.HORIZONTAL_WALL_EMPTY, end = "")
            print(self.PILLAR)
            # 수직 벽 출력(칸의 왼쪽 벽 유무 조회)
            for col in range(self.maze_size):
                if self.is_there_wall(row, col, Direction.LEFT):
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
            if self.is_there_wall(row, self.maze_size-1, Direction.RIGHT):
                print(self.VERTICAL_WALL)
            else:
                print(self.VERTICAL_WALL_EMPTY)
        # 가장 마지막 수평 벽 출력
        for col in range(self.maze_size):
            print(self.PILLAR, end = "")
            if self.is_there_wall(self.maze_size-1, col, Direction.DOWN):
                print(self.HORIZONTAL_WALL, end = "")
            else:
                print(self.HORIZONTAL_WALL_EMPTY, end = "")
        print(self.PILLAR)

    ## 미로 밖 좌표인지 확인하는 함수
    def out_of_maze(self, row, col):
        if row < 0 or row > self.maze_size-1 or col < 0 or col > self.maze_size-1:
            return True
        return False
    
    # 현 위치에서 벽 방향을 반환하는 함수
    def find_wall(self, row:int, col:int, discard_outline:bool = False):
        """row, col 위치에서 4방향 모두 벽 존재 여부를 확인하고, 벽 방향을 리스트로 반함"""
        wall_dir_list = []
        # 4가지 방향에 대해서...
        for dir in Direction:
            # 우선 벽이 있는지 확인
            if self.is_there_wall(row, col, dir):
                # 외벽을 카운트 한다면
                if not discard_outline:
                    wall_dir_list.append(dir)
                # 외벽은 벽으로 카운트 하지 않는다면
                else:
                    # 해당 방향이 외벽인지 확인(해당 방향으로 이동시 미로를 탈출한다면 그 벽은 외벽)
                    if self.out_of_maze(row+self.DIR_ROW[dir], col+self.DIR_COL[dir]):
                        continue
                    else:
                        wall_dir_list.append(dir)
        return wall_dir_list
    
    # 현 위치에서 벽 개수를 반환하는 함수
    def count_wall(self, row:int, col:int, discard_outline:bool = False):
        """현 위치에서 벽 개수를 반환하는 함수"""
        return len(self.find_wall(row, col, discard_outline))


# 직접 실행할때만 동작하는 실행코드
if __name__ == "__main__":
    maze1 = Maze(int(input("미로 크기를 입력하세요: ")))
    maze1.print_maze()