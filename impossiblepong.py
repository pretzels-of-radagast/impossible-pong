import pygame, math
import pygame.gfxdraw

# PYGAME ====================

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Pong')

clock = pygame.time.Clock()

# OBJECTS ====================

first = True

ball_pos = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
ball_r = 8
ball_speed = 0
ball_dir = 150

change_x = 0
change_y = 0

collisions = 0

paddle_width = 20
paddle_height = 100
paddle_rect = (20, 100)

paddle_one = pygame.Rect((60, (SCREEN_HEIGHT - paddle_height) / 2), paddle_rect)
paddle_two = pygame.Rect((SCREEN_WIDTH - 60, (SCREEN_HEIGHT - paddle_height) / 2), paddle_rect)

score_one = 0
score_two = 0

score_font = pygame.font.SysFont('verdana', 48)

keys = [False] * 5

two_y = paddle_two.y - paddle_two.height / 2

# COLORS ====================

black = (0, 0, 0)
white = (255, 255, 255)


def y_range(rect1, rect2):
   return rect1.y + rect1.height >= rect2.y and rect1.y <= rect2.y + rect2.height


def x_range(rect1, rect2):
   return rect1.x + rect1.width >= rect2.x and rect1.x <= rect2.x + rect2.width


def generate_two_y(paddle=False):

   ball_pos_copy = ball_pos.copy()
   ball_copy_dir = ball_dir

   while ball_pos_copy[0] + ball_r < paddle_two.x or math.cos(math.radians(ball_copy_dir)) < 0:
       ball_copy_dir %= 360

       '''y_miss = lambda rect: ball_rect.y + ball_rect.height < rect.y or ball_rect.y > rect.y + rect.height
       x_miss = lambda rect: ball_rect.x + ball_rect.width < rect.x or ball_rect.x > rect.x + rect.width'''
       # print('start')
       # print(ball_pos_copy, ball_copy_dir)

       # X - Collision
       # print('paddle collis')

       if paddle and ball_pos_copy[0] - ball_r <= paddle_one.x+paddle_one.width and math.cos(math.radians(ball_copy_dir)) < 0:
           ball_copy_dir = 180 - ball_copy_dir
           print('paddle')

       #print(ball_pos_copy, ball_copy_dir)

       #print('move ball')

       # Move ball

       ball_pos_copy[0] += ball_speed * math.cos(math.radians(ball_copy_dir))
       ball_pos_copy[1] -= ball_speed * math.sin(math.radians(ball_copy_dir))

       ball_pos_copy = [int(x) for x in ball_pos_copy]

       # print(ball_pos_copy, ball_copy_dir)
       # print('edge collis')

       if ball_pos_copy[0] + ball_r > SCREEN_WIDTH:
           ball_copy_dir = 180 - ball_copy_dir
           ball_pos_copy[0] = SCREEN_WIDTH - ball_r
       elif ball_pos_copy[0] - ball_r <= 0:
           ball_copy_dir = 180 - ball_copy_dir
           ball_pos_copy[0] = ball_r

       if ball_pos_copy[1] + ball_r > SCREEN_HEIGHT:
           ball_copy_dir = 360 - ball_copy_dir
           ball_pos_copy[1] = SCREEN_HEIGHT - ball_r
       elif ball_pos_copy[1] - ball_r <= 0:
           ball_copy_dir = 360 - ball_copy_dir
           ball_pos_copy[1] = ball_r

       # print(ball_pos_copy, ball_copy_dir)

       '''if ball_pos_copy[0] + ball_r >= paddle_two.x:
           break'''

   # steps = (paddle_two.x - ball_pos[0]) / ball_speed * math.cos(math.radians(ball_dir))
   # ychange = steps * ball_speed * math.sin(math.radians(ball_dir))
   # return int(ychange % SCREEN_HEIGHT) if int(ychange / SCREEN_HEIGHT) % 2 == 0 else SCREEN_HEIGHT - int(ychange % SCREEN_HEIGHT)

   print(ball_pos_copy)
   return ball_pos_copy[1]


