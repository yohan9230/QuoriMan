# 각종 모듈화된 객체들을 이곳에 모아서 최종적으로 실행하는 파이썬 파일. 이곳에서 게임이 돌아갈 것임.
from maze import Maze, Direction
from maze_generator import MazeGenerator
from maze_braider import MazeBraider
from player import Player

from lcd_controller import LCD
from renderer import Renderer
from input_observer import InputObserver

# 변경 가능한 상수
start_icon_margin = 0
player_icon_margin = 4
player_start_facing = Direction.UP
maze_size = 10

def main():
    maze = Maze(maze_size)
    
    start_row, start_col = map(int, input("시작 행, 열 번호 입력(범위: [0,0]~[미로크기-1,미로크기-1], 띄어쓰기로 구분): ").split())
    maze_generator = MazeGenerator(maze, start_row, start_col)
    if maze_generator.generate_maze():
        print("MazeGenerator: 미로 생성 성공")
    
    maze_braider = MazeBraider(maze)
    if maze_braider.braid_maze():
        if maze_braider.check_there_is_no_dead_end():
            print("MazeBraider: 막다른 길 제거 성공")
        else:
            print("MazeBraider: 막다른 길 제거 실패")
    
    player = Player(maze, start_row = start_row, start_col = start_col, facing = player_start_facing)
    
    maze_renderer = Renderer(maze, player = player, player_margin = player_icon_margin, start_point_icon_margin = start_icon_margin)
    # 
    maze_image = maze_renderer.draw_maze()
    
    # 렌더링한 이미지를 LCD에 출력하기 위한 LCD 객체 생성
    lcd_controller = LCD()
    lcd_controller.show_the_image(maze_image)


if __name__ == "__main__":
    main()