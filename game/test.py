import pygame
import random
import math
import os
import sys

# 初始化Pygame
pygame.init()
pygame.mixer.init()  # 初始化音频混音器

# 设置屏幕
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("太空冒险")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# 设置资源文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(current_dir, 'image')
music_dir = os.path.join(current_dir, 'music')

# 定义需要加载的图片文件列表
image_files = ['bg.png', 'rocket.png', 'meteor.png', 'coin.png', 'fuel_blue.png', 'fuel_red.png', 'fuel_orange.png', 'fuel_purple.png']

# 检查所有图片文件是否存在
for image_file in image_files:
    file_path = os.path.join(image_dir, image_file)
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 '{image_file}'")
        print(f"期望路径：{file_path}")
        pygame.quit()
        sys.exit(1)

# 加载图片
try:
    background = pygame.image.load(os.path.join(image_dir, 'bg.png'))
    rocket_img = pygame.image.load(os.path.join(image_dir, 'rocket.png'))
    meteor_img = pygame.image.load(os.path.join(image_dir, 'meteor.png'))
    coin_img = pygame.image.load(os.path.join(image_dir, 'coin.png'))
    fuel_blue_img = pygame.image.load(os.path.join(image_dir, 'fuel_blue.png'))
    fuel_red_img = pygame.image.load(os.path.join(image_dir, 'fuel_red.png'))
    fuel_orange_img = pygame.image.load(os.path.join(image_dir, 'fuel_orange.png'))
    fuel_purple_img = pygame.image.load(os.path.join(image_dir, 'fuel_purple.png'))
except pygame.error as e:
    print(f"加载图片时出错：{e}")
    pygame.quit()
    sys.exit(1)

# 缩放图片到合适的大小
rocket_img = pygame.transform.scale(rocket_img, (40, 60))
meteor_img = pygame.transform.scale(meteor_img, (30, 30))
coin_img = pygame.transform.scale(coin_img, (20, 20))
fuel_blue_img = pygame.transform.scale(fuel_blue_img, (20, 20))
fuel_red_img = pygame.transform.scale(fuel_red_img, (20, 20))
fuel_orange_img = pygame.transform.scale(fuel_orange_img, (20, 20))
fuel_purple_img = pygame.transform.scale(fuel_purple_img, (20, 20))

# 加载音效和背景音乐
try:
    coin_sound = pygame.mixer.Sound(os.path.join(music_dir, 'coin.mp3'))
    fuel_sound = pygame.mixer.Sound(os.path.join(music_dir, 'fuel.mp3'))
    fail_sound = pygame.mixer.Sound(os.path.join(music_dir, 'fail.mp3'))

    pygame.mixer.music.load(os.path.join(music_dir, 'bg.mp3'))
    pygame.mixer.music.set_volume(0.5)  # 设置背景音乐音量
except pygame.error as e:
    print(f"加载音频文件时出错：{e}")
    pygame.quit()
    sys.exit(1)

# 火箭类
class Rocket:
    def __init__(self):
        # 初始化火箭的位置、速度和状态
        self.x = WIDTH // 2  # 初始x坐标（屏幕中央）
        self.y = HEIGHT - 50  # 初始y坐标（屏幕底部上方50像素）
        self.speed = 5  # 移动速度
        self.invincible = False  # 无敌状态
        self.invincible_time = 0  # 无敌状态开始时间
        self.double_score = False  # 双倍得分状态
        self.double_score_time = 0  # 双倍得分状态开始时间

    def move(self, dx, dy):
        # 移动火箭，并确保不超出屏幕边界
        self.x = max(0, min(WIDTH - 40, self.x + dx * self.speed))
        self.y = max(0, min(HEIGHT - 60, self.y + dy * self.speed))

    def draw(self):
        # 绘制火箭
        screen.blit(rocket_img, (self.x, self.y))
        # 如果处于无敌状态，绘制一个橙色圆圈
        if self.invincible:
            pygame.draw.circle(screen, ORANGE, (int(self.x + 20), int(self.y + 30)), 30, 2)

# 陨石类
class Meteor:
    def __init__(self):
        # 初始化陨石的位置和速度
        self.x = random.randint(0, WIDTH - 30)  # 随机x坐标
        self.y = -30  # 初始y坐标（屏幕顶部上方）
        self.speed = random.uniform(1, 3)  # 随机下落速度

    def move(self):
        # 移动陨石（向下）
        self.y += self.speed

    def draw(self):
        # 绘制陨石
        screen.blit(meteor_img, (self.x, self.y))

# 道具类
class PowerUp:
    def __init__(self, type):
        # 初始化道具的位置、速度和类型
        self.x = random.randint(0, WIDTH - 20)  # 随机x坐标
        self.y = -20  # 初始y坐标（屏幕顶部上方）
        self.speed = 2  # 下落速度
        self.type = type  # 道具类型

    def move(self):
        # 移动道具（向下）
        self.y += self.speed

    def draw(self):
        # 根据道具类型绘制不同的图像
        if self.type == "coin":
            screen.blit(coin_img, (self.x, self.y))
        elif self.type == "slow_time":
            screen.blit(fuel_blue_img, (self.x, self.y))
        elif self.type == "speed_up":
            screen.blit(fuel_red_img, (self.x, self.y))
        elif self.type == "invincible":
            screen.blit(fuel_orange_img, (self.x, self.y))
        elif self.type == "double_score":
            screen.blit(fuel_purple_img, (self.x, self.y))

