from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI
import time

class OnScreenKeyboard:
    def __init__(self, display, touch):
        self.display = display
        self.touch = touch
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7'],
            ['8', '9', '0', 'A', 'B', 'C', 'D'],
            ['E', 'F', 'G', 'H', 'I', 'J', 'K'],
            ['L', 'M', 'N', 'O', 'P', 'Q', 'R'],
            ['S', 'T', 'U', 'V', 'W', 'X', 'Y'],
            ['Z', '_', '.', 'DEL', 'SPACE', 'ENTER']
        ]
        self.normal_key_width = 32
        self.special_key_width = 43
        self.key_height = 30
        self.margin = 2
        self.start_y = 50

    def draw(self):
        self.display.clear()
        y = self.start_y
        for row in self.keys:
            x = 0
            for key in row:
                key_width = self.special_key_width if key in ['DEL', 'SPACE', 'ENTER'] else self.normal_key_width
                key_margin = 1 if key in ['SPACE', 'ENTER'] else 5 if key in ['DEL'] else 10
                self.display.draw_rectangle(x, y, key_width, self.key_height, color565(0, 255, 0))
                self.display.draw_text8x8(x + key_margin, y + 10, key, color565(255, 255, 255))
                x += key_width + self.margin
            y += self.key_height + self.margin

    def get_key(self, x, y):
        if y < self.start_y:
            return None
        
        row = (y - self.start_y) // (self.key_height + self.margin)
        if row >= len(self.keys):
            return None

        x_in_row = x
        for key in self.keys[row]:
            key_width = self.special_key_width if key in ['DEL', 'SPACE', 'ENTER'] else self.normal_key_width
            if x_in_row < key_width:
                return key
            x_in_row -= (key_width + self.margin)
            if x_in_row < 0:
                break
        
        return None

