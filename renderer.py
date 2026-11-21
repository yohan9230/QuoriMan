# LCD에 렌더링 해주는 객체를 정의한 파일
# 미로 등 모든 렌더링 작업은 여기서 진행함
# 반대로 미로를 만들거나, LCD를 직접 사용하지 않음.

# 임의로 정하는 규칙: 미로 칸에 대해서 그림을 그릴때 기준은 픽셀 기준은 왼쪽 상단의 기둥으로 한다.
# 예를 들어서, (0,0) 칸의 렌더링 기준은 왼쪽 상단의 기둥이므로, (self.start_x, self.start_y) 가 된다.

# PIL: 파이썬에서 그림을 만들고, 읽고, 고치고, 저장 할 수 있게 해주는 라이브러리
from PIL import Image, ImageDraw
# 미로: 그릴 대상
from maze import Maze, Direction

class Renderer:
    screen_width:int
    screen_height:int
    cell_size:int
    wall_thickness:int
    start_x:int
    start_y:int
    background_color:tuple
    wall_color:tuple
    
    def __init__(self):
        # 상수
        # 화면 가로, 세로 크기(픽셀)
        self.screen_width = 240
        self.screen_height = 240
        # 벽 포함 미로 한 칸의 크기
        self.cell_size = 22
        # 한 칸 안에서 차지하는 벽의 두께
        self.wall_thickness = 1
        
        # 미로 그림 시작 지점. 모든 그림의 시작지점은 왼쪽 상단으로 고정
        self.start_x = 10
        self.start_y = 20
        
        # 배경색 및 벽 색
        self.background_color = (0,0,0)
        self.wall_color = (255, 255, 255)
    
    # (row, col) 위치의 미로 칸의 렌더링 기준점(왼쪽 상단 기둥)의 좌표를 리스트로 반환
    def find_anchor_pillar_pixel_pos(self, row:int, col:int):
        """(row, col) 위치의 미로 칸의 렌더링 기준점(왼쪽 상단 기둥)의 좌표를 튜플로 반환"""
        return [self.start_x + self.cell_size*col, self.start_y + self.cell_size * row]
    
    # 불가능한 시작/끝 좌표가 없는지 확인하는 함수. 문제 없을시 True 반환
    def is_point_calculation_correct(self, points:list):
        """불가능한 시작/끝 좌표가 없는지 확인하는 함수. 문제 없을시 True 반환"""
        [start_x, start_y, end_x, end_y] = points
        if start_x > end_x or start_y > end_y:
            return False
        return True
    
    # 미로 한칸의 상단 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수
    def return_up_wall_points(self, anchor:list):
        """미로 한칸의 상단 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수"""
        start_x = anchor[0]
        start_y = anchor[1]
        end_x = anchor[0] + self.cell_size - 1
        end_y = anchor[1] + self.wall_thickness - 1
        points = [start_x, start_y, end_x, end_y]
        if self.is_point_calculation_correct(points):
            return points
        else:
            raise RuntimeError("Renderer: 상단 벽 렌더링 좌표가 잘못 계산되었습니다.")
    
    # 미로 한칸의 우측 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수
    def return_right_wall_points(self, anchor:list):
        """미로 한칸의 우측 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수"""
        start_x = anchor[0]+self.cell_size-1-(self.wall_thickness-1)
        start_y = anchor[1]
        end_x = anchor[0]+self.cell_size-1
        end_y = anchor[1]+self.cell_size-1
        points = [start_x, start_y, end_x, end_y]
        if self.is_point_calculation_correct(points):
            return points
        else:
            raise RuntimeError("Renderer: 우측 벽 렌더링 좌표가 잘못 계산되었습니다.")
    
    # 미로 한칸의 하단 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수
    def return_down_wall_points(self, anchor:list):
        """미로 한칸의 하단 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수"""
        start_x = anchor[0]
        start_y = anchor[1]+self.cell_size-1-(self.wall_thickness-1)
        end_x = anchor[0]+self.cell_size-1
        end_y = anchor[1]+self.cell_size-1
        points = [start_x, start_y, end_x, end_y]
        if self.is_point_calculation_correct(points):
            return points
        else:
            raise RuntimeError("Renderer: 하단 벽 렌더링 좌표가 잘못 계산되었습니다.")
    
    # 미로 한칸의 좌측 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수
    def return_left_wall_points(self, anchor:list):
        """미로 한칸의 좌측 벽의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수"""
        start_x = anchor[0]
        start_y = anchor[1]
        end_x = anchor[0]+(self.wall_thickness-1)
        end_y = anchor[1]+self.cell_size-1
        points = [start_x, start_y, end_x, end_y]
        if self.is_point_calculation_correct(points):
            return points
        else:
            raise RuntimeError("Renderer: 좌측 벽 렌더링 좌표가 잘못 계산되었습니다.")
    
    # 벽 내부 공간의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수
    def return_inner_cell_points(self, anchor:list):
        """벽 내부 공간의 좌측 상단, 우측 하단의 좌표를 구하여 반환하는 함수"""
        start_x = anchor[0] + self.wall_thickness
        start_y = anchor[1] + self.wall_thickness
        end_x = anchor[0] + (self.cell_size-1) - self.wall_thickness
        end_y = anchor[1] + (self.cell_size-1) - self.wall_thickness
        points = [start_x, start_y, end_x, end_y]
        if self.is_point_calculation_correct(points):
            return points
        else:
            raise RuntimeError("Renderer: 벽을 제외한 내부 공간의 렌더링 좌표가 잘못 계산되었습니다.")
    
    # row, col 칸에서 상/하/좌/우 벽을 최종적으로 렌더링 하는 함수. 벽 없으면 색칠 안함.
    def draw_wall(self, maze:Maze, anchor:list, dir:Direction):
        
    
    # 최종적으로 미로를 렌더링 하는 함수. LCD 출력은 안함
    def draw_maze(self, maze:Maze):
        """최종적으로 미로를 렌더링 하는 함수. LCD 출력은 안함"""
        maze_size = maze.maze_size
        background = Image.new("RGB",(self.screen_width, self.screen_height), self.background_color)
        maze_brush = ImageDraw.Draw(background)
        
        