# 消息类
class Message:
    def __init__(self, text, color):
        # 初始化消息的文本、颜色和显示时间
        self.text = text
        self.color = color
        self.start_time = pygame.time.get_ticks()
        self.duration = 2000  # 消息显示2秒

    def draw(self, screen):
        # 在屏幕顶部绘制消息
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(WIDTH//2, 50))
        screen.blit(text_surface, text_rect)

# 绘制按钮函数
def draw_button(screen, text, x, y, width, height, normal_color, hover_color):
    # 获取鼠标位置和点击状态
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # 检查鼠标是否悬停在按钮上，并相应地改变颜色
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, normal_color, (x, y, width, height))
    
    # 绘制按钮文本
    small_font = pygame.font.Font(None, 32)
    text_surf = small_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surf, text_rect)
    return False

# 显示游戏结束界面
def show_game_over(screen, score, time):
    # 设置字体
    font = pygame.font.Font(None, 64)
    small_font = pygame.font.Font(None, 32)
    
    # 渲染文本
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    time_text = small_font.render(f"Time: {time}s", True, WHITE)
    
    # 设置按钮位置和大小
    button_width, button_height = 200, 50
    restart_button_x = WIDTH//2 - button_width - 20
    quit_button_x = WIDTH//2 + 20
    buttons_y = HEIGHT//2 + 100

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # 绘制游戏结束界面
        screen.fill(BLACK)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, HEIGHT//2 + 40))

        # 绘制重启和退出按钮
        if draw_button(screen, "Restart", restart_button_x, buttons_y, button_width, button_height, BLUE, PURPLE):
            return True
        if draw_button(screen, "Quit", quit_button_x, buttons_y, button_width, button_height, RED, ORANGE):
            return False

        pygame.display.flip()
    
    return False

# 游戏主循环
def game_loop():
    # 开始播放背景音乐
    pygame.mixer.music.play(-1)  # -1表示无限循环

    clock = pygame.time.Clock()
    rocket = Rocket()
    meteors = []
    powerups = []
    score = 0
    start_time = pygame.time.get_ticks()
    time_factor = 1
    font = pygame.font.Font(None, 36)
    messages = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 移动火箭
        keys = pygame.key.get_pressed()
        rocket.move(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
                    keys[pygame.K_DOWN] - keys[pygame.K_UP])

        # 生成陨石
        if random.random() < 0.02:
            meteors.append(Meteor())

        # 生成道具
        if random.random() < 0.01:
            powerups.append(PowerUp(random.choice(["coin", "slow_time", "speed_up", "invincible", "double_score"])))

        # 更新陨石位置
        for meteor in meteors[:]:
            meteor.move()
            if meteor.y > HEIGHT:
                meteors.remove(meteor)
                score += 1 * (2 if rocket.double_score else 1)

        # 更新道具位置
        for powerup in powerups[:]:
            powerup.move()
            if powerup.y > HEIGHT:
                powerups.remove(powerup)

        # 检测碰撞
        for meteor in meteors[:]:
            if (abs(meteor.x - rocket.x) < 30 and
                abs(meteor.y - rocket.y) < 30 and
                not rocket.invincible):
                fail_sound.play()  # 播放失败音效
                pygame.mixer.music.stop()  # 停止背景音乐
                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
                if show_game_over(screen, score, elapsed_time):
                    # 重新开始游戏
                    pygame.mixer.music.play(-1)  # 重新开始背景音乐
                    return True
                else:
                    # 退出游戏
                    return False

        # 检测道具拾取
        for powerup in powerups[:]:
            if abs(powerup.x - rocket.x) < 30 and abs(powerup.y - rocket.y) < 30:
                if powerup.type == "coin":
                    score += 10 * (2 if rocket.double_score else 1)
                    messages.append(Message("Coin +10 pts", GOLD))
                    coin_sound.play()  # 播放金币音效
                else:
                    fuel_sound.play()  # 播放燃料（道具）音效
                    if powerup.type == "slow_time":
                        time_factor = 0.5
                        messages.append(Message("Time Slowed", BLUE))
                    elif powerup.type == "speed_up":
                        rocket.speed += 2
                        messages.append(Message("Speed Up", RED))
                    elif powerup.type == "invincible":
                        rocket.invincible = True
                        rocket.invincible_time = pygame.time.get_ticks()
                        messages.append(Message("Invincible", ORANGE))
                    elif powerup.type == "double_score":
                        rocket.double_score = True
                        rocket.double_score_time = pygame.time.get_ticks()
                        messages.append(Message("Double Score", PURPLE))
                powerups.remove(powerup)

        # 更新无敌状态
        if rocket.invincible and pygame.time.get_ticks() - rocket.invincible_time > 5000:
            rocket.invincible = False

        # 更新双倍得分状态
        if rocket.double_score and pygame.time.get_ticks() - rocket.double_score_time > 10000:
            rocket.double_score = False

        # 更新时间减缓效果
        if time_factor < 1 and random.random() < 0.01:
            time_factor = min(1, time_factor + 0.1)

        # 绘制游戏元素
        screen.blit(background, (0, 0))
        rocket.draw()
        for meteor in meteors:
            meteor.draw()
        for powerup in powerups:
            powerup.draw()

        # 绘制消息
        current_time = pygame.time.get_ticks()
        for message in messages[:]:
            if current_time - message.start_time < message.duration:
                message.draw(screen)
            else:
                messages.remove(message)

        # 显示分数和时间
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        time_text = font.render(f"Time: {elapsed_time}s", True, WHITE)
        screen.blit(time_text, (10, 50))

        pygame.display.flip()
        clock.tick(60 * time_factor)

    pygame.mixer.music.stop()  # 确保在游戏结束时停止背景音乐
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Adventure")

    restart = True
    while restart:
        restart = game_loop()

    pygame.quit()

if __name__ == "__main__":
    main()