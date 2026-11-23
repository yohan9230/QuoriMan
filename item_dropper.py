# 미로에 떨어지는 모든 아이템을 관리하는 객체를 정의한 파일
from maze import Maze
from player import Player
import random

class ItemDropper:
    stick_num:int
    maze:Maze
    points:list
    player:Player
    
    def __init__(self, stage_stick_num:int, player:Player, maze:Maze):
        self.maze = maze
        self.player = player
        
        # 한 스테이지에서 드랍되는 막대기 개수
        self.stick_num = stage_stick_num
        
        # 막대기 위치를 정함
        self.stick_points = None
        self.decide_stick_pos()

    # 플레이어 시작 위치를 제외한 아이템(막대기 등) 드랍 후보 위치를 저장하는 함수
    def find_item_pos_candidate(self):
        """플레이어 시작 위치를 제외한 아이템(막대기) 드랍 후보 위치를 저장하는 함수"""
        points = []
        for row in range(self.maze.maze_size):
            for col in range(self.maze.maze_size):
                # 플레이어 시작 위치는 막대기 드랍 후보에서 제외
                if self.player.current_row == row and self.player.current_col == col:
                    continue
                points.append((row, col))
        return points

    # 해당 위치에 막대기가 있으면 True, 없으면 False 반환
    def is_there_stick(self, point:tuple):
        """해당 위치에 막대기가 있으면 True, 없으면 False 반환"""
        return point in self.stick_points
    
    # 막대기 자리를 정해서 집합으로 저장함
    def decide_stick_pos(self, stick_num:int = None):
        """막대기 자리를 정해서 집합으로 저장함"""
        # 막대기 개수를 전달받지 않았다면 그냥 객체 생성시 받은 막대기 개수를 그대로 사용
        if stick_num == None:
            stick_num = self.stick_num
        stick_points = set(random.sample(self.find_item_pos_candidate(), stick_num))
        self.stick_points = stick_points
    
    # 막대기가 있다면 막대기 위치 집합에서 해당 위치를 지우고, True 반환
    def remove_stick(self, pos_tuple:tuple = None):
        """막대기가 있다면 막대기 위치 집합에서 해당 위치를 지우고, True 반환"""
        if pos_tuple == None:
            pos_tuple = (self.player.current_row, self.player.current_col)
        (row, col) = pos_tuple
        if not (type(row) == int and type(col) == int):
            raise ValueError("ItemDropper: 가능하지 않는 플레이어 위치값")
        if self.is_there_stick((row, col)):
            self.stick_points.remove((row, col))
            return True
        else:
            return False