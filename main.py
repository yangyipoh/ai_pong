import pygame
import sys
from pong import Pong
import pickle
import argparse

BLACK = (0,0,0)
WHITE = (255,255,255)

def draw(surf, game, font):
  # middle lines
  pygame.draw.line(surf, WHITE, (game.width//2-1, 0), (game.width//2-1, game.height), width=3)

  # ball
  pygame.draw.circle(surf, WHITE, game.ball.position, game.ball.radius)

  # computer paddle
  paddle_shape = pygame.Rect(game.comp_paddle.x_pos-10, game.comp_paddle.y_pos, 10, game.comp_paddle.size)
  pygame.draw.rect(surf, WHITE, paddle_shape)
  paddle_shape = pygame.Rect(game.player_paddle.x_pos, game.player_paddle.y_pos, 10, game.player_paddle.size)
  pygame.draw.rect(surf, WHITE, paddle_shape)

  # score
  text = font.render(str(game.score[0]), True, WHITE)
  text_rect = text.get_rect()
  text_rect.center = (game.width//2-10-25, 10+25)
  surf.blit(text, text_rect)

  text = font.render(str(game.score[1]), True, WHITE)
  text_rect = text.get_rect()
  text_rect.center = (game.width//2+10+25, 10+25)
  surf.blit(text, text_rect)

def main():
  global BLACK, WHITE
  parser = argparse.ArgumentParser()
  parser.add_argument('--network', action='store_false', help='Use neural network or not (Default: False)')
  args = parser.parse_args()
  use_ai = args.network

  pygame.init()
  pygame.display.set_caption('Crappy Pong')
  font = pygame.font.Font('freesansbold.ttf', 32)
  fps = 120
  fpsClock = pygame.time.Clock()
  width, height = 640, 480
  screen = pygame.display.set_mode((width, height))

  # loading in network
  if use_ai:
    network = None
  else:
    with open('network.pkl', 'rb') as f:
      network = pickle.load(f)
  game = Pong(width, height, network)
  while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    
    player_input = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
      player_input = -1
    elif keys[pygame.K_DOWN]:
      player_input = 1

    # Update.
    game.update(player_input)

    # Draw.
    draw(screen, game, font)
    pygame.display.flip()

    if max(game.score) == 10:
      if game.score[0] > game.score[1]:
        print('Congrats Player 1')
      else:
        print('Congrats Player 2')
      break

    fpsClock.tick(fps)
  pygame.quit()
  sys.exit()


if __name__ == '__main__':
    main()
