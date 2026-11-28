# 미로의 기본 틀을 만드는 소스 파일. n * n 격자를 생성함.
from enum import IntEnum, Enum
import random

# 방향
class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

# 벽 종류
class Wall(IntEnum):
    EMPTY  = 0 # bool로 치면 False
    WALL = 1 # bool로 치면 True
    FENCE = 2 # bool로 치면 True
    
# 조작 모드(이동, 칸선택, 방향 선택)
class Mode(Enum):
    MOVE = 0
    SELECT = 1
    DIR = 2

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
        # 수평 벽 리스트 (maze_size+1 * maze_size), 0: 벽 없음, True(1): 벽 있음, True(2): 울타리 있음.
        self._horizontal_wall_list = []
        # 수직 벽 리스트 (maze_size * maze_size+1), 0: 벽 없음, True(1): 벽 있음, True(2): 울타리 있음.
        self._vertical_wall_list = []
        
        # maze_generator가 미로의 생성 시작 위치를 저장할 것임.
        self.start_row = None
        self.start_col = None
        
        # 현재 턴 수
        self.turn:int = 0
        # 현재 스테이지 번호
        self.stage:int = 1
        
        # 플레이어 시작 위치의 면 방향
        self.player_start_point_side_dir:Direction = None
        # 플레이어의 시작 위치
        self.player_start_point:tuple = None
        # 미로 출구 위치이 면 방향(= 야생동물의 스폰 위치 면 방향)
        self.exit_point_side_dir:Direction = None
        # 미로의 출구 위치
        self.exit_point:tuple = None
        # 야생동물 스폰 위치 후보 리스트
        self.candidate_wildlife_spawn_point:set = None
        # 야생동물 객체를 담는 리스트
        self.wildlife_list = []
        
        
        # 미로의 모드를 이동 모드로 초기화
        self.mode = Mode.MOVE
        
        self.make_horizontal_wall_list()
        self.make_vertical_wall_list()
    
    # 생성자에 있는 작업을 그대로 다시 수행함
    def reset(self):
        """생성자에 있는 작업을 그대로 다시 수행함"""
        if self.maze_size <= 0:
            raise ValueError("maze_size 값은 0이하 일수 없습니다. 변수값을 수정해주세요.")
        self._horizontal_wall_list = []
        self._vertical_wall_list = []
        
        self.start_row = None
        self.start_col = None
        
        self.turn:int = 0
        # 현재 스테이지 번호 <- 얘는 초기화하면 안됨
        # self.stage:int = 1
        
        self.player_start_point_side_dir:Direction = None
        self.player_start_point:tuple = None
        self.exit_point_side_dir:Direction = None
        self.exit_point:tuple = None
        self.wildlife_list = []
        
        # 미로의 모드도 초기화하면 안됨.
        # self.mode = Mode.MOVE
        
        self.make_horizontal_wall_list()
        self.make_vertical_wall_list()

    ## 수평 벽 정보 리스트 만드는 함수
    def make_horizontal_wall_list(self):
        """수평 벽 존재 여부 정보 담는 2차원 리스트"""
        for i in range(self.maze_size+1):
            row = []
            for j in range(self.maze_size):
                row.append(Wall.WALL)
            self._horizontal_wall_list.append(row)

    ## 수직 벽 정보 리스트 만드는 함수
    def make_vertical_wall_list(self):
        """수직 벽 존재 여부 정보 담는 2차원 리스트"""
        for i in range(self.maze_size):
            row = []
            for j in range(self.maze_size+1):
                row.append(Wall.WALL)
            self._vertical_wall_list.append(row)

    ## 수평 벽 정보 출력 함수
    def print_horizontal_wall_list(self):
        """수평 벽 리스트 출력 함수"""
        for i in range(self.maze_size+1):
            for j in range(self.maze_size):
                print(self._horizontal_wall_list[i][j], end = " ")
            print("")

    ## 수직 벽 정보 출력 함수
    def print_vertical_wall_list(self):
        """수직 벽 리스트 출력 함수"""
        for i in range(self.maze_size):
            for j in range(self.maze_size+1):
                print(self._vertical_wall_list[i][j], end = " ")
            print("")

    ## 벽 존재 여부 판단 함수
    def is_there_wall(self, row:int, col:int, d:Direction, virtual_fence_point:tuple = None, virtual_fence_dir:Direction = None):
        """- row, col 위치에서, d 방향에 벽이 있는지 확인하여 반환함
        - 가상의 울타리를 고려할 경우 virtal 인자를 쓰면 됨. 않 넣으면 현 미로 상태 기반으로만 벽 판단."""
        if self.out_of_maze(row, col):
            raise ValueError("잘못된 위치: 미로 밖")
        if (row, col) == virtual_fence_point and d == virtual_fence_dir: return Wall.FENCE
        if (row+self.DIR_ROW[d], col+self.DIR_COL[d]) == virtual_fence_point and (d + 2) % 4 == virtual_fence_dir: return Wall.FENCE
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
    def change_wall(self, row:int, col:int, d:Direction, change:int):
        """- 미로의 [row, col]칸에서, dir방향의 벽을 변경하는 함수
        - 0: 벽 없음, 1: 미로 벽, 2: 울타리"""
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

    # 미로의 출구와 플레이어의 위치를 결정하는 함수
    def place_player_and_exit(self):
        # 플레이어가 놓일 미로의 벽면 방향 결정
        self.player_start_point_side_dir = Direction(random.randint(Direction.UP, Direction.LEFT))
        player_random_value = random.randint(0, self.maze_size-1)
        exit_random_value = random.randint(0, self.maze_size-1)
        match self.player_start_point_side_dir:
            # 플레이어의 스폰 벽 방향 반대편에 출구 위치를 결정함
            case Direction.UP:
                # (0, random)위치에 플레이어 시작 위치
                self.player_start_point = (0, player_random_value)
                # (maze_size-1, random)위치에 출구 위치
                self.exit_point = (self.maze_size - 1, exit_random_value)
            case Direction.RIGHT:
                # (random, maze_size-1)
                self.player_start_point = (player_random_value, self.maze_size - 1)
                # (random, 0)
                self.exit_point = (exit_random_value, 0)
            case Direction.DOWN:
                # (maze_size-1, random)
                self.player_start_point = (self.maze_size - 1, player_random_value)
                # (0, random)
                self.exit_point = (0, exit_random_value)
            case Direction.LEFT:
                # (random, 0)
                self.player_start_point = (player_random_value, 0)
                # (random, maze_size-1)
                self.exit_point = (exit_random_value, self.maze_size - 1)
        self.exit_point_side_dir = Direction((self.player_start_point_side_dir + 2) % 4)
    
    # BFS로 A 위치부터 B 위치까지 길이 있는지 확인하는 함수
    def is_having_path(self, search_starting_point:tuple, end_point:tuple, virtual_fence_point:tuple = None, virtual_fence_dir:Direction = None):
        """- BFS로 특정 위치부터 다른 특정 위치까지 길이 있는지 확인하는 함수. 방문할 수 있으면 True, 없으면 False
        - search_starting_point: 탐색 시작 지점. 주로 플레이어 아니면 맹수
        - end_point: 도달하려는 위치, virtual_fence_point과 virtual_fence_dir: 사실상 울타리때문에 있는 인자임. 사용할때만 넣으면 됨"""
        # 방문 후보를 저장하는 큐 자료구조.
        points_que = []
        # 방문한 곳(이미 4방향에 대해 후보 탐색이 끝난 장소)를 저장한 집합. 다음 후보에서 자동 제외됨.
        visitied = set()
        
        # 탐색 시작 위치를 방문 후보 큐와 방문 위치에 추가
        points_que.append(search_starting_point)
        
        # 방문할 후보가 남아있는 동안 계속 반복(중간에 도착 지점을 찾으면 바로 return)
        while points_que:
            # 방문 후보 큐에서 가장 앞에 위치를 뽑아옴
            current_point = points_que.pop(0)
            # 4 방향에 대해서 탐색
            for dir in Direction:
                # 다음 방문할 곳을 일단 변수에 저장
                next_point = (current_point[0] + self.DIR_ROW[dir], current_point[1] + self.DIR_COL[dir])
                # 다음에 갈 곳이 방문했던 곳이 아니고, 해당 방향에 벽이 없다면 방문 후보임. 벽 조회할때 가상의 울타리도 같이 고려함
                if not (next_point[0], next_point[1]) in visitied and not (self.is_there_wall(current_point[0], current_point[1], dir, virtual_fence_point = virtual_fence_point, virtual_fence_dir = virtual_fence_dir)):
                    # 도착지점에 도착했다면 True를 반환함
                    if next_point == end_point: return True
                    # 방문 후보에 추가
                    points_que.append(next_point)
                    # 현 위치를 방문한 곳으로 추가.
                    visitied.add(current_point)
        # 갈 수 있는 모든 곳을 방문했음에도 도착지점에 도달하지 못하면 도달 할 수 없음이라고 판정
        return False

# 직접 실행할때만 동작하는 실행코드
if __name__ == "__main__":
    maze1 = Maze(int(input("미로 크기를 입력하세요: ")))
    maze1.print_maze()