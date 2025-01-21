from src.walls_colors import *

# Список обычных стен
walls_dict_list = [
    {
        "thickness": 20,
        "color": WALL_WHITE,
        "wall_x": 0,
        "wall_y": 860,
        "length": 120,
        "is_vertical": False,
        "type_wall": "barricada",
        "name": "левая стена"
    },
    {
        "thickness": 20,
        "color": WALL_WHITE,
        "wall_x": 320,
        "wall_y": 810,
        "length": 200,
        "is_vertical": False,
        "type_wall": "barricada",
        "name": "левая стена"
    }
]

# Список специальных стен
special_walls_dict_list = [
    {
        "thickness": 20,
        "color": WALL_BLUE,
        "wall_x": 300,
        "wall_y": 200,
        "length": 100,
        "is_vertical": True,
        "wall_type": "moving_vertical",  # Изменено с type_wall на wall_type для SpecialWall
        "name": "движущаяся вертикальная стена",
        "is_transparent": False,
        "is_deadly": False,
        "is_moving_vertical": True,
        "is_moving_horizontal": False
    },
    {
        "thickness": 20,
        "color": WALL_RED,
        "wall_x": 500,
        "wall_y": 300,
        "length": 200,
        "is_vertical": False,
        "wall_type": "moving_horizontal",
        "name": "движущаяся горизонтальная стена",
        "is_transparent": False,
        "is_deadly": False,
        "is_moving_vertical": False,
        "is_moving_horizontal": True
    }
]
