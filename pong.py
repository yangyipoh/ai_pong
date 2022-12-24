import random
import math

class Pong:
  def __init__(self, width:int, height:int, network=None):
    self.width = width
    self.height = height
    self.score = [0, 0]
    self.ball = Ball()
    self.comp_paddle = Paddle(30)
    self.player_paddle = Paddle(self.width-30)
    self.bounce = 0
    self.network = network

  def update(self, player_input:int):
    if self.network is None:
      self.move_paddle(player_input)
    else:
      self.move_paddle_nn()
    self.update_comp()
    self.update_ball()

  def move_paddle(self, player_input:int):
    self.player_paddle.update_pos(player_input, self.height)
  
  def update_ball(self):
    has_bounced = self.ball.update_pos(self.height, self.player_paddle, self.comp_paddle)
    if has_bounced:
      self.bounce += 1
      self.ball.mag += 0.3
      self.ball.calculate_direction()
    if self.ball.position[0]+self.ball.radius > self.width:
      self.ball = Ball()
      self.score[0] += 1
    elif self.ball.position[0]-self.ball.radius < 0:
      self.ball = Ball()
      self.score[1] += 1

  def update_comp(self):
    target_y_pos = self.ball.position[1]
    curr_y_pos = self.comp_paddle.y_pos+self.comp_paddle.size//2
    if target_y_pos > curr_y_pos:
      self.comp_paddle.update_pos(1, self.height)
    elif target_y_pos < curr_y_pos:
      self.comp_paddle.update_pos(-1, self.height)
    else:
      self.comp_paddle.update_pos(0, self.height)
  
  def move_paddle_nn(self):
    ball_x = self.ball.position[0]/self.width
    ball_y = self.ball.position[1]/self.height
    vel_x = self.ball.direction[0]/self.ball.mag
    vel_y = self.ball.direction[1]/self.ball.mag
    pos_y = self.player_paddle.y_pos/self.height
    output = self.network.activate((ball_x, ball_y, vel_x, vel_y, pos_y))
    # output = net.activate((ball_x, ball_y, pos_y))
    if max(output) == output[0]:
      comp_input = 1
    elif max(output) == output[1]:
      comp_input = -1
    else:
      comp_input = 0
    self.player_paddle.update_pos(comp_input, self.height)


class Paddle:
  def __init__(self, x_pos:int):
    self.size = 75
    self.x_pos = x_pos
    self.y_pos = 240-self.size//2

  def update_pos(self, paddle_input:int, height:int):
    self.y_pos += paddle_input*5
    self.y_pos = min(max(self.y_pos, 0), height-self.size)


class Ball:
  def __init__(self):
    self.position = [320.0, 240.0]  # start ball initially in the middle of the screen
    self.radius = 10
    self.mag = 5
    # self.theta = random.random()*2*math.pi - math.pi
    self.theta = random.choice([math.pi/4, -math.pi/4, math.pi/6, -math.pi/6])
    self.direction = self.calculate_direction()

  def update_pos(self, height:int, player:Paddle, comp:Paddle):
    is_return = False
    # if ball collide with the top or bottom of the screen
    if self.position[1] < self.radius or self.position[1] > height - self.radius:
      self.theta = -self.theta
      self.normalise_angle()
      self.direction = self.calculate_direction()
    # if ball collides with the player paddle
    elif player.x_pos < self.position[0]+self.radius < player.x_pos+10 and \
          player.y_pos < self.position[1] < player.y_pos+player.size and \
            -math.pi/2 < self.theta < math.pi/2:
      is_return = True
      self.theta = math.pi-self.theta
      self.theta += random.random()*0.1-0.05
      self.normalise_angle()
      self.direction = self.calculate_direction()
    # if ball collides with the computer paddle
    elif comp.x_pos-10 < self.position[0]-self.radius < comp.x_pos and \
        comp.y_pos < self.position[1] < comp.y_pos+player.size and \
            (self.theta < -math.pi/2 or self.theta > math.pi/2):
      self.theta = math.pi-self.theta
      self.theta += random.random()*0.1-0.05
      self.normalise_angle()
      self.direction = self.calculate_direction()
    self.position[0] += self.direction[0]
    self.position[1] += self.direction[1]
    return is_return

  def calculate_direction(self):
    return [self.mag*math.cos(self.theta), self.mag*math.sin(self.theta)]

  def normalise_angle(self):
    self.theta -= 2*math.pi*math.floor((self.theta+math.pi)/(math.pi*2))
