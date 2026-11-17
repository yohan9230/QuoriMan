from maze import Maze, Direction
import random

class MazeBraider:
    maze:Maze
    def __init__(self, maze:Maze):
        # 막다른 길 위치를 저장하는 리스트
        self.dead_end_pos = []
        # 막다른 길 위치에 대응하여 벽 방향을 모두 저장하는 리스트
        self.dead_end_dir = []
        self.maze = maze
    
    # 모든 칸의 4방향 벽을 조회 및 막다른 길 및 막다른 길마다 벽 위치 및 방향 저장
    def find_end_pos_and_wall_dir(self):
        """모든 칸의 4방향 벽을 조회 및 막다른 길 위치 및 막다른 길마다 벽 위치 및 방향 저장"""
        for row in range(self.maze.maze_size):
            for col in range(self.maze.maze_size):
                # 외벽을 무시하고 벽 개수를 셈
                wall_dir = self.maze.find_wall(row, col, True)
                # 한 위치에서 벽이 3개 이상이라면 막다른 길(외벽 제외)
                if len(wall_dir) >= 3:
                    # 막다른 길 좌표 저장
                    self.dead_end_pos.append([row, col])
                    # 막다른 길에서 외벽 제외한 벽 방향 저장
                    self.dead_end_dir.append(wall_dir)
                # 막다른 길이 아니면 continue
                elif len(wall_dir) <= 2 and len(wall_dir) >= 0:
                    continue
                # -1개 이하 혹은 5개 이상의 벽 개수가 나올 경우 에러
                else:
                    raise RuntimeError("DeadEndRemover: 가능할 수 없는 벽 개수")
    
    # 방향 리스트를 섞는 함수
    def shuffle_dir_list(self):
        """- 방향 리스트를 섞는 함수
        - 반환값 없이 바로 적용"""
        shuffled_dir_list = []
        for dir_list in self.dead_end_dir:
            shuffled_dir_list.append(random.shuffle(dir_list))
        if not len(self.shuffle_dir) == len(shuffled_dir_list):
            raise RuntimeError("MazeBraider: 방향 리스트 섞는 도중 누락된 위치가 생겼습니다.")
        self.shuffle_dir = shuffled_dir_list
    
    
    
                    
        