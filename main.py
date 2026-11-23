# 각종 모듈화된 객체들을 이곳에 모아서 최종적으로 실행하는 파이썬 파일. 이곳에서 게임이 돌아갈 것임.
from maze import Maze, Direction
from maze_generator import MazeGenerator
from maze_braider import MazeBraider
from player import Player
from item_dropper import ItemDropper

from lcd_controller import LCD
from renderer import Renderer
from input_observer import InputObserver

import random
import time

# 변경 가능한 상수
start_icon_margin = 0
player_icon_margin = 4
player_start_facing = Direction.UP
maze_size = 10

## 스테이지별로 드랍되는 재료(막대기) 개수 설정
stick_num = 15

def main():
    # -----------------------------------------------------
    maze = Maze(maze_size)
    
    # 미로 시작 위치 랜덤으로 정해짐
    maze_start_row = random.randint(0,maze_size-1)
    maze_start_col = random.randint(0,maze_size-1)
    maze_generator = MazeGenerator(maze = maze, start_row = maze_start_row, start_col = maze_start_col)
    
    # 플레이어 시작 위치 랜덤으로 정해짐
    # 나중에 스폰 위치를 테두리 부분으로 고정 필요
    player_start_row = random.randint(0,maze_size-1)
    player_start_col = random.randint(0,maze_size-1)
    
    if maze_generator.generate_maze():
        print("MazeGenerator: 미로 생성 성공")
    
    maze_braider = MazeBraider(maze)
    if maze_braider.braid_maze():
        if maze_braider.check_there_is_no_dead_end():
            print("MazeBraider: 막다른 길 제거 성공")
        else:
            print("MazeBraider: 막다른 길 제거 실패")
    
    # 플레이어 생성
    player = Player(maze, start_row = player_start_row, start_col = player_start_col, facing = player_start_facing)
    maze_renderer = Renderer(maze, player = player, player_margin = player_icon_margin, start_point_icon_margin = start_icon_margin)
    
    item_dropper = ItemDropper(stick_num, player, maze)
    
    # 미로 이미지 만들기
    maze_image = maze_renderer.draw_maze()
    
    # 렌더링한 이미지를 LCD에 출력하기 위한 LCD 객체 생성
    lcd_controller = LCD()
    # 첫 화면 내보내기
    lcd_controller.show_the_image(maze_image)
    
    # 라즈베리 파이의 입력 신호를 받는 객체 생성
    signal_observer = InputObserver()
    
    # -----------------------------------------------------
    
    current_turn = 0
    while True:
        # 조이스틱의 움직임이 감지되면(방향 변경이 감지되면)
        if signal_observer.check_direction_changed():
            # 플레이어가 움직일수 있다면 움직임
            if player.move(signal_observer.current_direction):
                # 움직이고 나서, 막대기가 있다면 플레이어 막대기 카운트 + 1
                if item_dropper.remove_stick():
                    player.stick_num += 1
                current_turn += 1
                # 플레이어 이동하는 것으로 미로를 재 렌더링함
                maze_image = maze_renderer.draw_maze()
                # 재 렌더링한 미로를 LCD로 출력함
                lcd_controller.show_the_image(maze_image)
                print("현재 턴수: ", end = "")
                print(current_turn)
            
        time.sleep(0.02)
    


if __name__ == "__main__":
    main()