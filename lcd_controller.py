# LCD 컨트롤 전용 소스파일. 모든 LCD 관련 조작은 이 파일을 통해서만 한다.

# 라즈베리 파이의 핀 번호를 담고 있는 라이브러리.
import board
# 라즈베리 파이의 핀으로부터 신호를 입력/출력 할 수 있게 해주는 객체를 담은 라이브러리. 해당 객체명은 DigitalInOut 라고 함.
import digitalio
# LCD 디스플레이 컨트롤러 칩
from adafruit_rgb_display import st7789

from PIL import Image, ImageDraw

# commander <- 이것만 사용하면 됨.
class LCD:
    """commander <- 이것만 사용하면 됨."""
    # 자동 완성 켜지게 먼저 선언
    CS_chip_select_pin:digitalio.DigitalInOut
    DC_data_command_pin:digitalio.DigitalInOut
    RST_reset_display_controller_chip_pin:digitalio.DigitalInOut
    backlight_pin:digitalio.DigitalInOut
    
    # 너비, 높이 등 st7789에 넣을 상수들
    WIDTH = HEIGHT = 240
    ROTATION = 180
    X_OFFSET = 0
    Y_OFFSET = 80
    BAUDRATE=24000000
    
    
    def __init__(self):
        # CS 핀 입출력 객체
        self.CS_chip_select_pin = digitalio.DigitalInOut(board.CE0)
        # DC 핀 입출력 객체
        self.DC_data_command_pin = digitalio.DigitalInOut(board.D25)
        # LCD 패널을 움직이는 디스플레이 컨트롤러 칩(ST7789)을 초기화할때 사용하는 핀
        self.RST_reset_display_controller_chip_pin = digitalio.DigitalInOut(board.D24)
        
        # LCD 패널 백라이트 조작 핀
        self.backlight_pin = digitalio.DigitalInOut(board.D26)
        
        # SPI 버스 객체 생성
        self.spi = board.SPI()
        
        # -----------------------------------------------------
        
        # LCD 컨트롤러 칩 객체
        self.commander = st7789.ST7789(
            self.spi, 
            cs = self.CS_chip_select_pin, 
            dc = self.DC_data_command_pin, 
            rst = self.RST_reset_display_controller_chip_pin, 
            width = self.WIDTH, 
            height = self.HEIGHT,
            rotation = self.ROTATION,
            x_offset = self.X_OFFSET,
            y_offset = self.Y_OFFSET,
            baudrate = self.BAUDRATE)

        # 백라이트 핀을 출력 모드로 설정
        self.backlight_pin.switch_to_output()
        # 값을 True 로 바꿔서 백라이트를 켬
        self.backlight_pin.value = True
        
    # image 사진을 그대로 LCD에 출력하는 함수
    def show_the_image(self, image):
        """- image 사진을 그대로 LCD에 출력하는 함수. 
        - 반환값 없음"""
        self.commander.image(image)


# -----------------------------------------------------

if __name__ == "__main__":
    tmp_lcd = LCD()
    tmp_commander = tmp_lcd.commander
    
    # 임시로 배경으로 쓸 이미지 생성
    tmp_background = Image.new("RGB",(tmp_lcd.WIDTH, tmp_lcd.HEIGHT))
    
    # 배경을 기반으로 그릴 수 있는 ImageDraw 객체 생성
    tmp_imagedraw = ImageDraw.Draw(tmp_background)
    
    # 배경 위에 그림을 그림. 사각형. 빨간색
    tmp_imagedraw.rectangle((0, 0, 39, 39), fill = (255, 0, 0))
    
    # 배경에 쓸 이미지를 LCD로 내보냄. ImageDraw로 그린것도 같이 나옴.
    tmp_lcd.show_the_image(tmp_background)