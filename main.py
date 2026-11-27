# 각종 모듈화된 객체들을 이곳에 모아서 최종적으로 실행하는 파이썬 파일. 이곳에서 게임이 돌아갈 것임.
from maze import Maze, Direction, Mode
from maze_generator import MazeGenerator
from maze_braider import MazeBraider
from player import Player
from item_dropper import ItemDropper
from cursor import Cursor

from lcd_controller import LCD
from renderer import Renderer
from input_observer import InputObserver

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

## 울타리 하나당 막대기 소모 개수
need_stick_num = 4

## 렌더링 항목 그릴지 여부
draw_start_point_icon = False
draw_player = True
draw_stick = True
draw_exit = True

# 렌더링 아이콘 색
background_color = (0,0,0)
wall_color = (255, 255, 255)
fence_color = "orange"
start_point_icon_color = "blue"
cursor_color = (135, 206, 235)

player_icon_color = "red"
stick_icon_color = "brown"
exit_icon_color = "green"

## 렌더링 아이콘마다 여백 값
start_point_icon_margin = 0
player_icon_margin = 2
stick_icon_margin = 7
exit_icon_margin = 0
# -----------------------------------------------------

# maze를 초기화 하는 함수
def initialize_maze(maze:Maze, player:Player, maze_generator:MazeGenerator, maze_bradier:MazeBraider, item_dropper:ItemDropper, maze_renderer:Renderer, cursor:Cursor,first_using:bool):
    """- 기존 maze 객체를 격자수준부터 다시 만듬.
    - 플레이어 시작 위치, 막대기 위치 등등 모두 초기화
    - 플레이어 객체는 건들지 않음"""
        # 미로 초기화가 첫 호출이라면
    if first_using:
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
            exit_icon_margin = exit_icon_margin)
        # 각 아이콘별 색 설정
        maze_renderer.set_icon_color(
            background_color = background_color,
            wall_color = wall_color,
            fence_color = fence_color,
            start_point_icon_color = start_point_icon_color,
            cursor_color = cursor_color,
            player_icon_color = player_icon_color,
            stick_icon_color = stick_icon_color,
            exit_icon_color = exit_icon_color
        )
    else:
        # 두번째 이상 호출부터면 이전 스테이지의 영향을 받지 않기 위해 일부 객체 초기화
        maze.reset()
        maze_generator.reset()
        maze_bradier.reset()
        item_dropper.reset()
        cursor.reset()
    
    # 플레이어와 출구의 시작 위치 랜덤으로 정해짐(플레이어와 출구의 위치는 항상 정 반대편 면임)
    maze.place_player_and_exit()
    # 미로 생성
    maze_generator.generate_maze()
    
    # 막다른 길을 찾고, 해당 막다른 길의 벽 방향을 리스트로 저장함
    maze_bradier.find_end_pos_and_wall_dir()
    # 막다른 길 후보를 섞음
    maze_bradier.shuffle_dir_list()
    
    # 막다른 길 제거
    maze_bradier.braid_maze()
    # 플레이어의 시작 위치에 플레이어를 둠
    player.stand_player_start_point(maze.player_start_point)
    # 막대기 위치 결정
    item_dropper.decide_stick_pos()

# 미로 이미지를 새로고침 및 LCD에 출력. 플레이어, 막대기 등 모든 객체 포함
def refresh_maze_image(maze_renderer:Renderer, lcd_controller:LCD):
    """미로 이미지를 새로고침 및 LCD에 출력함. 플레이어, 막대기 등 모든 객체 포함"""
    # 미로 이미지 만들기
    maze_image = maze_renderer.draw_maze()
    # 첫 화면 내보내기
    lcd_controller.show_the_image(maze_image)

