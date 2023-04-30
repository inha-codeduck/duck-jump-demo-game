import pygame
import random
import os
import sys

__author__ = "MARU"
__version__ = "0.0.1"

# 게임 화면 설정
WIDTH, HEIGHT = 800, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 게임 요소 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inha Duck Game")
clock = pygame.time.Clock()

# 오리 클래스
class Duck(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(resource_path("duck.png"))  # 오리 이미지 파일 불러오기
        self.image = pygame.transform.scale(self.image, (50, 50))  # 오리 크기 변경
        self.rect = self.image.get_rect()
        self.rect.x = width // 3
        self.rect.y = height - self.rect.height
        self.jump_height = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_height = 15

    def update(self, height):
        if self.is_jumping:
            self.rect.y -= self.jump_height
            self.jump_height -= 1
            if self.rect.y >= height - self.rect.height:
                self.rect.y = height - self.rect.height
                self.is_jumping = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 장애물 클래스
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(resource_path("cactus.png"))  # 장애물 이미지 파일 불러오기
        self.image = pygame.transform.scale(self.image, (50, 50))  # 장애물 크기 변경
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height - self.rect.height

    def update(self, game_speed):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 점수판 클래스
class Scoreboard:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen, score):
        score_text = self.font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

# 이미지의 상대경로를 가져옵니다.
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

# 게임의 시작 화면을 표시합니다.
def start_screen():
    button_font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 60)
    info_font = pygame.font.Font(None, 24)
    button_color = (100, 100, 255)
    button_hover_color = (150, 150, 255)

    title = title_font.render("Inha Duck Game", True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    button = button_font.render("Start", True, WHITE)
    button_rect = button.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
    button_bg_color = button_color

    author_text = info_font.render(f"Developer: {__author__}", True, BLACK)
    version_text = info_font.render(f"Version: {__version__}", True, BLACK)

    while True:
        screen.fill(WHITE)
        screen.blit(title, title_rect)
        screen.blit(author_text, (10, HEIGHT - 50))
        screen.blit(version_text, (10, HEIGHT - 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True
            if event.type == pygame.MOUSEMOTION:
                if button_rect.collidepoint(event.pos):
                    button_bg_color = button_hover_color
                else:
                    button_bg_color = button_color

        pygame.draw.rect(screen, button_bg_color, button_rect.inflate(10, 10))
        screen.blit(button, button_rect)
        pygame.display.update()
        clock.tick(30)

# 게임 오버 화면을 표시하고, 다시하기 버튼을 눌렀을 때 게임을 재시작합니다.
def game_over_screen(score):
    button_font = pygame.font.Font(None, 36)
    text_font = pygame.font.Font(None, 60)
    button_color = (100, 100, 255)
    button_hover_color = (150, 150, 255)

    text = text_font.render("Game Over", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    button = button_font.render("Restart", True, WHITE)
    button_rect = button.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
    button_bg_color = button_color

    while True:
        screen.fill(WHITE)
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True
            if event.type == pygame.MOUSEMOTION:
                if button_rect.collidepoint(event.pos):
                    button_bg_color = button_hover_color
                else:
                    button_bg_color = button_color

        pygame.draw.rect(screen, button_bg_color, button_rect.inflate(10, 10))
        screen.blit(button, button_rect)
        pygame.display.update()
        clock.tick(30)

# 게임 루프
def game_loop():
    running = True
    game_speed = 10
    score = 0
    obstacles = pygame.sprite.Group()
    duck = Duck(WIDTH, HEIGHT)
    score_board = Scoreboard()

    while running:
        clock.tick(30)
        screen.fill(WHITE)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    duck.jump()

        # 오리 점프
        duck.update(HEIGHT)

        # 장애물 생성
        if random.randint(0, 100) < 2:
            obstacles.add(Obstacle(WIDTH, HEIGHT))

        # 장애물 이동 및 충돌 처리
        for obstacle in obstacles:
            obstacle.update(game_speed)
            if duck.rect.colliderect(obstacle.rect):
                if game_over_screen(score):  # 게임 오버 시 게임 오버 화면 호출
                    return True
                else:
                    return False

        # 게임 속도 및 점수 관리
        game_speed += 0.001
        score += 1

        # 화면에 요소 그리기
        duck.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)
        score_board.draw(screen, score)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    print(f"Developer: {__author__}")
    print(f"Version: {__version__}")
    start_game = start_screen()
    if start_game:
        while True:
            play_again = game_loop()
            if not play_again:
                break
