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

# 터미널 출력 여부(디버깅용)
print_terminal_debuging = True

# -----------------------------------------------------
# 변경 가능한 상수

## 미로 크기
maze_size = 10
## 처음 시작 시 플레이어가 바라보는 방향
player_start_facing = Direction.UP

## 스테이지별로 드랍되는 재료(막대기) 개수 설정
stick_num = 15

## 렌더링 항목 그릴지 여부
draw_start_point_icon = False
draw_player = True
draw_stick = True
draw_exit = True

## 렌더링 아이콘마다 여백 값
start_point_icon_margin = 0
player_icon_margin = 2
stick_icon_margin = 7
exit_icon_margin = 0
# -----------------------------------------------------

def main():
    # -----------------------------------------------------
    maze = Maze(maze_size)
    # 미로 시작 위치 랜덤으로 정해짐
    maze_start_row = random.randint(0,maze_size-1)
    maze_start_col = random.randint(0,maze_size-1)
    
    # 플레이어와 출구의 시작 위치 랜덤으로 정해짐(플레이어와 출구의 위치는 항상 정 반대편 면임)
    maze.place_player_and_exit()
    
    # 미로 생성
    maze_generator = MazeGenerator(maze = maze, start_row = maze_start_row, start_col = maze_start_col)
    maze_generator.generate_maze()
    
    # 막다른 길 제거
    maze_braider = MazeBraider(maze)
    maze_braider.braid_maze()
    
    # 플레이어 생성
    player = Player(maze, facing = player_start_facing)
    
    # 아이템 드롭퍼 객체 생성
    item_dropper = ItemDropper(stick_num, player, maze)
    # 막대기 위치 결정
    item_dropper.decide_stick_pos()

    # 렌더링 객체 생성
    maze_renderer = Renderer(
        maze = maze, 
        player = player, 
        item_dropper=item_dropper)
    # 각 아이콘별로 그릴지 여부를 설정
    maze_renderer.set_rendering_icons(
        draw_start_point_icon = draw_start_point_icon, 
        draw_player = draw_player, 
        draw_stick = draw_stick,
        draw_exit = draw_exit)
    # 각 아이콘별 여백 설정
    maze_renderer.set_rendering_icons_margin(
        start_point_icon_margin = start_point_icon_margin,
        player_icon_margin = player_icon_margin,
        stick_icon_margin = stick_icon_margin,
        exit_icon_margin = exit_icon_margin
    )
    
    # 터미널 디버깅 기능이 켜져있다면 import
    if print_terminal_debuging:
        from terminal_debugger import TerminalDebugger
        terminal_debugger = TerminalDebugger(maze = maze, player = player)
    
    # 미로 이미지 만들기
    maze_image = maze_renderer.draw_maze()
    
    # 렌더링한 이미지를 LCD에 출력하기 위한 LCD 객체 생성
    lcd_controller = LCD()
    # 첫 화면 내보내기
    lcd_controller.show_the_image(maze_image)
    
    # 라즈베리 파이의 입력 신호를 받는 객체 생성
    signal_observer = InputObserver()
    
    # -----------------------------------------------------
    
    maze.turn = 0
    
    if print_terminal_debuging:
        terminal_debugger.print_stage_num()
    
    while True:
        # 조이스틱의 움직임이 감지되면(방향 변경이 감지되면)
        if signal_observer.check_direction_changed():
            # 플레이어가 움직일수 있다면 움직임
            if player.move(signal_observer.current_direction):
                # 움직이고 나서, 막대기가 있다면 플레이어 막대기 카운트 + 1
                if item_dropper.remove_stick():
                    player.stick_num += 1
                    player.score += 1
                maze.turn += 1
                # 플레이어 이동하는 것으로 미로를 재 렌더링함
                maze_image = maze_renderer.draw_maze()
                # 재 렌더링한 미로를 LCD로 출력함
                lcd_controller.show_the_image(maze_image)
                
                # 터미널 디버깅 기능이 켜져있다면
                if print_terminal_debuging:
                    # 턴수 출력
                    terminal_debugger.print_turn_count()
                    # 플레이어의 막대기 수 출력
                    terminal_debugger.print_player_stick_num()
                    # 플레이어의 점수 출력
                    terminal_debugger.print_player_score()
                
                # 플레이어가 출구에 도착하면 움직임 감지를 중지함
                if player.is_player_arrived_exit():
                    maze.stage += 1
                    break
                
        time.sleep(0.02)
    

if __name__ == "__main__":
    main()