import ctypes

user32 = ctypes.windll.user32
SCREEN_WIDTH, SCREEN_HEIGHT = user32.GetSystemMetrics(
    0), user32.GetSystemMetrics(1)

SCREEN_CENTER_X = SCREEN_WIDTH // 2
SCREEN_CENTER_Y = SCREEN_HEIGHT // 2