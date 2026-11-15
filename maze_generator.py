from maze import Direction, Maze
import random

class MazeGenerator():
    # Direction과 순서가 동일함
    DIR_ROW = [-1, 0, 1, 0]
    DIR_COL = [0, 1, 0, -1]
    
    current_row:int
    current_col:int
    maze:Maze
    
    def __init__(self, start_row:int, start_col:int, maze:Maze):
        if maze.out_of_maze(start_row, start_col):
            raise ValueError("MazeGenerator: 시작 위치가 잘못되었습니다.")
        self.current_row = start_row
        self.current_col = start_col
        self.maze = maze
        # 방문 여부를 표현하는 2차원 bool 기반 리스트
        self.visited = []
        # 방문한 위치를 기록하는 스택
        self.visitied_pos_stack = []
        self.make_visitied()
        # 시작 위치를 방문 처리
        self.visited[start_row][start_col] = True
        # 사직 위치 스택에 넣기
        self.visitied_pos_stack.append([start_row, start_col])
    
    # 방문한 곳을 표시하는 2차원 리스트를 생성하는 함수
    def make_visitied(self):
        """미로에서, 방문한 곳을 표시하는 2차원 리스트를 생성하는 함수"""
        for i in range(self.maze.maze_size):
            tmp_list = []
            for j in range(self.maze.maze_size):
                tmp_list.append(False)
            self.visited.append(tmp_list)
    
    # [row, col] 위치로 미로 생성자가 방문하도록 하는 함수
    def move_pos(self, row:int, col:int):
        """[row, col] 위치로 미로 생성자가 방문하도록 하는 함수"""
        if self.visited[row][col] == True:
            raise RuntimeError("MazeGenerator: 방문한 곳을 또 방문할 수 없습니다. DFS 미로 만들기 알고리즘을 수정하세요.")
        self.visited[row][col] = True
        self.visitied_pos_stack.append([row, col])
        self.current_row = row
        self.current_col = col
    
    # 현 위치에서 다음으로 갈 방향을 결정하여 방향 후보를 리스트로 반환하는 함수
    def find_candidate_next_dir(self):
        """현 위치에서 다음으로 갈 방향을 결정하여 방향 후보를 리스트로 반환하는 함수"""
        candidate_dir = []
        for d in Direction:
            next_row = self.current_row+self.DIR_ROW[d]
            next_col = self.current_col+self.DIR_COL[d]
            if not self.maze.out_of_maze(next_row, next_col):
                if not self.visited[next_row][next_col]:
                    candidate_dir.append(d)
        return candidate_dir

    # 갈수 있는 방향이 없을때 한걸음 뒤로 이동
    def backward(self):
        self.visitied_pos_stack.pop()
        if not self.visitied_pos_stack:
            return
        self.current_row = self.visitied_pos_stack[-1][0]
        self.current_col = self.visitied_pos_stack[-1][1]
    
    # 현 위치에서 특정 방향의 벽을 부수는 함수
    def call_wall_breaker(self, d:Direction):
        """MazeGenerator의 현 위치에서 특정 방향의 벽을 부수는 함수"""
        if self.maze.out_of_maze(self.current_row+self.DIR_ROW[d], self.current_col+self.DIR_COL[d]) == True:
            raise RuntimeError("WallBreaker: 부술수 없는 벽을 부술려 하고 있습니다.")
        if not self.maze.is_there_wall(self.current_row, self.current_col, d):
            raise RuntimeError("WallBreaker: 부술 벽이 없습니다.")      
        self.maze.change_wall(self.current_row, self.current_col, d, False)
    
    # 가려는 방향을 정하고, 그쪽 방향의 벽을 부수고 MazeGenerator가 한칸 이동함.
    def remove_wall_and_move_once(self):
        candidate_dir = self.find_candidate_next_dir()
        while not candidate_dir:
            self.backward()
            if not self.visitied_pos_stack:
                if self.check_all_visitied() == True:
                    return
                else:
                    raise RuntimeError("MazeGenerator: 방문하지 않은 곳이 있는 상태로 끝났습니다. DFS 알고리즘을 수정하세요.")
            candidate_dir = self.find_candidate_next_dir()
        next_dir = random.choice(candidate_dir)
        self.call_wall_breaker(next_dir)
        self.move_pos(self.current_row+self.DIR_ROW[next_dir], self.current_col+self.DIR_COL[next_dir])
    
    # 모든 칸을 방문했는지 알려주는 함수
    def check_all_visitied(self):
        """- 모든 칸을 방문했는지 반환해주는 함수
        - 모두 방문시 True, 한칸이라도 방문하지 않았다면 False 반환"""
        for i in range(self.maze.maze_size):
            if not all(self.visited[i]):
                return False
        return True

    # 위 함수들을 종합하여, 최종적으로 미로를 만드는 함수. 정상 종료시 True를 반환함
    def generate_maze(self):
        while self.visitied_pos_stack:
            self.remove_wall_and_move_once()
        return True
    
# -----------------------------------------------------

if __name__ == "__main__":
    maze_size = int(input("미로 크기 입력: "))
    maze = Maze(maze_size)
    start_row, start_col = map(int, input("시작 행, 열 번호 입력(1행 1열 부터 시작, 띄어쓰기로 구분): ").split())
    start_row = start_row-1
    start_col = start_col-1
    maze_generator = MazeGenerator(start_row, start_col, maze)
    if maze_generator.generate_maze():
        print("미로 생성 성공")
        maze.print_maze(start_row, start_col)