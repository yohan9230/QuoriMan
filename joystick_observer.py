# 조이스틱 신호를 읽어서 반환하는 객체 정의
import board
import digitalio

from maze import Direction

class JoystickObserver:
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
        
    # 위, 오른쪽, 아래, 왼쪽을 순서대로 눌려있는지 확하여 눌린 방향을 반환. 없으면 None 반환
    def read_dirction_from_joystick(self):
        """위, 오른쪽, 아래, 왼쪽을 순서대로 눌려있는지 확하여 눌린 방향을 반환. 없으면 None 반환"""
        if not self.joystick_up_pin.value: return Direction.UP
        elif not self.joystick_right_pin.value: return Direction.RIGHT
        elif not self.joystick_down_pin: return Direction.DOWN
        elif not self.joystick_left_pin: return Direction.LEFT
        else: return None