class CodeBreaker:
    BLACK = color565(0, 0, 0)
    WHITE = color565(255, 255, 255)
    GREEN = color565(0, 255, 0)
    RED = color565(255, 0, 0)
    BLUE = color565(0, 0, 255)

    def __init__(self, display, spi2):
        self.display = display
        self.touch = Touch(spi2, cs=Pin(33), int_pin=Pin(36), int_handler=self.touchscreen_press)
        self.current_level = 0
        self.secret_code = ""
        self.last_touch = (0, 0)
        self.keyboard = OnScreenKeyboard(display, self.touch)
        self.touch_detected = False

    def touchscreen_press(self, x, y):
        adjusted_x = x
        adjusted_y = int(self.display.height - y)
        self.last_touch = (adjusted_x, adjusted_y)
        self.touch_detected = True

    def start_game(self):
        self.display.clear()
        self.display.draw_text8x8(10, 10, "CodeBreaker", self.WHITE, background=self.BLUE)
        self.display.draw_text8x8(10, 30, "Touch to start", self.GREEN)
        
        while True:
            if self.touch_detected:
                self.touch_detected = False
                break
            time.sleep(0.1)
        
        self.run_game()

    def run_game(self):
        levels = [
            self.binary_decoder,
            self.regex_matcher,
            self.logic_gate_puzzle,
            self.algorithm_optimization,
            self.cryptography_challenge
        ]
        for level in range(len(levels)):
            self.current_level = level
            level_completed = levels[level]()
            if level_completed:
                self.show_level_complete()
            else:
                self.show_level_failed()
            if self.current_level >= len(levels) - 1:
                break
        self.show_game_complete()

    def binary_decoder(self):
        binary = "01001000 01100101 01101100 01101100 01101111"
        answer = "Hello"
        
        self.display.clear()
        self.display.draw_text8x8(10, 10, "Level 1: Binary Decoder", self.WHITE)
        self.display.draw_text8x8(10, 30, "Decode: " + binary, self.GREEN)
        
        user_input = self.get_user_input("Your answer:")
        if user_input.lower() == answer.lower():
            self.secret_code += "A"
            return True
        return False

    def regex_matcher(self):
        pattern = "^[a-z0-9_-]{3,16}$"
        answer = "user_123"
        
        self.display.clear()
        self.display.draw_text8x8(10, 10, "Level 2: Regex Matcher", self.WHITE)
        self.display.draw_text8x8(10, 30, "Pattern: " + pattern, self.GREEN)
        self.display.draw_text8x8(10, 50, "Find a matching string", self.GREEN)
        
        user_input = self.get_user_input("Your answer:")
        if user_input == answer:
            self.secret_code += "B"
            return True
        return False

    def logic_gate_puzzle(self):
        puzzle = "A AND (B OR C)"
        answer = "101"
        
        self.display.clear()
        self.display.draw_text8x8(10, 10, "Level 3: Logic Gate", self.WHITE)
        self.display.draw_text8x8(10, 30, puzzle, self.GREEN)
        self.display.draw_text8x8(10, 50, "Input: 1 1 0", self.GREEN)
        self.display.draw_text8x8(10, 70, "Output: ?", self.GREEN)
        
        user_input = self.get_user_input("Your answer (0/1):")
        if user_input == answer:
            self.secret_code += "C"
            return True
        return False

    def algorithm_optimization(self):
        code = "def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)"
        answer = "dynamic programming"
        
        self.display.clear()
        self.display.draw_text8x8(10, 10, "Level 4: Optimization", self.WHITE)
        self.display.draw_text8x8(10, 30, "Optimize:", self.GREEN)
        self.display.draw_text8x8(10, 50, code, self.GREEN)
        
        user_input = self.get_user_input("Optimization technique:")
        if answer in user_input.lower():
            self.secret_code += "D"
            return True
        return False

    def cryptography_challenge(self):
        cipher = "Uif tfdsfu jt jo uif mbtu mfwfm"
        answer = "The secret is in the last level"
        
        self.display.clear()
        self.display.draw_text8x8(10, 10, "Level 5: Cryptography", self.WHITE)
        self.display.draw_text8x8(10, 30, "Decrypt:", self.GREEN)
        self.display.draw_text8x8(10, 50, cipher, self.GREEN)
        
        user_input = self.get_user_input("Decrypted message:")
        if user_input.lower() == answer.lower():
            self.secret_code += "E"
            return True
        return False

    def check_touch(self):
        touch_point = self.touch.get_touch()
        if touch_point is not None:
            self.last_touch = touch_point
            return True
        return False

    def start_game(self):
        self.display.clear()
        self.display.draw_text8x8(10, 10, "CodeBreaker", self.WHITE, background=self.BLUE)
        self.display.draw_text8x8(10, 30, "Touch to start", self.GREEN)
        
        while True:
            if self.touch_detected:
                self.touch_detected = False
                break
            time.sleep(0.1)
        
        self.run_game()

    def run_game(self):
        levels = [
            self.binary_decoder,
            self.regex_matcher,
            self.logic_gate_puzzle,
            self.algorithm_optimization,
            self.cryptography_challenge
        ]
        for level in range(len(levels)):
            self.current_level = level
            level_completed = levels[level]()
            if level_completed:
                self.show_level_complete()
            else:
                self.show_level_failed()
            if self.current_level >= len(levels) - 1:
                break
        self.show_game_complete()

    def get_user_input(self, prompt):
        self.display.clear()
        self.display.draw_text8x8(10, 10, prompt, self.WHITE)
        self.keyboard.draw()
        self.touch_detected = False
        user_input = ""
        while True:
            if self.touch_detected:
                self.touch_detected = False
                x, y = self.last_touch
                key = self.keyboard.get_key(x, y)
                print(f"Touch at ({x}, {y}), Key: {key}")  # Debugging-Ausgabe
                if key:
                    if key == 'ENTER':
                        return user_input
                    elif key == 'DEL':
                        if user_input:
                            user_input = user_input[:-1]
                    elif key == 'SPACE':
                        user_input += ' '
                    else:
                        user_input += key
                    
                    self.display.fill_rectangle(10, 30, self.display.width - 20, 20, self.BLACK)
                    if user_input:
                        self.display.draw_text8x8(10, 30, user_input, self.GREEN)
            
            time.sleep(0.1)

    def show_level_complete(self):
        self.display.clear()
        self.display.draw_text8x8(10, 10, "Level Complete!", self.GREEN)
        if self.secret_code:
            self.display.draw_text8x8(10, 30, f"Code part: {self.secret_code[-1]}", self.WHITE)
        else:
            self.display.draw_text8x8(10, 30, "No code part collected", self.WHITE)
        self.display.draw_text8x8(10, 50, "Touch to continue", self.GREEN)
        
        self.wait_for_touch()

    def show_level_failed(self):
        self.display.clear()
        self.display.draw_text8x8(10, 10, "Level Failed!", self.RED)
        self.display.draw_text8x8(10, 30, "Touch to continue", self.GREEN)
        
        self.wait_for_touch()

    def show_game_complete(self):
        self.display.clear()
        self.display.draw_text8x8(10, 10, "Game Over!", self.GREEN)
        self.display.draw_text8x8(10, 30, "You've completed CodeBreaker!", self.WHITE)
        if self.secret_code:
            self.display.draw_text8x8(10, 50, f"Secret Code: {self.secret_code}", self.BLUE)
        else:
            self.display.draw_text8x8(10, 50, "No secret code collected", self.RED)
        self.display.draw_text8x8(10, 70, "Touch to restart", self.GREEN)
        
        self.wait_for_touch()
        self.start_game()

    def wait_for_touch(self):
        self.touch_detected = False
        while not self.touch_detected:
            time.sleep(0.1)

def main():
    spi1 = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi1, dc=Pin(2), cs=Pin(15), rst=Pin(0))
    
    bl_pin = Pin(21, Pin.OUT)
    bl_pin.on()
    
    spi2 = SPI(2, baudrate=1000000, sck=Pin(25), mosi=Pin(32), miso=Pin(39))

    game = CodeBreaker(display, spi2)
    game.start_game()

if __name__ == "__main__":
    main()