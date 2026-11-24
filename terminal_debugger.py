from maze import Maze
from player import Player

class TerminalDebugger:
    def __init__(self, maze:Maze, player:Player):
        self.maze = maze
        self.player = player
    
    def print_turn_count(self):
        print("현재 턴수: ", end ="")
        print(self.maze.turn)
    
    def print_player_stick_num(self):
        print("현재 플레이어가 소유한 막대기 수: ", end = "")
        print(self.player.stick_num)
    
    def print_player_score(self):
        print("현재 플레이어 점수: ", end = "")
        print(self.player.score)
    
    def print_stage_num(self):
        print("현재 스테이지: ", end = "")
        print(self.maze.stage)