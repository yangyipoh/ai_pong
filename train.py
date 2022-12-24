import sys
import os
import pygame
import neat
from pong import Pong
import pickle

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GENERATION = 0

def draw(surf, games, font, idx:int):
  game = games[idx][2]
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

  # game index
  text = font.render(f'Game: {idx}', True, WHITE)
  text_rect = text.get_rect()
  text_rect.center = (10+70, 10+25)
  surf.blit(text, text_rect)

  # game index
  text = font.render(f'Gen: {GENERATION}', True, WHITE)
  text_rect = text.get_rect()
  text_rect.center = (game.width-10-70, 10+25)
  surf.blit(text, text_rect)

def fitness(genomes, config):
  global BLACK, WHITE, GENERATION
  GENERATION += 1
  pygame.init()
  pygame.display.set_caption('Crappy Pong')
  font = pygame.font.Font('freesansbold.ttf', 32)
  fps = 60
  fpsClock = pygame.time.Clock()
  width, height = 640, 480
  screen = pygame.display.set_mode((width, height))

  agents = []
  for _, genome in genomes:
    genome.fitness = 0  # start with fitness level of 0
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = Pong(width, height)
    agent = (net, genome, game)
    agents.append(agent)
  
  run_time = 2  # run for 1 minute
  game_idx = 0

  # Game loop.
  for _ in range(fps*60*run_time):
    screen.fill(BLACK)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          game_idx = (game_idx + 1)%len(agents)
        elif event.key == pygame.K_DOWN:
          game_idx = (game_idx - 1)%len(agents)

    # Update.
    for net, genome, game in agents:
      ball_x = game.ball.position[0]/width
      ball_y = game.ball.position[1]/height
      vel_x = game.ball.direction[0]/game.ball.mag
      vel_y = game.ball.direction[1]/game.ball.mag
      pos_y = game.player_paddle.y_pos/height
      output = net.activate((ball_x, ball_y, vel_x, vel_y, pos_y))
      # output = net.activate((ball_x, ball_y, pos_y))
      if max(output) == output[0]:
        player_input = 1
      elif max(output) == output[1]:
        player_input = -1
      else:
        player_input = 0
      game.update(player_input)

    # Draw.
    draw(screen, agents, font, game_idx)

    pygame.display.flip()
    # fpsClock.tick(fps)  # uncomment if you want to train in real time
  
  for net, genome, game in agents:
    genome.fitness = 0.1*game.bounce + 5*game.score[1] - 2*game.score[0]
    if genome.fitness > 12:
      with open('network.pkl', 'wb') as f:
        pickle.dump(net, f)

def main():
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, 'config.ini')
  config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                              neat.DefaultSpeciesSet, neat.DefaultStagnation,
                              config_path)
  p = neat.Population(config)

  p.add_reporter(neat.StdOutReporter(True))
  stats = neat.StatisticsReporter()
  p.add_reporter(stats)

  winner = p.run(fitness, 50)
  print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
  main()
