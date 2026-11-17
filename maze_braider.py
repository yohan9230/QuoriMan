# DFS를 기반으로 미로를 만드는 소스 파일. 막다른 길은 존재. 출구/입구 아직 없음.
from maze import Maze
from maze_generator import MazeGenerator
import random

class MazeBraider:
    maze:Maze
    def __init__(self, maze:Maze):
        # 막다른 길 위치를 저장하는 리스트
        self.dead_end_pos = []
        # 막다른 길 위치에 대응하여 벽 방향을 모두 저장하는 리스트
        self.dead_end_dir = []
        self.maze = maze
        # 막다른 길 찾기 함수 호출
        self.find_end_pos_and_wall_dir()
        # 벽 후보 리스트 섞기
        self.shuffle_dir_list()
    
    # row, col에서 막다른 길인지 확인하여 반환하는 함수
    def is_dead_end (self, row:int, col: int):
        """row, col에서 막다른 길인지 확인하여 반환하는 함수"""
        wall_num = self.maze.count_wall(row, col, False)
        if wall_num >= 3:
            return True
        elif wall_num <= 2 and wall_num >= 0:
            return False
        else:
            raise RuntimeError("MazeBraider: 가능할 수 없는 벽 개수")
    
    # 모든 칸의 4방향 벽을 조회 및 막다른 길 및 막다른 길마다 벽 위치 및 방향 저장
    def find_end_pos_and_wall_dir(self):
        """모든 칸의 4방향 벽을 조회 및 막다른 길 위치 및 막다른 길마다 벽 위치 및 방향 저장"""
        self.dead_end_pos.clear()
        self.dead_end_dir.clear()
        for row in range(self.maze.maze_size):
            for col in range(self.maze.maze_size):
                # 한 위치에서 벽이 3개 이상이라면 막다른 길(외벽 포함)
                if self.is_dead_end(row, col):
                    # 막다른 길 좌표 저장
                    self.dead_end_pos.append([row, col])
                    # 막다른 길에서 외벽 제외한 벽 방향 저장
                    self.dead_end_dir.append(self.maze.find_wall(row, col, True))
    
    # 방향 리스트를 섞는 함수
    def shuffle_dir_list(self):
        """- 방향 리스트를 섞는 함수
        - 반환값 없이 바로 적용"""
        for dir_list in self.dead_end_dir:
            random.shuffle(dir_list)
    
    # 최종적으로 막다른 길을 모두 뚫는 함수
    def braid_maze(self):
        """- 막다른 길을 모두 뚫는 함수
        - 반환값 없음"""
        # 모든 막다른 길이 있는 위치에서...
        for index in range(len(self.dead_end_pos)):
            row = self.dead_end_pos[index][0]
            col = self.dead_end_pos[index][1]
            # 마지막으로 부수기전, 다른 곳에서 이미 벽을 부쉈으면 막다른 길이 아니게 되므로 한번 더 확인
            if self.is_dead_end(row, col):
                # 벽 리스트 중 가장 첫번째 방향의 벽을 제거
                breaking_wall_dir = self.dead_end_dir[index].pop(0)
                self.maze.change_wall(row, col, breaking_wall_dir, False)
        return True
        
    # 막다른 길이 없는지 확인하여 반환하는 함수
    def check_there_is_no_dead_end(self):
        """- 막다른 길이 없는지 확인하여 반환하는 함수
        - 막다른 길이 하나라도 있으면 False, 하나도 없다면 True 반환"""
        self.find_end_pos_and_wall_dir()
        if not self.dead_end_dir and not self.dead_end_pos:
            return True
        else:
            return False

# -----------------------------------------------------

if __name__ == "__main__":
    maze_size = int(input("미로 크기 입력: "))
    maze = Maze(maze_size)
    start_row, start_col = map(int, input("시작 행, 열 번호 입력(1행 1열 부터 시작, 띄어쓰기로 구분): ").split())
    start_row = start_row-1
    start_col = start_col-1
    maze_generator = MazeGenerator(start_row, start_col, maze)
    if maze_generator.generate_maze():
        print("MazeGenerator: 미로 생성 성공")
    
    maze_braider = MazeBraider(maze)
    if maze_braider.braid_maze():
        if maze_braider.check_there_is_no_dead_end():
            print("MazeBraider: 막다른 길 제거 성공")
            maze.print_maze(start_row, start_col)
        else:
            print("MazeBraider: 막다른 길 제거 실패")