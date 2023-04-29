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
    # 코드 작성

# 장애물 클래스
class Obstacle(pygame.sprite.Sprite):
    # 코드 작성

# 점수판 클래스
class Scoreboard():
    # 코드 작성

# 게임 루프
def game_loop():
    running = True
    jump = False
    game_speed = 10
    score = 0
    obstacles = pygame.sprite.Group()
    duck = Duck(WIDTH, HEIGHT)

    while running:
        clock.tick(30)
        screen.fill(WHITE)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 코드 작성: 공룡 점프, 장애물 생성 및 충돌 처리, 게임 속도 및 점수 관리

        # 화면에 요소 그리기
        duck.draw(screen)
        obstacles.draw(screen)
        Scoreboard.draw(screen, score)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    game_loop()
