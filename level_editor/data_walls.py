# Цвета
WALL_WHITE = (255, 255, 255)
WALL_RED = (255, 0, 0)
WALL_GREEN = (0, 255, 0)
WALL_BLUE = (0, 0, 255)
WALL_BLACK = (0, 0, 0)
WIN_COLOR = (255, 215, 0)
LOSE_COLOR = (180, 0, 0)

walls_list = [
    [20, WALL_WHITE, 0, 860, 120, False, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 320, 810, 200, False, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 320, 810, 150, True, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 500, 810, 100, True, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 520, 880, 120, False, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 640, 640, 260, True, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 420, 540, 270, True, 'barricada', 'левая стена'],

    [20, WALL_WHITE, 0, 460, 120, False, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 320, 410, 200, False, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 320, 410, 150, True, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 500, 410, 100, True, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 520, 480, 120, False, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 640, 240, 260, True, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 420, 140, 270, True, 'barricada', 'левая стена'], 
]

special_walls_list = [
    # [толщина, цвет, x, y, длина, верт?, тип, имя, прозрачность, смертельность, движ.верт, движ.гор]
    [20, WALL_BLUE, 300, 200, 100, True, 'moving_vertical', 'движущаяся вертикальная стена', False, False, True, False],    
    [20, WALL_RED, 500, 300, 200, False, 'moving_horizontal', 'движущаяся горизонтальная стена', False, False, False, True],    
    [20, WALL_GREEN, 700, 400, 150, True, 'transparent', 'прозрачная стена', True, False, False, False],    
    [20, WALL_RED, 0, 500, 100, False, 'deadly', 'смертельная стена', False, True, False, False]
]
