#KEY METHODS USED
#pygame.display.set
#pygame.event and event.type
#pygame.time.Clock()
#.fill()
#pygame.display.update()
#pygame.key.get_pressed()

import pygame
pygame.init()

#Set height and width of the screen as variables
WIDTH, HEIGHT = 1600, 1000
#set the display to be same dimensions as height and width
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")#set window title

FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0) 

PADDLE_HEIGHT, PADDLE_WIDTH = (200, 20)

BALL_HEIGHT, BALL_WIDTH = (20, 20)

SCORE_FONT = pygame.font.SysFont("helvetica", 100)

#Class for paddle
class Paddle:
    COLOUR = WHITE
    VEL = 10#Speed of the paddles

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = self.originY = y
        self.width = width
        self.height = height

    #Draws the paddle onto the display for every frame per second  
    def draw(self,display):
        pygame.draw.rect(display, self.COLOUR, (self.x, self.y, self.width, self.height))

    #sets the move logic for the paddles
    def move(self, up=True):       
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    
    def paddleReset(self):
        self.y = self.originY

def ballCollision(ball, leftPaddle, rightPaddle):
    #reverses the ball.y value and velocity once 
    #it reaches the vertical end of the screen
    if ball.y + ball.height >= HEIGHT:   
        ball.yVel *= -1 
    elif ball.y  <= 0:
        ball.yVel *= -1

    #if ball is moving towards left paddle.
    if ball.xVel < 0:
        if ball.y + ball.height >= leftPaddle.y and ball.y - ball.height <= leftPaddle.y + leftPaddle.height:
            if ball.x <= leftPaddle.x + leftPaddle.width - 10:
                ball.xVel *= -1

                #Handles ball velocity relating to the distance between the
                #ball and the center of the left and right paddles.
                middleY = leftPaddle.y + leftPaddle.height/2
                displacementY = middleY - ball.y
                reduction = (leftPaddle.height/2)/ball.MAX
                yVel = displacementY / reduction
                ball.yVel = -1 * yVel
    else:
    #if ball is moving to right paddle
        if ball.y + ball.height >= rightPaddle.y and ball.y - ball.height <= rightPaddle.y + rightPaddle.height:
            if ball.x >= rightPaddle.x - 10:
                ball.xVel *= -1

                middleY = rightPaddle.y + rightPaddle.height/2
                displacementY = middleY - ball.y
                reduction = (rightPaddle.height/2)/ball.MAX
                yVel = displacementY / reduction
                ball.yVel = -1 * yVel
    #Handles movement for the paddles
def paddleMoveEvent(keys, leftPaddle, rightPaddle):
    if keys[pygame.K_w] and leftPaddle.y >= 15:
        leftPaddle.move(up=True)
    if keys[pygame.K_s] and leftPaddle.y + PADDLE_HEIGHT <= HEIGHT-15:
        leftPaddle.move(up=False)
    
    if keys[pygame.K_UP] and rightPaddle.y >= 15:
        rightPaddle.move(up=True)
    if keys[pygame.K_DOWN] and rightPaddle.y + PADDLE_HEIGHT <= HEIGHT-15:
        rightPaddle.move(up=False)

#Created class for ball
class Ball:
    MAX = 15
    COLOUR = WHITE
    
    def __init__(self,x,y,width,height):
        self.x = self.originX = x
        self.y = self.originY = y
        self.width = width
        self.height = height
        self.xVel = self.MAX
        self.yVel = 0 #at default, the ball is moving neither up nor down
    
    def draw(self, display):
        pygame.draw.rect(display, self.COLOUR, (self.x, self.y, BALL_WIDTH,BALL_HEIGHT))

    def move(self):
        self.x += self.xVel
        self.y += self.yVel
    
    def reset(self):
        self.x = self.originX
        self.y = self.originY
        self.xVel *= -1
        self.yVel = 0
    

#Function to draw game elements to the display
def draw(display, paddles, ball, leftScore, rightScore):
    display.fill(BLACK)

    #Draws the scores onto the display
    leftScoreText = SCORE_FONT.render(f"{leftScore}", 1, WHITE)
    rightScoreText = SCORE_FONT.render(f"{rightScore}", 1, WHITE)
    display.blit(leftScoreText, (WIDTH//4-leftScoreText.get_width()//2,40))
    display.blit(rightScoreText, (WIDTH * (3/4) - rightScoreText.get_width()//2,40))


    for i in paddles:
        i.draw(display)

    for line in range(10, HEIGHT, HEIGHT//10):
        if line % 2 == 1:
            continue
        pygame.draw.rect(display, WHITE, (WIDTH//2-5, line, 10, HEIGHT//20))

    ball.draw(display)

        
    pygame.display.update()#updates the display for each frame per second


#Main loop of the game
def main():
    run = True
    clock = pygame.time.Clock()

    #Create the left and right paddles
    leftPaddle = Paddle(10, (HEIGHT//2-PADDLE_HEIGHT//2),
                        PADDLE_WIDTH,PADDLE_HEIGHT)
    
    rightPaddle = Paddle(WIDTH-10-PADDLE_WIDTH, HEIGHT//2-PADDLE_HEIGHT//2, 
                         PADDLE_WIDTH, PADDLE_HEIGHT)
    
    ball = Ball(WIDTH//2-BALL_WIDTH//2, HEIGHT//2-BALL_HEIGHT//2, BALL_WIDTH, BALL_HEIGHT)

    leftScore = 0
    rightScore = 0

    #main loop
    while run:
        clock.tick(FPS)#regulate the fps basically.
        draw(DISPLAY, [leftPaddle,rightPaddle], ball, leftScore, rightScore)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        keys = pygame.key.get_pressed()
        paddleMoveEvent(keys,leftPaddle,rightPaddle)
        
        ball.move()
        ballCollision(ball, leftPaddle, rightPaddle)

        if ball.x < 0:
            rightScore += 1
            ball.reset()
            leftPaddle.paddleReset()
            rightPaddle.paddleReset()
        elif ball.x > WIDTH:
            leftScore += 1
            ball.reset()
            leftPaddle.paddleReset()
            rightPaddle.paddleReset()

    pygame.quit()

#runs the game.
main()