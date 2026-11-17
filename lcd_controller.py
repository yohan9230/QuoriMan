# LCD 컨트롤 전용 소스파일. 모든 LCD 관련 조작은 이 파일을 통해서만 한다.

# 라즈베리 파이의 핀 번호를 담고 있는 라이브러리.
import board
# 라즈베리 파이의 핀으로부터 신호를 입력/출력 할 수 있게 해주는 객체를 담은 라이브러리. 해당 객체명은 DigitalInOut 임.
import digitalio

class LCDController:
    def __init__(self):
        # CS 핀 입출력 객체
        chip_select_pin = digitalio.DigitalInOut(board.CE0)
        # DC 핀 입출력 객체
        data_command_pin = digitalio.DigitalInOut(board.D25)
        # LCD 패널을 움직이는 디스플레이 컨트롤러 칩을 초기화할때 사용하는 핀(ST7789)
        reset_display_controller_chip = digitalio.DigitalInOut(board.D24)