# 플레이어 객체를 정의한 파일.

from maze import Maze, Direction

class Player:
    maze:Maze
    
    current_row:int
    current_col:int
    facing:Direction
    
    stick_num:int
    
    def __init__(self, maze:Maze, facing:Direction = Direction.UP):
        # 플레이어가 속한 미로 객체를 받음
        self.maze = maze
        # 플레이어의 위치를 저장하는 변수들
        self.current_row:int = self.maze.player_start_point[0]
        self.current_col:int = self.maze.player_start_point[1]
        
        # 플레이어가 현재 바라보고 있는 방향을 저장함
        self.facing = facing
        
        # 플레이어가 가진 막대기 수 초기화
        self.stick_num = 0
        
        # 플레이어 점수
        self.score = 0
    
    # 플레이어의 위치를 변경하는 함수
    def move(self, dir:Direction):
        """- 플레이어의 위치를 변경하는 함수
        - 움직이기 실패면 False, 성공이면 True 반환"""
        # 벽 있으면 움직이기 실패
        if self.maze.is_there_wall(self.current_row, self.current_col, dir):
            return False
        # 벽 없으면 움직이고 True 반환
        else:
            self.current_row += self.maze.DIR_ROW[dir]
            self.current_col += self.maze.DIR_COL[dir]
            self.facing = dir
            return True
    
    # 플레이어가 출구에 도착했는지 확인하는 함수
    def is_player_arrived_exit(self):
        """- 플레이어가 출구에 도착했는지 확인하는 함수
        - 도착했으면 True, 아직 도착 안했으면 False 반환"""
        return (self.current_row, self.current_col) == self.maze.exit_point
        
        
# -----------------------------------------------------

if __name__ == "__main__":
    from maze_generator import MazeGenerator
    from maze_braider import MazeBraider
    import time

    # -----------------------------------------------------
    maze_size = int(input("미로 크기 입력: "))
    maze = Maze(maze_size)
    start_row, start_col = map(int, input("시작 행, 열 번호 입력(범위: [0,0]~[미로크기-1,미로크기-1], 띄어쓰기로 구분): ").split())
    maze_generator = MazeGenerator(maze = maze, start_row = start_row, start_col = start_col)
    if maze_generator.generate_maze():
        print("MazeGenerator: 미로 생성 성공")
    
    maze_braider = MazeBraider(maze)
    if maze_braider.braid_maze():
        if maze_braider.check_there_is_no_dead_end():
            print("MazeBraider: 막다른 길 제거 성공")
            maze.print_maze(start_row, start_col)
        else:
            print("MazeBraider: 막다른 길 제거 실패")

    maze.place_player_and_exit()
    player = Player(maze = maze)
    
    while True:
        print(player.current_row, end = ", ")
        print(player.current_col)
        move_direction = input()
        match move_direction:
            case 'w':
                player.move(Direction.UP)
            case 'd':
                player.move(Direction.RIGHT)
            case 's':
                player.move(Direction.DOWN)
            case 'a':
                player.move(Direction.LEFT)
            case _:
                raise ValueError("Player: 이동할 수 없는 방향입니다.")
        
        
        
        