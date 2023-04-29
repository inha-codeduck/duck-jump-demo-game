import pygame
import random

# 게임 화면 설정
WIDTH, HEIGHT = 800, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 게임 요소 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Game")
clock = pygame.time.Clock()

# 오리 클래스
class Duck(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("duck.png")  # 오리 이미지 파일 불러오기
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
        self.image = pygame.image.load("cactus.png")  # 장애물 이미지 파일 불러오기
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
                running = False

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
    game_loop()
