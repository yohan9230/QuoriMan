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
        
    # 눌렸을때와 안눌렸을때 bool 값이 헷갈려서 뒤집는 함수 선언. 신호는 반드시 이 함수로만 호출할 것.
    def is_pressed(self, pin:digitalio.DigitalInOut):
        """- 눌렸을때와 안눌렸을때 bool 값이 헷갈려서 뒤집는 함수 선언. 
        - 신호는 반드시 이 함수로만 호출할 것."""
        return not pin.value
        
    # 위, 오른쪽, 아래, 왼쪽을 순서대로 눌려있는지 확하여 눌린 방향을 반환. 없으면 None 반환
    def read_dirction_from_joystick(self):
        """위, 오른쪽, 아래, 왼쪽을 순서대로 눌려있는지 확하여 눌린 방향을 반환. 없으면 None 반환"""
        for dir in Direction:
            if self.is_pressed(self.joystick_pin_list[dir]): return dir
        return None
    
    # 5번 버튼의 입력 값을 바로 반환함
    def read_five_button(self):
        """5번 버튼의 입력 값을 바로 반환함"""
        return self.is_pressed(self.five_button_pin)
    
    # 6번 버튼의 입력 값을 바로 반환함.
    def read_six_button(self):
        """6번 버튼의 입력 값을 바로 반환함."""
        return self.is_pressed(self.six_button_pin)

    def is_updated(self, before_signal:bool, pin:digitalio.DigitalInOut):
        if before_signal: return False
        if self.is_pressed(pin): return True
        return False
        
        
    
# -----------------------------------------------------

if __name__ == "__main__":
    import time
    
    tmp_input_observer = InputObserver()
    
    # 위, 오른쪽, 아래, 왼쪽 순서대로 기존 신호값 저장.
    current_dir_signal = []
    
    for d in Direction:
        current_dir_signal.append(tmp_input_observer.is_pressed(tmp_input_observer.joystick_pin_list[d]))
        
    current_five_button = tmp_input_observer.is_pressed(tmp_input_observer.five_button_pin)
    current_six_button = tmp_input_observer.is_pressed(tmp_input_observer.six_button_pin)
    
    while True:
        # 4방향 조이스틱 입력 검사
        dir = tmp_input_observer.read_dirction_from_joystick()
        ## 눌린 값이 없다면 4방향 모두 눌리지 않음 -> 전부 False로 설정
        if dir == None:
            current_dir_signal = [False, False, False, False]
        else:
            if tmp_input_observer.is_updated(current_dir_signal[dir], tmp_input_observer.joystick_pin_list[dir]):
                for d in Direction:
                    current_dir_signal[d] = False
                current_dir_signal[dir] = True
                print(dir.name)
        # 5번 버튼 검사
        if tmp_input_observer.is_updated(current_five_button, tmp_input_observer.five_button_pin):
            current_five_button = True
            print("5번 버튼 눌림")
        else:
            current_five_button = tmp_input_observer.is_pressed(tmp_input_observer.five_button_pin)
        # 6번 버튼 검사
        if tmp_input_observer.is_updated(current_six_button, tmp_input_observer.six_button_pin):
            current_six_button = True
            print("6번 버튼 눌림")
        else:
            current_six_button = tmp_input_observer.is_pressed(tmp_input_observer.six_button_pin)
        time.sleep(0.02)