def main():
    # -----------------------------------------------------
    maze = Maze(maze_size)
    maze_generator = MazeGenerator(maze = maze)
    maze_braider = MazeBraider(maze)
    
    # 칸 선택하는 커서 객체 생성
    cursor = Cursor(maze = maze)
    
    # 플레이어 객체 생성
    player = Player(maze, facing = player_start_facing)
    
    # 아이템 드롭퍼 객체 생성
    item_dropper = ItemDropper(stick_num, player, maze)

    # 렌더링 객체 생성
    maze_renderer = Renderer(maze = maze, player = player, item_dropper = item_dropper, cursor = cursor)

    # 터미널 디버깅 기능이 켜져있다면 import 및 객체 생성
    if print_terminal_debuging:
        from terminal_debugger import TerminalDebugger
        terminal_debugger = TerminalDebugger(maze = maze, player = player)
    
    # 렌더링한 이미지를 LCD에 출력하기 위한 LCD 객체 생성
    lcd_controller = LCD()
    
    # 라즈베리 파이의 입력 신호를 받는 객체 생성
    signal_observer = InputObserver()

    # -----------------------------------------------------
    
    # 미로 최초 초기화
    initialize_maze(
        maze = maze, 
        player = player,
        maze_generator = maze_generator, 
        maze_bradier = maze_braider, 
        item_dropper = item_dropper, 
        maze_renderer = maze_renderer,
        cursor = cursor,
        first_using = True)
    
    # 무한 스테이지 반복
    while True:
        # 미로 이미지를 새로고침 및 LCD에 출력함
        refresh_maze_image(maze_renderer = maze_renderer, lcd_controller = lcd_controller)
        
        if print_terminal_debuging:
            print("-----------------")
            terminal_debugger.print_stage_num()

        # 입력을 주기적으로 감지
        while True:
            refresh_maze_image(maze_renderer = maze_renderer, lcd_controller = lcd_controller)
            time.sleep(0.02)
            # 미로의 모드에 따라 입력의 역할이 달라짐.
            match maze.mode:
                # 미로의 모드가 움직이기라면...
                case Mode.MOVE:
                    # 조이스틱의 움직임이 감지되면(방향 변경이 감지되면) 플레이어 이동
                    if signal_observer.check_direction_changed():
                            # 플레이어가 움직일수 있다면 움직임
                            if player.move(signal_observer.current_direction):
                                # 움직이고 나서, 막대기가 있다면 플레이어 막대기 카운트 + 1
                                if item_dropper.remove_stick():
                                    player.stick_num += 1
                                    player.score += 1
                                maze.turn += 1
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
                    
                    # 5버튼이 눌린것이 감지되면 칸 선택 모드로 변경
                    elif signal_observer.check_five_button_pressed():
                        maze.mode = Mode.SELECT
                        # 커서의 시작 지점을 플레이어의 현 좌표로 설정
                        cursor.point_set((player.current_row, player.current_col))
                        if print_terminal_debuging:
                            print("Mode: 칸 선택 모드로 전환")

                # 미로의 모드가 칸 선택이라면...
                case Mode.SELECT:
                    if signal_observer.check_five_button_pressed():
                        maze.mode = Mode.DIR
                        if print_terminal_debuging:
                            print("Mode: 방향 선택 모드로 전환")

                    elif signal_observer.check_six_button_pressed():
                        maze.mode = Mode.MOVE
                        if print_terminal_debuging:
                            print("Mode: 이동 모드로 전환")
                    
                    elif signal_observer.check_direction_changed():
                        # 커서를 조이스틱 방향으로 이동시킴
                        cursor.move(signal_observer.current_direction)
                        
                case Mode.DIR:
                    if signal_observer.check_five_button_pressed():
                        # 아직 미구현. 칸과 방향을 받아서 울타리를 세우게 해야함
                        if print_terminal_debuging:
                            print("Player: 울타리 설치")
                    elif signal_observer.check_six_button_pressed():
                        maze.mode = Mode.SELECT
                        if print_terminal_debuging:
                            print("Mode: 칸 선택 모드로 전환")
    
        # 스테이지 초기화. 기존 객체를 그대로 전달받음
        initialize_maze(
            maze = maze, 
            player = player,
            maze_generator = maze_generator, 
            maze_bradier = maze_braider, 
            item_dropper = item_dropper, 
            maze_renderer = maze_renderer,
            cursor = cursor, 
            first_using = False)

if __name__ == "__main__":
    main()