# 조이스틱 및 5,6번 버튼 신호를 읽어서 반환하는 객체 정의
import board
import digitalio

from maze import Direction

class InputObserver:
    def __init__(self):
        # 조이스틱 신호 입력을 받는 객체를 각 변수에 저장
        # 모두 입력 모드로 설정함
        # 눌려있을때 False, 안눌려 있을때 True 값을 가짐.
        self._joystick_up_pin = digitalio.DigitalInOut(board.D17)
        self._joystick_up_pin.switch_to_input(pull=digitalio.Pull.UP)
        self._joystick_right_pin = digitalio.DigitalInOut(board.D23)
        self._joystick_right_pin.switch_to_input(pull=digitalio.Pull.UP)
        self._joystick_down_pin = digitalio.DigitalInOut(board.D22)
        self._joystick_down_pin.switch_to_input(pull=digitalio.Pull.UP)
        self._joystick_left_pin = digitalio.DigitalInOut(board.D27)
        self._joystick_left_pin.switch_to_input(pull=digitalio.Pull.UP)
        
        # 위, 오른쪽, 아래, 왼쪽 순서대로 핀 객체 저장
        self.joystick_pin_list = [self._joystick_up_pin, self._joystick_right_pin, self._joystick_down_pin, self._joystick_left_pin]
        
        # 5번 버튼과 6번 버튼 핀
        # 모두 입력 모드로 설정함
        # 눌려있을때 False, 안눌려 있을때 True 값을 가짐.
        self.five_button_pin = digitalio.DigitalInOut(board.D5)
        self.five_button_pin.switch_to_input(pull=digitalio.Pull.UP)
        self.six_button_pin = digitalio.DigitalInOut(board.D6)
        self.six_button_pin.switch_to_input(pull=digitalio.Pull.UP)
        
        # 현재 조이스틱 방향을 저장함. 방향이 없으면 None.
        self.current_direction = self.read_direction_from_joystick()

        # 현재 5번, 6번 버튼의 눌림 상태를 저장함
        self.current_five_button = self.is_pressed(self.five_button_pin)
        self.current_six_button = self.is_pressed(self.six_button_pin)
        
    # 눌렸을때와 안눌렸을때 bool 값이 헷갈려서 뒤집는 함수 선언. 신호는 반드시 이 함수로만 호출할 것.
    def is_pressed(self, pin:digitalio.DigitalInOut):
        """- 눌렸을때와 안눌렸을때 bool 값이 헷갈려서 뒤집는 함수 선언. 
        - 신호는 반드시 이 함수로만 호출할 것."""
        return not pin.value
        
    # 위, 오른쪽, 아래, 왼쪽을 순서대로 눌려있는지 확하여 눌린 방향을 반환. 없으면 None 반환
    def read_direction_from_joystick(self):
        """위, 오른쪽, 아래, 왼쪽을 순서대로 눌려있는지 확하여 눌린 방향을 반환. 없으면 None 반환"""
        for dir in Direction:
            if self.is_pressed(self.joystick_pin_list[dir]): return dir
        return None
    
    # 조이스틱의 방향이 바뀌었는지 확인하는 함수
    def check_direction_changed(self):
        # 현재 눌린 방향 검사
        dir = self.read_direction_from_joystick()
        # 이전 값과 다르다면 우선 값 저장
        if dir != self.current_direction:
            self.current_direction = dir
            # 이번에 바뀐 값이 None이 아니라면 다른 방향으로 바뀐 것이므로 True 반환
            if dir != None:
                return True
            # None으로 바뀐 것이면 그냥 조이스틱을 푼 것임
            else:
                return False
        else:
            self.current_direction = dir
            return False
    
    # 5번 버튼의 입력 값을 바로 반환함
    def read_five_button(self):
        """5번 버튼의 입력 값을 바로 반환함"""
        return self.is_pressed(self.five_button_pin)
    
    # 5번 버튼이 눌렸는지 확인함
    def check_five_button_pressed(self):
        this_time_five_button_signal = self.is_pressed(self.five_button_pin)
        if this_time_five_button_signal and this_time_five_button_signal != self.current_five_button:
            self.current_five_button = this_time_five_button_signal
            return True
        self.current_five_button = this_time_five_button_signal
        return False
    
    # 6번 버튼의 입력 값을 바로 반환함.
    def read_six_button(self):
        """6번 버튼의 입력 값을 바로 반환함."""
        return self.is_pressed(self.six_button_pin)

    # 6번 버튼이 눌렸는지 확인함
    def check_six_button_pressed(self):
        this_time_six_button_signal = self.is_pressed(self.six_button_pin)
        if this_time_six_button_signal and this_time_six_button_signal != self.current_six_button:
            self.current_six_button = this_time_six_button_signal
            return True
        self.current_six_button = this_time_six_button_signal
        return False

# -----------------------------------------------------

if __name__ == "__main__":
    import time
    
    tmp_input_observer = InputObserver()
    
    while True:
        if tmp_input_observer.check_direction_changed():
            print(tmp_input_observer.current_direction.name)
        if tmp_input_observer.check_five_button_pressed():
            print("5번 버튼 눌림")
        if tmp_input_observer.check_six_button_pressed():
            print("6번 버튼 눌림")
        time.sleep(0.02)