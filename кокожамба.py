# Разработай свою игру в этом файле!
import pygame
from pygame import *
import math
import random

pygame.init()

widow = display.set_mode((700, 500))
display.set_caption('Лабиринт')
fon = transform.scale(image.load('фон.png'), (700, 500))

class Gamesprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        widow.blit(self.image, (self.rect.x, self.rect.y))

class Player(Gamesprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        Gamesprite.__init__(self, picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.start_x = x
        self.start_y = y
        self.hp = 3
        self.shoot_cooldown = 0
    
    def update(self):
        old_x = self.rect.x
        old_y = self.rect.y
        
        self.rect.x += self.x_speed
        # Создаем уменьшенный хитбокс для проверки столкновений
        temp_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10)
        for wall in barriers:
            wall_temp_rect = pygame.Rect(wall.rect.x + 3, wall.rect.y + 3, wall.rect.width - 6, wall.rect.height - 6)
            if temp_rect.colliderect(wall_temp_rect):
                self.rect.x = old_x
                break
            
        self.rect.y += self.y_speed
        # Создаем уменьшенный хитбокс для проверки столкновений
        temp_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10)
        for wall in barriers:
            wall_temp_rect = pygame.Rect(wall.rect.x + 3, wall.rect.y + 3, wall.rect.width - 6, wall.rect.height - 6)
            if temp_rect.colliderect(wall_temp_rect):
                self.rect.y = old_y
                break
        
        # Обновление кулдауна стрельбы
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def reset_position(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.hp = 3

class Enemy(Gamesprite):
    def __init__(self, picture, w, h, x, y):
        Gamesprite.__init__(self, 'бэби.png', w, h, x, y)
        self.speed = 1
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.move_timer = 0
        self.shoot_timer = random.randint(30, 90)
    
    def update(self, player):
        # Простое движение врага
        self.move_timer += 1
        if self.move_timer > random.randint(30, 60):
            self.direction = random.choice(['up', 'down', 'left', 'right'])
            self.move_timer = 0
        
        old_x = self.rect.x
        old_y = self.rect.y
        
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        
        # Проверка столкновения со стенами с уменьшенными хитбоксами
        temp_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10)
        for wall in barriers:
            wall_temp_rect = pygame.Rect(wall.rect.x + 3, wall.rect.y + 3, wall.rect.width - 6, wall.rect.height - 6)
            if temp_rect.colliderect(wall_temp_rect):
                self.rect.x = old_x
                self.rect.y = old_y
                self.direction = random.choice(['up', 'down', 'left', 'right'])
                break
    
    def shoot(self):
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(60, 120)
            return True
        return False

class Drone(Gamesprite):
    def __init__(self, picture, w, h, x, y):
        Gamesprite.__init__(self, 'дрон.png', w, h, x, y)
        self.speed = 2
        self.dx = 0
        self.dy = 0
        self.move_pattern = 0
    
    def update(self, player):
        # Дрон летает по паттерну или преследует игрока
        self.move_pattern += 1
        
        if self.move_pattern < 60:
            # Преследование игрока
            if self.rect.x < player.rect.x:
                self.dx = self.speed
            elif self.rect.x > player.rect.x:
                self.dx = -self.speed
            else:
                self.dx = 0
                
            if self.rect.y < player.rect.y:
                self.dy = self.speed
            elif self.rect.y > player.rect.y:
                self.dy = -self.speed
            else:
                self.dy = 0
        else:
            # Движение по кругу
            self.dx = self.speed * math.cos(self.move_pattern * 0.05)
            self.dy = self.speed * math.sin(self.move_pattern * 0.05)
            if self.move_pattern > 120:
                self.move_pattern = 0
        
        old_x = self.rect.x
        old_y = self.rect.y
        
        self.rect.x += self.dx
        # Проверка столкновения со стенами с уменьшенными хитбоксами
        temp_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6)
        for wall in barriers:
            wall_temp_rect = pygame.Rect(wall.rect.x + 3, wall.rect.y + 3, wall.rect.width - 6, wall.rect.height - 6)
            if temp_rect.colliderect(wall_temp_rect):
                self.rect.x = old_x
                self.dx = -self.dx
                break
            
        self.rect.y += self.dy
        # Проверка столкновения со стенами с уменьшенными хитбоксами
        temp_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6)
        for wall in barriers:
            wall_temp_rect = pygame.Rect(wall.rect.x + 3, wall.rect.y + 3, wall.rect.width - 6, wall.rect.height - 6)
            if temp_rect.colliderect(wall_temp_rect):
                self.rect.y = old_y
                self.dy = -self.dy
                break
    
    def shoot(self):
        return random.randint(1, 50) == 1

