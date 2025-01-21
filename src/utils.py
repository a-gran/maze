import pygame

def create_walls(walls_dict_list, Wall):
    """
    Создает список объектов стен из списка словарей
    
    Args:
        walls_dict_list (list): Список словарей с параметрами стен
        Wall (class): Класс стены
    
    Returns:
        list: Список объектов стен
    """
    wall_objects = []
    for wall_dict in walls_dict_list.copy():  # Используем copy() чтобы не изменять оригинальный словарь
        # Создаем стену, передавая параметры напрямую из словаря
        wall = Wall(
            thickness=wall_dict["thickness"],
            color=wall_dict["color"],
            wall_x=wall_dict["wall_x"],
            wall_y=wall_dict["wall_y"],
            length=wall_dict["length"],
            is_vertical=wall_dict["is_vertical"],
            type_wall=wall_dict["type_wall"],
            name=wall_dict["name"]
        )
        wall_objects.append(wall)
    return wall_objects

def create_special_walls(special_walls_dict_list, SpecialWall):
    """
    Создает список объектов специальных стен из списка словарей
    
    Args:
        special_walls_dict_list (list): Список словарей с параметрами специальных стен
        SpecialWall (class): Класс специальной стены
    
    Returns:
        list: Список объектов специальных стен
    """
    special_wall_objects = []
    for wall_dict in special_walls_dict_list.copy():  # Используем copy() чтобы не изменять оригинальный словарь
        # Создаем специальную стену, передавая параметры напрямую из словаря
        wall = SpecialWall(
            thickness=wall_dict["thickness"],
            color=wall_dict["color"],
            wall_x=wall_dict["wall_x"],
            wall_y=wall_dict["wall_y"],
            length=wall_dict["length"],
            is_vertical=wall_dict["is_vertical"],
            wall_type=wall_dict["wall_type"],  # Используем wall_type для SpecialWall
            name=wall_dict["name"],
            is_transparent=wall_dict["is_transparent"],
            is_deadly=wall_dict["is_deadly"],
            is_moving_vertical=wall_dict["is_moving_vertical"],
            is_moving_horizontal=wall_dict["is_moving_horizontal"]
        )
        special_wall_objects.append(wall)
    return special_wall_objects

def handle_collision_with_walls(sprite, walls, special_walls=None):
    """
    Обработка столкновений со стенами с учетом движущихся стен
    """
    collision_occurred = False
    
    # Сначала проверяем обычные стены
    for wall in walls:
        if pygame.sprite.collide_rect(sprite, wall):
            # Определяем направление столкновения
            if sprite.rect.centerx < wall.rect.left:  # Столкновение справа
                sprite.rect.right = wall.rect.left
            elif sprite.rect.centerx > wall.rect.right:  # Столкновение слева
                sprite.rect.left = wall.rect.right
            elif sprite.rect.centery < wall.rect.top:  # Столкновение снизу
                sprite.rect.bottom = wall.rect.top
            else:  # Столкновение сверху
                sprite.rect.top = wall.rect.bottom
            collision_occurred = True

    # Затем проверяем специальные стены
    if special_walls:
        for wall in special_walls:
            if pygame.sprite.collide_rect(sprite, wall):
                # Пропускаем прозрачные стены в прозрачном состоянии
                if wall.is_transparent and wall.is_currently_transparent:
                    continue

                # Для движущихся стен
                if wall.is_moving_horizontal or wall.is_moving_vertical:
                    if wall.is_moving_horizontal:
                        moving_right = wall.move_direction > 0
                        if moving_right and sprite.rect.left < wall.rect.right:
                            # Если стена движется вправо и игрок слева от нее
                            sprite.rect.left = wall.rect.right
                        elif not moving_right and sprite.rect.right > wall.rect.left:
                            # Если стена движется влево и игрок справа от нее
                            sprite.rect.right = wall.rect.left
                            
                    if wall.is_moving_vertical:
                        moving_down = wall.move_direction > 0
                        if moving_down and sprite.rect.top < wall.rect.bottom:
                            # Если стена движется вниз и игрок над ней
                            sprite.rect.top = wall.rect.bottom
                        elif not moving_down and sprite.rect.bottom > wall.rect.top:
                            # Если стена движется вверх и игрок под ней
                            sprite.rect.bottom = wall.rect.top
                            
                    collision_occurred = True
                else:
                    # Для неподвижных специальных стен - обычная обработка
                    if sprite.rect.centerx < wall.rect.left:
                        sprite.rect.right = wall.rect.left
                    elif sprite.rect.centerx > wall.rect.right:
                        sprite.rect.left = wall.rect.right
                    elif sprite.rect.centery < wall.rect.top:
                        sprite.rect.bottom = wall.rect.top
                    else:
                        sprite.rect.top = wall.rect.bottom
                    collision_occurred = True
    
    return collision_occurred

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