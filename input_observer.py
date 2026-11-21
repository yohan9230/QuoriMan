# 조이스틱 및 5,6번 버튼 신호를 읽어서 반환하는 객체 정의
import board
import digitalio

from maze import Direction

class InputObserver:
    def __init__(self):
        # 조이스틱 신호 입력을 받는 객체를 각 변수에 저장
        # 모두 입력 모드로 설정함
        # 눌려있을때 False, 안눌려 있을때 True 값을 가짐.
        self.joystick_up_pin = digitalio.DigitalInOut(board.D17)
        self.joystick_up_pin.switch_to_input(pull=digitalio.Pull.UP)
        self.joystick_right_pin = digitalio.DigitalInOut(board.D23)
        self.joystick_right_pin.switch_to_input(pull=digitalio.Pull.UP)
        self.joystick_down_pin = digitalio.DigitalInOut(board.D22)
        self.joystick_down_pin.switch_to_input(pull=digitalio.Pull.UP)
        self.joystick_left_pin = digitalio.DigitalInOut(board.D27)
        self.joystick_left_pin.switch_to_input(pull=digitalio.Pull.UP)
        
        # 5번 버튼과 6번 버튼 핀
        # 모두 입력 모드로 설정함
        # 눌려있을때 False, 안눌려 있을때 True 값을 가짐.
        self.five_button_pin = digitalio.DigitalInOut(board.D5)
        self.five_button_pin.switch_to_input(pull=digitalio.Pull.UP)
        self.six_button_pin = digitalio.DigitalInOut(board.D6)
        self.six_button_pin.switch_to_input(pull=digitalio.Pull.UP)
        
    # 눌렸을때와 안눌렸을때 bool 값이 헷갈려서 뒤집는 함수 선언. 신호는 반드시 이 함수로만 호출할 것.
    def _is_pressed(self, pin:digitalio.DigitalInOut):
        """- 눌렸을때와 안눌렸을때 bool 값이 헷갈려서 뒤집는 함수 선언. 
        - 신호는 반드시 이 함수로만 호출할 것."""
        return not pin.value
        
    # 위, 오른쪽, 아래, 왼쪽을 순서대로 눌려있는지 확하여 눌린 방향을 반환. 없으면 None 반환
    def read_dirction_from_joystick(self):
        """위, 오른쪽, 아래, 왼쪽을 순서대로 눌려있는지 확하여 눌린 방향을 반환. 없으면 None 반환"""
        if self._is_pressed(self.joystick_up_pin): return Direction.UP
        elif self._is_pressed(self.joystick_right_pin): return Direction.RIGHT
        elif self._is_pressed(self.joystick_down_pin): return Direction.DOWN
        elif self._is_pressed(self.joystick_left_pin): return Direction.LEFT
        else: return None
    
    def read_five_button(self):
        return self._is_pressed(self.five_button_pin)
    
    def read_six_button(self):
        return self._is_pressed(self.six_button_pin)
    
# -----------------------------------------------------

if __name__ == "__main__":
    import time
    
    tmp_joystick = InputObserver()
    
    while True:
        # 매 검사마다 0.1초씩 대기
        time.sleep(0.1)
        dir = tmp_joystick.read_dirction_from_joystick()
        if dir != None:
            print(dir.name)
        if tmp_joystick.read_five_button():
            print("5번 버튼 눌림")
        if tmp_joystick.read_six_button():
            print("6번 버튼 눌림. 테스트 종료")
            break