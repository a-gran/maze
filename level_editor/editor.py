import pygame
import json
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from src.walls import Wall, SpecialWall  # Обновляем путь импорта
from paths import *  # Импортируем все необходимые пути

class MazeEditor:
    def __init__(self):
        # Инициализация PyGame
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('Maze Editor')
        self.clock = pygame.time.Clock()

        # Создание окна настроек с помощью Tkinter
        self.root = tk.Tk()
        self.root.title("Wall Settings")
        self.root.geometry("300x600")
        
        # Параметры стены
        self.current_wall = {
            'thickness': 20,
            'color': WALL_WHITE,
            'is_vertical': False,
            'length': 100,
            'type': 'barricada',
            'is_transparent': False,
            'is_deadly': False,
            'is_moving_vertical': False,
            'is_moving_horizontal': False
        }
        
        self.walls = []
        self.selected_wall = None
        self.dragging = False
        
        self._create_settings_ui()
        
    def _create_settings_ui(self):
        # Толщина стены
        tk.Label(self.root, text="Thickness:").pack()
        thickness_var = tk.StringVar(value="20")
        thickness_entry = tk.Entry(self.root, textvariable=thickness_var)
        thickness_entry.pack()
        thickness_var.trace('w', lambda *args: self._update_param('thickness', int(thickness_var.get() if thickness_var.get().isdigit() else 20)))

        # Длина стены
        tk.Label(self.root, text="Length:").pack()
        length_var = tk.StringVar(value="100")
        length_entry = tk.Entry(self.root, textvariable=length_var)
        length_entry.pack()
        length_var.trace('w', lambda *args: self._update_param('length', int(length_var.get() if length_var.get().isdigit() else 100)))

        # Ориентация стены
        tk.Label(self.root, text="Orientation:").pack()
        orientation_var = tk.BooleanVar()
        tk.Radiobutton(self.root, text="Horizontal", variable=orientation_var, value=False, 
                      command=lambda: self._update_param('is_vertical', False)).pack()
        tk.Radiobutton(self.root, text="Vertical", variable=orientation_var, value=True,
                      command=lambda: self._update_param('is_vertical', True)).pack()

        # Тип стены
        tk.Label(self.root, text="Wall Type:").pack()
        wall_types = ['barricada', 'moving_vertical', 'moving_horizontal', 'transparent', 'deadly']
        type_var = tk.StringVar(value='barricada')
        type_combo = ttk.Combobox(self.root, textvariable=type_var, values=wall_types)
        type_combo.pack()
        type_combo.bind('<<ComboboxSelected>>', lambda *args: self._update_param('type', type_var.get()))

        # Цвет стены
        color_button = tk.Button(self.root, text="Choose Color", command=self._choose_color)
        color_button.pack()

        # Специальные свойства
        tk.Label(self.root, text="Special Properties:").pack()
        
        transparent_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Transparent", variable=transparent_var,
                      command=lambda: self._update_param('is_transparent', transparent_var.get())).pack()
        
        deadly_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Deadly", variable=deadly_var,
                      command=lambda: self._update_param('is_deadly', deadly_var.get())).pack()
        
        moving_v_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Moving Vertical", variable=moving_v_var,
                      command=lambda: self._update_param('is_moving_vertical', moving_v_var.get())).pack()
        
        moving_h_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Moving Horizontal", variable=moving_h_var,
                      command=lambda: self._update_param('is_moving_horizontal', moving_h_var.get())).pack()

        # Кнопки управления
        tk.Button(self.root, text="Delete Selected", command=self._delete_selected).pack()
        tk.Button(self.root, text="Save Maze", command=self._save_maze).pack()
        tk.Button(self.root, text="Load Maze", command=self._load_maze).pack()
        tk.Button(self.root, text="Export to Python", command=self._export_to_python).pack()

    def _update_param(self, param, value):
        self.current_wall[param] = value

    def _choose_color(self):
        color = colorchooser.askcolor(title="Choose wall color")[0]
        if color:
            self.current_wall['color'] = color

    def _delete_selected(self):
        if self.selected_wall is not None:
            self.walls.remove(self.selected_wall)
            self.selected_wall = None

    def _create_wall(self, pos):
        x, y = pos
        wall_params = self.current_wall.copy()
        
        if wall_params['type'] in ['moving_vertical', 'moving_horizontal', 'transparent', 'deadly']:
            wall = SpecialWall(
                thickness=wall_params['thickness'],
                color=wall_params['color'],
                wall_x=x,
                wall_y=y,
                length=wall_params['length'],
                is_vertical=wall_params['is_vertical'],
                wall_type=wall_params['type'],
                name=wall_params['type'],
                is_transparent=wall_params['is_transparent'],
                is_deadly=wall_params['is_deadly'],
                is_moving_vertical=wall_params['is_moving_vertical'],
                is_moving_horizontal=wall_params['is_moving_horizontal']
            )
        else:
            wall = Wall(
                thickness=wall_params['thickness'],
                color=wall_params['color'],
                wall_x=x,
                wall_y=y,
                length=wall_params['length'],
                is_vertical=wall_params['is_vertical'],
                type_wall=wall_params['type'],
                name=wall_params['type']
            )
        
        self.walls.append(wall)
        return wall

    def _save_maze(self):
        maze_data = []
        for wall in self.walls:
            wall_data = {
                'thickness': wall.thickness,
                'color': wall.color,
                'wall_x': wall.rect.x,
                'wall_y': wall.rect.y,
                'length': wall.length,
                'is_vertical': wall.is_vertical,
                'type': wall.type_wall,
                'name': wall.name
            }
            
            if isinstance(wall, SpecialWall):
                wall_data.update({
                    'is_transparent': wall.is_transparent,
                    'is_deadly': wall.is_deadly,
                    'is_moving_vertical': wall.is_moving_vertical,
                    'is_moving_horizontal': wall.is_moving_horizontal
                })
            
            maze_data.append(wall_data)
            
        with open('maze.json', 'w') as f:
            json.dump(maze_data, f)
        
        messagebox.showinfo("Success", "Maze saved successfully!")

    def _load_maze(self):
        try:
            with open('maze.json', 'r') as f:
                maze_data = json.load(f)
            
            self.walls = []
            for wall_data in maze_data:
                if wall_data['type'] in ['moving_vertical', 'moving_horizontal', 'transparent', 'deadly']:
                    wall = SpecialWall(
                        thickness=wall_data['thickness'],
                        color=wall_data['color'],
                        wall_x=wall_data['wall_x'],
                        wall_y=wall_data['wall_y'],
                        length=wall_data['length'],
                        is_vertical=wall_data['is_vertical'],
                        wall_type=wall_data['type'],
                        name=wall_data['name'],
                        is_transparent=wall_data.get('is_transparent', False),
                        is_deadly=wall_data.get('is_deadly', False),
                        is_moving_vertical=wall_data.get('is_moving_vertical', False),
                        is_moving_horizontal=wall_data.get('is_moving_horizontal', False)
                    )
                else:
                    wall = Wall(
                        thickness=wall_data['thickness'],
                        color=wall_data['color'],
                        wall_x=wall_data['wall_x'],
                        wall_y=wall_data['wall_y'],
                        length=wall_data['length'],
                        is_vertical=wall_data['is_vertical'],
                        type_wall=wall_data['type'],
                        name=wall_data['name']
                    )
                self.walls.append(wall)
                
            messagebox.showinfo("Success", "Maze loaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved maze found!")

    def _export_to_python(self):
        walls_list = []
        special_walls_list = []
        
        for wall in self.walls:
            if isinstance(wall, SpecialWall):
                special_walls_list.append([
                    wall.thickness,
                    wall.color,
                    wall.rect.x,
                    wall.rect.y,
                    wall.length,
                    wall.is_vertical,
                    wall.type_wall,
                    wall.name,
                    wall.is_transparent,
                    wall.is_deadly,
                    wall.is_moving_vertical,
                    wall.is_moving_horizontal
                ])
            else:
                walls_list.append([
                    wall.thickness,
                    wall.color,
                    wall.rect.x,
                    wall.rect.y,
                    wall.length,
                    wall.is_vertical,
                    wall.type_wall,
                    wall.name
                ])
        
        with open('maze_data.py', 'w') as f:
            f.write('walls_list = [\n')
            for wall in walls_list:
                f.write(f'    {wall},\n')
            f.write(']\n\n')
            
            f.write('special_walls_list = [\n')
            for wall in special_walls_list:
                f.write(f'    {wall},\n')
            f.write(']\n')
            
        messagebox.showinfo("Success", "Maze exported to maze_data.py!")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        # Проверяем, не кликнули ли мы на существующую стену
                        mouse_pos = pygame.mouse.get_pos()
                        clicked = False
                        for wall in self.walls:
                            if wall.rect.collidepoint(mouse_pos):
                                self.selected_wall = wall
                                self.dragging = True
                                clicked = True
                                break
                        
                        if not clicked:
                            # Создаем новую стену
                            self.selected_wall = self._create_wall(mouse_pos)
                            self.dragging = True
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left click
                        self.dragging = False
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging and self.selected_wall:
                        self.selected_wall.rect.x, self.selected_wall.rect.y = event.pos
            
            # Отрисовка
            self.window.fill((0, 0, 0))
            
            # Отрисовка всех стен
            for wall in self.walls:
                if isinstance(wall, SpecialWall):
                    wall.update()
                wall.draw_wall(self.window)
            
            # Подсветка выбранной стены
            if self.selected_wall:
                pygame.draw.rect(self.window, (255, 255, 0), self.selected_wall.rect, 2)
            
            pygame.display.flip()
            self.clock.tick(60)
            
            # Обновление Tkinter
            self.root.update()
        
        pygame.quit()
        self.root.destroy()

if __name__ == '__main__':
    editor = MazeEditor()
    editor.run()