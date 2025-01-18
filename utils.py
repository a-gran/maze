def create_walls(walls_list, Wall):  # Добавляем параметр Wall
    wall_objects = []
    for wall_params in walls_list:
        wall = Wall(
            thickness=wall_params[0],
            color=wall_params[1],
            wall_x=wall_params[2],
            wall_y=wall_params[3],
            length=wall_params[4],
            is_vertical=wall_params[5],
            type_wall=wall_params[6],
            name=wall_params[7]
        )
        wall_objects.append(wall)
    return wall_objects

def create_special_walls(special_walls_list, SpecialWall):  # Добавляем параметр SpecialWall
    special_wall_objects = []
    for wall_params in special_walls_list:
        wall = SpecialWall(
            thickness=wall_params[0],
            color=wall_params[1],
            wall_x=wall_params[2],
            wall_y=wall_params[3],
            length=wall_params[4],
            is_vertical=wall_params[5],
            wall_type=wall_params[6],
            name=wall_params[7],
            is_transparent=wall_params[8],
            is_deadly=wall_params[9],
            is_moving_vertical=wall_params[10],
            is_moving_horizontal=wall_params[11]
        )
        special_wall_objects.append(wall)
    return special_wall_objects

def draw_lives(window, lives, lives_font, wall_white):
    lives_text = lives_font.render(f'Lives: {lives}', True, wall_white)
    window.blit(lives_text, (10, 10))

def end_game(window, finish, end_text, font, win_color, lose_color, money_sound=None, kick_sound=None):
    finish = True
    if end_text == 'win':
        if money_sound:
            money_sound.play()
        win_text = font.render('YOU WIN!', True, win_color)
        window.blit(win_text, (500, 500))
    elif end_text == 'lose':
        if kick_sound:
            kick_sound.play()
        lose_text = font.render('YOU LOSE!', True, lose_color)
        window.blit(lose_text, (500, 500))
    return finish