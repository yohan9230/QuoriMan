from maze import Maze, Direction

class Cursor:
    maze:Maze
    
    def __init__(self, maze):
        self.maze = maze
        self.current_point:tuple = None
        self.current_dir:Direction = Direction.UP
    
    def reset(self):
        self.current_point = None
        self.current_dir = Direction.UP
    
    # 커서를 point로 옮김
    def point_set(self, point:tuple):
        """- 커서를 point로 옮김"""
        self.current_point = point
    
    # 커서의 위치를 지정된 방향으로 옮김
    def move(self, dir:Direction):
        """- 커서의 위치를 지정된 방향으로 옮김.
        - 미로 밖이면 옮기지 않고 False 반환, 옮기면 True 반환"""
        next_row = self.current_point[0] + self.maze.DIR_ROW[dir]
        next_col = self.current_point[1] + self.maze.DIR_COL[dir]
        
        if self.maze.out_of_maze(next_row, next_col):
            return False
        else:
            self.current_point = (next_row, next_col)
            return True
    
    # 커서의 방향을 설정함
    def set_dir(self, dir:Direction):
        """커서의 방향을 설정함"""
        self.current_dir = dir