while True:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           quit()
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_w:     keys[0] = True
           if event.key == pygame.K_s:     keys[1] = True
           # if event.key == pygame.K_UP:    keys[2] = True
           # if event.key == pygame.K_DOWN:  keys[3] = True

           if first and event.key == pygame.K_SPACE:  # Start
               ball_speed = 4
               first = False
           if event.key == pygame.K_r:  # Reset
               first = True

               ball_pos = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
               ball_speed = change_x = change_y = collisions = 0
               ball_dir = 150

               paddle_one = pygame.Rect((60, (SCREEN_HEIGHT - paddle_height) / 2), paddle_rect)
               paddle_two = pygame.Rect((SCREEN_WIDTH - 60, (SCREEN_HEIGHT - paddle_height) / 2), paddle_rect)

               score_one = 0
               score_two = 0

       if event.type == pygame.KEYUP:
           if event.key == pygame.K_w:     keys[0] = False
           if event.key == pygame.K_s:     keys[1] = False
           # if event.key == pygame.K_UP:    keys[2] = False
           # if event.key == pygame.K_DOWN:  keys[3] = False

   # Move Paddle

   one_change = two_change = 0

   if keys[0]:
       paddle_one.y -= 5
       one_change = -5
   if keys[1]:
       paddle_one.y += 5
       one_change = 5

   if abs((paddle_two.y + paddle_two.height/2) - two_y) > paddle_two.height/2:
       if two_y > paddle_two.y:
           paddle_two.y += 5
           two_change = 5
           #print('down')
       else:
           paddle_two.y -= 5
           two_change = -5
           #print('up')

   '''if keys[2]:
       paddle_two.y -= 5
       two_change = -5
   if keys[3]:
       paddle_two.y += 5
       two_change = 5'''

   if paddle_one.y < 0:
       paddle_one.y = 0
   elif paddle_one.y + paddle_one.height > SCREEN_HEIGHT:
       paddle_one.y = SCREEN_HEIGHT - paddle_one.height

   if paddle_two.y < 0:
       paddle_two.y = 0
   elif paddle_two.y + paddle_two.height > SCREEN_HEIGHT:
       paddle_two.y = SCREEN_HEIGHT - paddle_two.height

   # Ball Collisions

   change_x = ball_speed * math.cos(math.radians(ball_dir))
   change_y = -ball_speed * math.sin(math.radians(ball_dir))

   ball_rect = pygame.Rect((ball_pos[0] - ball_r, ball_pos[1] - ball_r), (ball_r * 2, ball_r * 2))

   ball_rect_x = pygame.Rect((ball_pos[0] - ball_r + change_x, ball_pos[1] - ball_r), (ball_r * 2, ball_r * 2))
   ball_rect_y = pygame.Rect((ball_pos[0] - ball_r, ball_pos[1] - ball_r + change_y), (ball_r * 2, ball_r * 2))

   one_collide = paddle_one.colliderect(ball_rect)
   two_collide = paddle_two.colliderect(ball_rect)

   '''y_miss = lambda rect: ball_rect.y + ball_rect.height < rect.y or ball_rect.y > rect.y + rect.height
   x_miss = lambda rect: ball_rect.x + ball_rect.width < rect.x or ball_rect.x > rect.x + rect.width'''

   # X - Collision

   if paddle_one.colliderect(ball_rect_x) and y_range(ball_rect_x, paddle_one):
       ball_dir = 180 - ball_dir
       collisions += 1

       two_y = generate_two_y()
       print(two_y)

   elif paddle_two.colliderect(ball_rect_x) and y_range(ball_rect_x, paddle_two):
       ball_dir = 180 - ball_dir
       collisions += 1

       two_y = generate_two_y(paddle=True)
       print(two_y)

   if collisions == 6 and ball_speed <= 10:  # speed ball up
       collisions = 0
       ball_speed += 1

       two_y = generate_two_y()
       print(two_y)

       # Y - Collision

   if paddle_one.colliderect(ball_rect_y) and x_range(ball_rect_y, paddle_one):
       if change_y - one_change > 0:
           ball_pos[1] = paddle_one.top - ball_r
       else:
           ball_pos[1] = paddle_one.bottom + ball_r

       ball_dir = 360 - ball_dir

       two_y = generate_two_y()
       print(two_y)

   elif paddle_two.colliderect(ball_rect_y) and x_range(ball_rect_y, paddle_two):
       if change_y - two_change > 0:
           ball_pos[1] = paddle_two.top - ball_r
       else:
           ball_pos[1] = paddle_two.bottom + ball_r

       ball_dir = 360 - ball_dir

   # Move ball

   ball_pos[0] += ball_speed * math.cos(math.radians(ball_dir))
   ball_pos[1] -= ball_speed * math.sin(math.radians(ball_dir))

   ball_pos = [int(x) for x in ball_pos]

   if ball_pos[0] + ball_r > SCREEN_WIDTH:
       ball_dir = 180 - ball_dir
       ball_pos[0] = SCREEN_WIDTH - ball_r
       score_one += 1
   elif ball_pos[0] - ball_r <= 0:
       ball_dir = 180 - ball_dir
       ball_pos[0] = ball_r
       score_two += 1

       two_y = generate_two_y()
       print(two_y)

   if ball_pos[1] + ball_r > SCREEN_HEIGHT:
       ball_dir = 360 - ball_dir
       ball_pos[1] = SCREEN_HEIGHT - ball_r

       '''two_y = generate_two_y()
       print(two_y)'''

   elif ball_pos[1] - ball_r <= 0:
       ball_dir = 360 - ball_dir
       ball_pos[1] = ball_r

       '''two_y = generate_two_y()
       print(two_y)'''

   # if abs(ball_pos[0] - paddle_two.x) < ball_speed * math.cos(math.radians(ball_dir)) and ball_speed * math.cos(math.radians(ball_dir)) > 0:
   #     print(ball_pos[1])

   # Draw Screen

   screen.fill(black)

   pygame.draw.rect(screen, white, paddle_one)
   pygame.draw.rect(screen, white, paddle_two)

   pygame.gfxdraw.aacircle(screen, int(ball_pos[0]), int(ball_pos[1]), ball_r-1, white)
   pygame.draw.circle(screen, white, ball_pos, ball_r)

   score_surface = score_font.render(str(score_one) + '  ' + str(score_two), True, white)

   screen.blit(score_surface, (int((SCREEN_WIDTH - score_surface.get_width()) / 2), 40))

   pygame.display.update()

   clock.tick(60)
