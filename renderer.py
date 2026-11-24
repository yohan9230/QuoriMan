# LCD에 렌더링 해주는 객체를 정의한 파일
# 미로 등 모든 렌더링 작업은 여기서 진행함
# 반대로 미로를 만들거나, LCD를 직접 사용하지 않음.

# 임의로 정하는 규칙: 미로 칸에 대해서 그림을 그릴때 기준은 픽셀 기준은 왼쪽 상단의 기둥으로 한다.
# 예를 들어서, (0,0) 칸의 렌더링 기준은 왼쪽 상단의 기둥이므로, (self.start_x, self.start_y) 가 된다.

# PIL: 파이썬에서 그림을 만들고, 읽고, 고치고, 저장 할 수 있게 해주는 라이브러리
from PIL import Image, ImageDraw
# 그릴 객체 관련 소스파일 전부 import
from maze import Maze, Direction
from player import Player
from item_dropper import ItemDropper

class Renderer:
    screen_width:int
    screen_height:int
    cell_size:int
    wall_thickness:int
    start_x:int
    start_y:int
    background_color:tuple
    wall_color:tuple
    maze:Maze
    player:Player
    
    start_point_icon:bool
    player_icon:bool
    stick_icon:bool

    player_icon_margin:int
    start_point_icon_margin:int
    stick_icon_margin:int
    
    def __init__(self, maze:Maze, player:Player, item_dropper:ItemDropper):
        self.maze = maze
        self.player = player
        self.item_dropper = item_dropper
        
        # -----------------------------------------------------
        # 상수
        # 화면 가로, 세로 크기(픽셀)
        self.screen_width = 240
        self.screen_height = 240
        # 벽 포함 미로 한 칸의 크기
        self.cell_size = 22
        # 한 칸 안에서 차지하는 벽의 두께
        self.wall_thickness = 1
        
        # -----------------------------------------------------
        # 아이콘 그리기 여부
        self.start_point_icon:bool = False
        self.player_icon:bool = False
        self.stick_icon:bool = False
        self.exit_icon:bool = False
        
        # 여백
        self.player_icon_margin:int = None
        self.start_point_icon_margin:int = None
        self.stick_icon_margin:int = None
        self.exit_icon_margin:int = None
        
        # 미로 그림 시작 지점. 모든 그림의 시작지점은 왼쪽 상단으로 고정
        self.start_x = 10
        self.start_y = 20
        
        # 배경색 및 벽 색
        self.background_color = (0,0,0)
        self.wall_color = (255, 255, 255)
        
        # 배경 이미지와 해당 배경위에 그림을 그릴 수 있는 "브러시" 객체 생성
        self.maze_image = Image.new("RGB",(self.screen_width, self.screen_height), self.background_color)
        self.maze_brush = ImageDraw.Draw(self.maze_image)
    
    # (row, col) 위치의 미로 칸의 렌더링 기준점(왼쪽 상단 기둥)의 좌표를 리스트로 반환
    def find_pillar_anchor_point(self, row:int, col:int):
        """(row, col) 위치의 미로 칸의 렌더링 기준점(왼쪽 상단 기둥)의 좌표를 리스트로 반환"""
        return [self.start_x + self.cell_size*col, self.start_y + self.cell_size * row]
    
    # (row, col) 위치의 미로 칸의 벽 제외 내부 렌더링 기준점의 좌표를 리스트로 반환
    def find_inner_anchor_point(self, row:int, col:int, margin:int = 0):
        """(row, col) 위치의 미로 칸의 벽 제외 내부 렌더링 기준점의 좌표를 리스트로 반환"""
        pillar_anchor_point = self.find_pillar_anchor_point(row, col)
        return [pillar_anchor_point[0] + self.wall_thickness + margin, 
                pillar_anchor_point[1] + self.wall_thickness + margin]
    
    # 불가능한 시작/끝 좌표가 없는지 확인하는 함수. 문제 없을시 True 반환
    def is_point_calculation_correct(self, points:list):
        """불가능한 시작/끝 좌표가 없는지 확인하는 함수. 문제 없을시 True 반환"""
        [start_x, start_y, end_x, end_y] = points
        if start_x > end_x or start_y > end_y:
            return False
        return True
    
    
    # 미로 한칸의 상단 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수
    def return_up_wall_points(self, pillar_anchor:list):
        """미로 한칸의 상단 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수"""
        start_x = pillar_anchor[0]
        start_y = pillar_anchor[1]
        end_x = pillar_anchor[0] + self.cell_size - 1
        end_y = pillar_anchor[1] + self.wall_thickness - 1
        points = [start_x, start_y, end_x, end_y]
        if self.is_point_calculation_correct(points):
            return points
        else:
            raise RuntimeError("Renderer: 상단 벽 렌더링 좌표가 잘못 계산되었습니다.")
    
    # 미로 한칸의 우측 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수
    def return_right_wall_points(self, pillar_anchor:list):
        """미로 한칸의 우측 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수"""
        start_x = pillar_anchor[0]+self.cell_size-1-(self.wall_thickness-1)
        start_y = pillar_anchor[1]
        end_x = pillar_anchor[0]+self.cell_size-1
        end_y = pillar_anchor[1]+self.cell_size-1
        points = [start_x, start_y, end_x, end_y]
        if self.is_point_calculation_correct(points):
            return points
        else:
            raise RuntimeError("Renderer: 우측 벽 렌더링 좌표가 잘못 계산되었습니다.")
    
    # 미로 한칸의 하단 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수
    def return_down_wall_points(self, pillar_anchor:list):
        """미로 한칸의 하단 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수"""
        start_x = pillar_anchor[0]
        start_y = pillar_anchor[1]+self.cell_size-1-(self.wall_thickness-1)
        end_x = pillar_anchor[0]+self.cell_size-1
        end_y = pillar_anchor[1]+self.cell_size-1
        points = [start_x, start_y, end_x, end_y]
        if self.is_point_calculation_correct(points):
            return points
        else:
            raise RuntimeError("Renderer: 하단 벽 렌더링 좌표가 잘못 계산되었습니다.")
    
    # 미로 한칸의 좌측 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수
    def return_left_wall_points(self, pillar_anchor:list):
        """미로 한칸의 좌측 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수"""
        start_x = pillar_anchor[0]
        start_y = pillar_anchor[1]
        end_x = pillar_anchor[0]+(self.wall_thickness-1)
        end_y = pillar_anchor[1]+self.cell_size-1
        points = [start_x, start_y, end_x, end_y]
        if self.is_point_calculation_correct(points):
            return points
        else:
            raise RuntimeError("Renderer: 좌측 벽 렌더링 좌표가 잘못 계산되었습니다.")
    
    
    # 벽 내부 공간의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수
    def return_inner_cell_points(self, pillar_anchor:list, margin:int = 0):
        """벽 내부 공간의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수"""
        start_x = pillar_anchor[0] + self.wall_thickness + margin
        start_y = pillar_anchor[1] + self.wall_thickness + margin
        end_x = pillar_anchor[0] + (self.cell_size-1) - self.wall_thickness - margin
        end_y = pillar_anchor[1] + (self.cell_size-1) - self.wall_thickness - margin
        inner_points = [start_x, start_y, end_x, end_y]
        if self.is_point_calculation_correct(inner_points):
            return inner_points
        else:
            raise RuntimeError("Renderer: 벽을 제외한 내부 공간의 렌더링 좌표가 잘못 계산되었습니다.")
    
    # row, col 칸에서 상/하/좌/우 벽을 렌더링 하는 함수. 벽 없으면 색칠 안함. 방향 지정시 해당 벽만 렌더링함
    def draw_wall(self, row:int, col:int, dir:Direction = None):
        """row, col 칸에서 상/하/좌/우 벽을 렌더링 하는 함수. 벽 없으면 색칠 안함. 방향 지정시 해당 벽만 렌더링함"""
        # 특정 방향을 지정하지 않았다면, 모든 방향에 대해 벽 렌더링 수행
        pillar_anchor = self.find_pillar_anchor_point(row, col)
        match dir:
            case None:
                for d in Direction:
                    self.draw_wall(row, col, d)
            case Direction.UP:
                if self.maze.is_there_wall(row, col, Direction.UP): 
                    self.maze_brush.rectangle(self.return_up_wall_points(pillar_anchor), fill = self.wall_color)
            case Direction.RIGHT:
                if self.maze.is_there_wall(row, col, Direction.RIGHT): 
                    self.maze_brush.rectangle(self.return_right_wall_points(pillar_anchor), fill = self.wall_color)
            case Direction.DOWN:
                if self.maze.is_there_wall(row, col, Direction.DOWN): 
                    self.maze_brush.rectangle(self.return_down_wall_points(pillar_anchor), fill = self.wall_color)
            case Direction.LEFT:
                if self.maze.is_there_wall(row, col, Direction.LEFT): 
                    self.maze_brush.rectangle(self.return_left_wall_points(pillar_anchor), fill = self.wall_color)
            case _:
                raise ValueError("Renderer: 렌더링 할 수 없는 벽 방향입니다.")
    
    # 미로 생성 시작지점에 파란색 사각형을 그림. 반환값 없음
    def _draw_start_point_icon(self):
        """미로 생성 시작지점에 파란색 사각형을 그림. 반환값 없음"""
        pillar_anchor = self.find_pillar_anchor_point(self.maze.start_row, self.maze.start_col)
        points = self.return_inner_cell_points(pillar_anchor, margin=self.start_point_icon_margin)
        self.maze_brush.rectangle(points, fill = "blue")
        
    # 최종적으로 모든 칸의 벽을 렌더링 하도록 하는 함수. LCD 출력은 안함. maze_image 이미지 반환
    def draw_maze(self):
        """- 최종적으로 모든 칸의 벽을 렌더링 하는 함수. 
        - LCD 출력은 안함. 
        - maze_image 이미지 반환"""
        # 배경을 그리기 전, 기본 배경으로 초기화
        self.maze_brush.rectangle((0, 0, self.screen_width-1, self.screen_height-1), self.background_color)
        maze_size = self.maze.maze_size
        for row in range(maze_size):
            for col in range(maze_size):
                self.draw_wall(row, col)
        # 그리는 순서: 시작 지점 -> 출구 -> 막대기 -> 플레이어
        if self.start_point_icon: self._draw_start_point_icon()
        if self.exit_icon: self._draw_exit()
        if self.stick_icon: self._draw_stick()
        if self.player_icon: self._draw_player()
        return self.maze_image

    # 각 렌더링 객체를 그릴지 설정하는 함수
    def set_rendering_icons(self, draw_start_point_icon:bool, draw_player:bool, draw_stick:bool, draw_exit:bool):
        """각 렌더링 객체를 그릴지 설정하는 함수"""
        self.start_point_icon = draw_start_point_icon
        self.player_icon = draw_player
        self.stick_icon = draw_stick
        self.exit_icon = draw_exit
    
    # 각 렌더링 해야하는 객체의 여백을 설정하는 함수
    def set_rendering_icons_margin(self, start_point_icon_margin:int, player_icon_margin:int, stick_icon_margin:int, exit_icon_margin:int):
        """각 렌더링 해야하는 객체의 여백을 설정하는 함수"""
        self.start_point_icon_margin = start_point_icon_margin
        self.player_icon_margin = player_icon_margin
        self.stick_icon_margin = stick_icon_margin
        self.exit_icon_margin = exit_icon_margin
    

    # -----------------------------------------------------

    # 플레이어를 렌더링 하는 함수
    def _draw_player(self):
        """플레이어를 렌더링 하는 함수"""
        pillar_anchor_point = self.find_pillar_anchor_point(self.player.current_row, self.player.current_col)
        inner_points = self.return_inner_cell_points(pillar_anchor_point, margin = self.player_icon_margin)
        self.maze_brush.ellipse(inner_points, fill = "red")
    
    # -----------------------------------------------------
    
    # tuple(row, col)에서 막대기를 렌더링 하는 함수. 혹은 모든 막대기를 렌더링 함
    def _draw_stick(self, pos:tuple = None):
        """막대기를 렌더링 하는 함수"""
        if pos == None:
            if self.item_dropper.stick_points == None:
                raise RuntimeError("Renderer: ItemDropper: 막대기 위치를 전달받지 못해 막대기를 렌더링 할 수 없습니다.")
            for point in self.item_dropper.stick_points:
                self._draw_stick(point)
        else:
            (row, col) = pos
            if not (type(row) == int and type(col) == int):
                raise ValueError("Rendere: 잘못된 좌표값")
            pillar_anchor = self.find_pillar_anchor_point(row, col)
            inner_points = self.return_inner_cell_points(pillar_anchor = pillar_anchor, margin = self.stick_icon_margin)
            self.maze_brush.ellipse(inner_points, fill = "brown")
    
    # -----------------------------------------------------
    
    # 출구를 렌더링 하는 함수.
    def _draw_exit(self):
        """출구를 렌더링 하는 함수"""
        point = self.maze.exit_point
        pillar_anchor = self.find_pillar_anchor_point(point[0], point[1])
        inner_points = self.return_inner_cell_points(pillar_anchor = pillar_anchor, margin = self.exit_icon_margin)
        self.maze_brush.rectangle(inner_points, fill = "green")

# -----------------------------------------------------
# LCD에 직접 미로를 띄움

if __name__ == "__main__":
    from maze_generator import MazeGenerator
    from maze_braider import MazeBraider
    from lcd_controller import LCD
    
    stick_num = 1
    
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
        else:
            print("MazeBraider: 막다른 길 제거 실패")
    
    maze.place_player_and_exit()
    
    player = Player(maze = maze)
    
    item_dropper = ItemDropper(stage_stick_num = stick_num, player = player, maze = maze)
    item_dropper.decide_stick_pos(stick_num)
    
    maze_renderer = Renderer(maze = maze, player = player, item_dropper = item_dropper)
    maze_renderer.set_rendering_icons(draw_start_point_icon=True, draw_player=True, draw_stick=True, draw_exit = True)
    maze_renderer.set_rendering_icons_margin(start_point_icon_margin = 0, player_icon_margin = 2, stick_icon_margin = 7, exit_icon_margin = 0)
    maze_image = maze_renderer.draw_maze()
    
    # 렌더링한 이미지를 LCD에 출력하기 위한 LCD 객체 생성
    lcd_controller = LCD()
    lcd_controller.show_the_image(maze_image)