class Bullet(Gamesprite):
    def __init__(self, x, y, direction, speed=5, is_enemy=False):
        if is_enemy:
            super().__init__('враг_пуля.png', 8, 8, x, y)
        else:
            super().__init__('пуля.png', 8, 8, x, y)
        self.direction = direction
        self.speed = speed
        self.is_enemy = is_enemy
    
    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        
        # Удаление пули, если она вышла за экран
        if self.rect.x < 0 or self.rect.x > 700 or self.rect.y < 0 or self.rect.y > 500:
            return True
        return False

barriers = sprite.Group()

# Границы - создаем с уменьшенными хитбоксами через отдельные rect'ы
wall_top = Gamesprite('wall.png', 700, 10, 0, -5)
wall_bottom = Gamesprite('wall.png', 700, 10, 0, 495)
wall_left = Gamesprite('wall.png', 10, 500, -5, 0)
wall_right = Gamesprite('wall.png', 10, 500, 695, 0)

barriers.add(wall_top, wall_bottom, wall_left, wall_right)

# Нормальный лабиринт с проходами
# Вертикальные стены
wall_1 = Gamesprite('wall.png', 10, 200, 150, 50)
wall_2 = Gamesprite('wall.png', 10, 150, 150, 300)
wall_3 = Gamesprite('wall.png', 10, 250, 300, 100)
wall_4 = Gamesprite('wall.png', 10, 200, 300, 350)
wall_5 = Gamesprite('wall.png', 10, 180, 450, 50)
wall_6 = Gamesprite('wall.png', 10, 180, 450, 280)
wall_7 = Gamesprite('wall.png', 10, 150, 550, 150)
wall_8 = Gamesprite('wall.png', 10, 150, 550, 320)

# Горизонтальные стены
wall_9 = Gamesprite('wall.png', 200, 10, 50, 150)
wall_10 = Gamesprite('wall.png', 180, 10, 250, 250)
wall_11 = Gamesprite('wall.png', 150, 10, 400, 200)
wall_12 = Gamesprite('wall.png', 200, 10, 200, 400)
wall_13 = Gamesprite('wall.png', 180, 10, 450, 380)
wall_14 = Gamesprite('wall.png', 150, 10, 100, 300)

# Добавляем все стены
walls = [wall_1, wall_2, wall_3, wall_4, wall_5, wall_6, wall_7, wall_8, 
         wall_9, wall_10, wall_11, wall_12, wall_13, wall_14]

for wall in walls:
    barriers.add(wall)

final = Gamesprite('сокровище.png', 50, 50, 600, 420)
player = Player('mem.png', 30, 30, 30, 30, 0, 0)

# Создание врагов
enemies = sprite.Group()
drone1 = Drone('дрон.png', 25, 25, 200, 200)
drone2 = Drone('дрон.png', 25, 25, 400, 100)
enemy1 = Enemy('бэби.png', 30, 30, 350, 250)
enemy2 = Enemy('бэби.png', 30, 30, 500, 300)

enemies.add(drone1, drone2, enemy1, enemy2)

# Группа для пуль
player_bullets = sprite.Group()
enemy_bullets = sprite.Group()

run = True
finish = False
win = transform.scale(image.load('всё.png'), (700, 500))

# Шрифт для отображения HP и текста
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

