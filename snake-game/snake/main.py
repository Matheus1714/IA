import sys
import pygame
from snake import utils
from snake.constants import Screen, Game
from snake.entity import Snake, Food
from snake.utils import checkered_surface, score_update


def game():
    pg_screen: pygame.Surface = pygame.display.get_surface()
    background = checkered_surface(pg_screen)
    clock = pygame.time.Clock()
    snake = Snake()
    foods = pygame.sprite.RenderPlain()
    foods.add(Food(snake))

    frametime = 0
    while True:
        pg_screen.blit(background, (0, 0))
        snake.update(frametime, foods)
        foods.update()
        snake.draw(pg_screen)
        foods.draw(pg_screen)
        score = len(snake.sprites()) - Game.NUM_UNITS_RESPAWN
        score_update(score)
        pygame.display.update()
        frametime = clock.tick(Screen.FPS)
        if snake.dead:
            return


def game_over():
    pg_screen: pygame.Surface = pygame.display.get_surface()
    background = checkered_surface(pg_screen)
    pg_screen.blit(background, (0, 0))
    utils.draw_center_text("Game over! Press any key to continue")
    pygame.display.update()
    # Avoid continuing from game over screen after death because of a missclick
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.update()


def main():
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption("Snake with pygame")
    pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))

    while True:
        game()
        game_over()


if __name__ == "__main__":
    main()
