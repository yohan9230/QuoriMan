from maze import Direction, Maze
import random

class MazeGenerator():
    DIR_ROW = [-1, 0, 1, 0]
    DIR_COL = [0, 1, 0, -1]
    
    current_row:int
    current_col:int
    maze:Maze
    
    def __init__(self, start_row:int, start_col:int, maze:Maze):
        if maze.out_of_maze(start_row, start_col) == True:
            raise ValueError("MazeGenerator: 시작 위치가 잘못되었습니다.")
        self.current_row = start_row
        self.current_col = start_col
        self.maze = maze
        # 방문 여부를 표현하는 2차원 bool 기반 리스트
        self.visitied = []
        # 방문한 위치를 기록하는 스택
        self.visitied_pos_stack = []
        self.make_visitied()
        # 시작 위치를 방문 처리
        self.visitied[start_row][start_col] = True
        # 사직 위치 스택에 넣기
        self.visitied_pos_stack.append([start_row, start_col])
    
    # 방문한 곳을 표시하는 2차원 리스트를 생성하는 함수
    def make_visitied(self):
        """미로에서, 방문한 곳을 표시하는 2차원 리스트를 생성하는 함수"""
        for i in range(self.maze.maze_size):
            tmp_list = []
            for j in range(self.maze.maze_size):
                tmp_list.append(False)
            self.visitied.append(tmp_list)
    
    # [row, col] 위치로 미로 생성자가 방문하도록 하는 함수
    def move_pos(self, row:int, col:int):
        """[row, col] 위치로 미로 생성자가 방문하도록 하는 함수"""
        if self.visitied[row][col] == True:
            raise RuntimeError("MazeGenerator: 방문한 곳을 또 방문할 수 없습니다. DFS 미로 만들기 알고리즘을 수정하세요.")
        self.visitied[row][col] = True
        self.visitied_pos_stack.append([row, col])
        self.current_row = row
        self.current_col = col
    
    # 현 위치에서 다음으로 갈 방향을 결정하여 방향 후보를 리스트로 반환하는 함수
    def find_candidate_next_dir(self):
        """현 위치에서 다음으로 갈 방향을 결정하여 방향 후보를 리스트로 반환하는 함수"""
        candidate_dir = []
        for dir in range(len(Direction)):
            next_row = self.current_row+self.DIR_ROW[dir]
            next_col = self.current_col+self.DIR_COL[dir]
            if self.maze.out_of_maze(next_row, next_col) == False:
                if self.visitied[next_row][next_col] == False:
                    candidate_dir.append(Direction(dir))
        return candidate_dir

    # 현 위치에서 특정 방향의 벽을 부수는 함수
    def call_wall_breaker(self, dir:Direction):
        """MazeGenerator의 현 위치에서 특정 방향의 벽을 부수는 함수"""
        if self.maze.out_of_maze(self.current_row+self.DIR_ROW[dir], self.current_col+self.DIR_COL[dir]) == True:
            raise RuntimeError("WallBreaker: 부술수 없는 벽을 부술려 하고 있습니다.")
        if self.maze.is_there_wall(self.current_row, self.current_col, dir) == False:
            raise RuntimeError("WallBreaker: 부술 벽이 없습니다.")      
        self.maze.change_wall(self.current_row, self.current_col, dir, False)
    
    # 가려는 방향을 정하고, 그쪽 방향의 벽을 부수고 MazeGenerator가 이동함.
    def remove_wall_and_move(self):
        candidate_dir = self.find_candidate_next_dir()
        if not candidate_dir:
            return
        next_dir = random.choice(candidate_dir)
        self.call_wall_breaker(next_dir)
        self.move_pos(self.current_row+self.DIR_ROW[next_dir], self.current_col+self.DIR_COL[next_dir])
        
        