while run:
    time.delay(50)
    
    for e in event.get():
        if e.type == QUIT:
            run = False
            
        elif e.type == KEYDOWN:
            if e.key == K_w:
                player.y_speed = -3
            elif e.key == K_s:
                player.y_speed = 3
            elif e.key == K_a:
                player.x_speed = -3
            elif e.key == K_d:
                player.x_speed = 3
            elif e.key == K_r:
                player.reset_position()
                finish = False
                player_bullets.empty()
                enemy_bullets.empty()
                # Восстанавливаем врагов, если они были удалены
                if len(enemies) < 4:
                    enemies.empty()
                    drone1 = Drone('дрон.png', 25, 25, 200, 200)
                    drone2 = Drone('дрон.png', 25, 25, 400, 100)
                    enemy1 = Enemy('бэби.png', 30, 30, 350, 250)
                    enemy2 = Enemy('бэби.png', 30, 30, 500, 300)
                    enemies.add(drone1, drone2, enemy1, enemy2)
            # Стрельба из игрока
            elif e.key == K_UP and player.shoot_cooldown == 0:
                bullet = Bullet(player.rect.centerx - 4, player.rect.top, 'up')
                player_bullets.add(bullet)
                player.shoot_cooldown = 20
            elif e.key == K_DOWN and player.shoot_cooldown == 0:
                bullet = Bullet(player.rect.centerx - 4, player.rect.bottom, 'down')
                player_bullets.add(bullet)
                player.shoot_cooldown = 20
            elif e.key == K_LEFT and player.shoot_cooldown == 0:
                bullet = Bullet(player.rect.left, player.rect.centery - 4, 'left')
                player_bullets.add(bullet)
                player.shoot_cooldown = 20
            elif e.key == K_RIGHT and player.shoot_cooldown == 0:
                bullet = Bullet(player.rect.right, player.rect.centery - 4, 'right')
                player_bullets.add(bullet)
                player.shoot_cooldown = 20
                
        elif e.type == KEYUP:
            if e.key in [K_w, K_s]:
                player.y_speed = 0
            if e.key in [K_a, K_d]:
                player.x_speed = 0
    
    if not finish:
        widow.blit(fon, (0, 0))
        barriers.draw(widow)
        final.reset()
        
        # Обновление игрока
        player.reset()
        player.update()
        
        # Обновление врагов
        for enemy in enemies:
            enemy.update(player)
            enemy.reset()
            
            # Стрельба врагов
            if isinstance(enemy, Drone):
                if enemy.shoot():
                    # Дрон стреляет в направлении игрока
                    dx = player.rect.centerx - enemy.rect.centerx
                    dy = player.rect.centery - enemy.rect.centery
                    
                    if abs(dx) > abs(dy):
                        if dx > 0:
                            bullet = Bullet(enemy.rect.right, enemy.rect.centery - 4, 'right', 3, True)
                        else:
                            bullet = Bullet(enemy.rect.left, enemy.rect.centery - 4, 'left', 3, True)
                    else:
                        if dy > 0:
                            bullet = Bullet(enemy.rect.centerx - 4, enemy.rect.bottom, 'down', 3, True)
                        else:
                            bullet = Bullet(enemy.rect.centerx - 4, enemy.rect.top, 'up', 3, True)
                    enemy_bullets.add(bullet)
            elif isinstance(enemy, Enemy):
                if enemy.shoot():
                    # Враг стреляет в случайном направлении
                    direction = random.choice(['up', 'down', 'left', 'right'])
                    bullet = Bullet(enemy.rect.centerx - 4, enemy.rect.centery - 4, direction, 3, True)
                    enemy_bullets.add(bullet)
        
        # Обновление пуль игрока
        for bullet in player_bullets:
            if bullet.update():
                player_bullets.remove(bullet)
            else:
                bullet.reset()
                
                # Проверка попадания во врагов
                hits = sprite.spritecollide(bullet, enemies, True)
                if hits:
                    player_bullets.remove(bullet)
        
        # Обновление пуль врагов
        for bullet in enemy_bullets:
            if bullet.update():
                enemy_bullets.remove(bullet)
            else:
                bullet.reset()
                
                # Проверка попадания в игрока
                if sprite.collide_rect(bullet, player):
                    player.hp -= 1
                    enemy_bullets.remove(bullet)
                    if player.hp <= 0:
                        finish = True
        
        # Проверка столкновения игрока с врагами с уменьшенными хитбоксами
        player_temp_rect = pygame.Rect(player.rect.x + 5, player.rect.y + 5, player.rect.width - 10, player.rect.height - 10)
        for enemy in enemies:
            enemy_temp_rect = pygame.Rect(enemy.rect.x + 5, enemy.rect.y + 5, enemy.rect.width - 10, enemy.rect.height - 10)
            if player_temp_rect.colliderect(enemy_temp_rect):
                player.hp -= 1
                # Телепортируем врага, чтобы не было постоянного урона
                enemy.rect.x = random.randint(50, 650)
                enemy.rect.y = random.randint(50, 450)
                if player.hp <= 0:
                    finish = True
                break
        
        # Проверка достижения финала с уменьшенными хитбоксами
        player_temp_rect = pygame.Rect(player.rect.x + 5, player.rect.y + 5, player.rect.width - 10, player.rect.height - 10)
        final_temp_rect = pygame.Rect(final.rect.x + 5, final.rect.y + 5, final.rect.width - 10, final.rect.height - 10)
        if player_temp_rect.colliderect(final_temp_rect):
            finish = True
        
        # Отображение HP
        hp_text = font.render(f"HP: {player.hp}", True, (255, 0, 0))
        widow.blit(hp_text, (10, 10))
        
    else:
        if player.hp <= 0:
            # Белый экран с надписью "проиграл ахаха"
            widow.fill((255, 255, 255))  # Белый фон
            lose_text = big_font.render("проиграл ахаха", True, (0, 0, 0))
            text_rect = lose_text.get_rect(center=(350, 200))
            widow.blit(lose_text, text_rect)
        else:
            widow.blit(win, (0, 0))
        
        text = font.render("R - рестарт", True, (0, 0, 0) if player.hp <= 0 else (255, 255, 255))
        text_rect = text.get_rect(center=(350, 400))
        widow.blit(text, text_rect)
    
    display.update()
