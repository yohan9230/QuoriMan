from maze import Maze, Direction
from player import Player
from enum import Enum
import random

class GoalPointType(Enum):
    FRONTWARD = 0
    BACKWARD = 1
    PLAYER = 2
    
class WildLife():
    def __init__(self, maze:Maze, player:Player, tracking_distance:int):
        self.maze = maze
        self.player = player
        
        self.goal_point_kind:GoalPointType = None
        self.goal_point:tuple = None
        self.tracking_distance:int = tracking_distance
        
        self.current_point:tuple = None
        self.facing:Direction = None
    
    # 스폰 위치로 가능한 좌표들의 리스트를 maze에 저장함
    def find_candidate_spawn_points(self):
        """스폰 위치로 가능한 좌표들의 리스트를 maze에 저장함"""
        spawn_side_dir = self.maze.exit_point_side_dir
        candidate_wildlife_spawn_point = set()
        match spawn_side_dir:
            case Direction.UP:
                row = 0
                for col in range(self.maze.maze_size):
                    if row == self.maze.exit_point[0] and col == self.maze.exit_point[1]: continue
                    candidate_wildlife_spawn_point.add((row, col))
            case Direction.RIGHT:
                col = self.maze.maze_size - 1
                for row in range(self.maze.maze_size):
                    if row == self.maze.exit_point[0] and col == self.maze.exit_point[1]: continue
                    candidate_wildlife_spawn_point.add((row, col))
            case Direction.DOWN:
                row = self.maze.maze_size - 1
                for col in range(self.maze.maze_size):
                    if row == self.maze.exit_point[0] and col == self.maze.exit_point[1]: continue
                    candidate_wildlife_spawn_point.add((row, col))
            case Direction.LEFT:
                col = 0
                for row in range(self.maze.maze_size):
                    if row == self.maze.exit_point[0] and col == self.maze.exit_point[1]: continue
                    candidate_wildlife_spawn_point.add((row, col))
        # 미로에 야생동물이 스폰될 수 있는 위치를 담은 리스트 저장
        self.maze.candidate_wildlife_spawn_point = candidate_wildlife_spawn_point

    # point 좌표에서 벽이 없는 방향 중 랜덤으로 한곳으로 쳐다보도록 하여 야생동물을 스폰시킴
    def _spawn_wildlife(self, point:tuple):
        """point 좌표에서 벽이 없는 방향 중 랜덤으로 한곳으로 쳐다보도록 하여 야생동물을 스폰시킴"""
        self.current_point = point
        candidate_dir = []
        for dir in Direction:
            if not self.maze.is_there_wall(point[0], point[1], dir):
                candidate_dir.append(dir)
        self.facing = random.choice(candidate_dir)
    
    # 최종적으로 야생동물의 스폰 위치를 결정 및 스폰시킴
    def determine_spawn_point_and_spawn(self):
        """- 최종적으로 야생동물의 스폰 위치를 결정 및 스폰시킴"""
        # 후보 위치중 하나를 무작위로 시작 위치로 설정
        self._spawn_wildlife(random.choice(list(self.maze.candidate_wildlife_spawn_point)))
    
    # -----------------------------------------------------
    # 이 야생동물의 목표지점 결정 타입을 지정함
    def set_goal_point_kind(self, goal_type:GoalPointType):
        """이 야생동물의 목표지점 결정 타입을 지정함"""
        self.goal_point_kind = goal_type
    
    # 플레이어 기반 최종 목표 지점을 결정함
    def find_goal_point(self):
        """플레이어 기반 최종 목표 지점을 결정함"""
        if self.goal_point_kind == GoalPointType.FRONTWARD:
            self.goal_point = (self.player.current_row + self.maze.DIR_ROW[self.player.facing] * self.tracking_distance, self.player.current_col + self.maze.DIR_COL[self.player.facing] * self.tracking_distance)
        elif self.goal_point_kind == GoalPointType.BACKWARD:
            self.goal_point = (self.player.current_row + self.maze.DIR_ROW[(self.player.facing + 2) % 4] * self.tracking_distance, self.player.current_col + self.maze.DIR_COL[(self.player.facing + 2) % 4] * self.tracking_distance) 
        elif self.goal_point_kind == GoalPointType.PLAYER:
            self.goal_point = (self.player.current_row, self.player.current_col)
    
    # dir 방향으로 이동했을때 목표 좌표와 야생 동물 사이의 유클리드 거리를 구함
    def calculate_distance_from_player(self, dir:Direction = None):
        """- dir 방향으로 이동했을때 목표 좌표와 야생 동물 사이의 유클리드 거리를 구함
        - 실제로 야싱동물을 이동시키진 않음
        - 방향을 넣지 않으면 현재 야생동물 위치와 플레이어 위치 사이의 유클리드 거리를 구함"""
        if dir != None:
            next_row = self.current_point[0] + self.maze.DIR_ROW[dir]
            next_col = self.current_point[1] + self.maze.DIR_COL[dir]
            return ((self.goal_point[0] - next_row) ** 2 + (self.goal_point[1] - next_col) ** 2) ** (1/2)
        else:
            return ((self.goal_point[0] - self.current_point[0]) ** 2 + (self.goal_point[1] - self.current_point[1]) ** 2) ** (1/2)
    
    # 이동할수 있는 방향을 반환함. 이동할수 있는 방향이 없으면 None 반환
    def determind_dir(self):
        """이동할수 있는 방향을 반환함. 이동할수 있는 방향이 없으면 None 반환"""
        if self.facing == None or self.current_point == None:
            raise RuntimeError("WildLife: 스폰되지 않은 야생동물의 다음 이동 방향을 정하려 합니다.")
        # 다음 이동 방향을 정함(우선 None)
        candidate_dir = []
        min_distance = self.maze.maze_size ** 2
        for dir in Direction:
            # 이번 방향이 뒤를 도는 방향이라면 후보 방향으로 취급하지 않음
            if dir == (self.facing + 2) % 4: continue
            # 이번 방향쪽에 벽 혹은 울타리가 있다변 후보 방향으로 취급하지 않음
            if self.maze.is_there_wall(self.current_point[0], self.current_point[1], dir): continue
            this_time_distance = self.calculate_distance_from_player(dir)
            # 이번 방향이 가장 많이 거리를 줄일 수 있는 방향이라면
            if this_time_distance < min_distance:
                min_distance = this_time_distance
                # 방향 후보 리스트를 초기화 후 이번 방향만 넣음
                candidate_dir = [dir]
            # 이번 방향 역시 가장 많은 거리를 줄일 수 있는 방향 중 하나라면
            elif this_time_distance == min_distance:
                # 방향 후보 리스트에 이번 방향 추가
                candidate_dir.append(dir)
        
        # 방향 후보 리스트가 비어있지 않다면 후보중 하나를 뽑음
        if candidate_dir:
            return random.choice(candidate_dir)
        else:
            return None
    
    # 뒤로 돌게 함(1턴 소모)
    def turn_facing(self):
        """뒤로 돌게 함(1턴 소모)"""
        self.facing = Direction((self.facing + 2) % 4)
    
    # 야생동물을 1턴 움직임
    def move(self, dir:Direction):
        """야생동물을 1턴 움직임"""
        if dir == None:
            raise RuntimeError("WildLife: 이동할수 없는 방향입니다: 방향 = None")
        next_point = (self.current_point[0] + self.maze.DIR_ROW[dir], self.current_point[1] + self.maze.DIR_COL[dir])
        if self.maze.out_of_maze(next_point[0], next_point[1]):
            raise RuntimeError("WildLife: 이동할수 없는 방향입니다: 미로 밖 탈출")
        self.current_point = next_point
        self.facing = dir

# -----------------------------------------------------

# WildLife를 상속받는 곰 객체    
class Bear(WildLife):
    # WildLife 생성자를 호출
    def __init__(self, maze, player, tracking_distance):
        super().__init__(maze, player, tracking_distance)