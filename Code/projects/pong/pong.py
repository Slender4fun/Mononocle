import display
import touch
import time

# Game variables
paddle_height = 40  # Adjusted size
paddle_width = 5    # Adjusted size
ball_size = 15       # Adjusted size
screen_width = display.WIDTH
screen_height = display.HEIGHT

paddle_speed = 5    # Speed of paddle movement
ai_paddle_speed = 3

# Initial positions
paddle1_y = screen_height / 2
paddle2_y = screen_height / 2
ball_x = int(screen_width / 2)
ball_y = int(screen_height / 2)
ball_speed_x = -5  # Adjusted speed
ball_speed_y = 5  # Adjusted speed

# ui
score_player = 0
score_ai = 0

field_top = display.Line(8, 8, screen_width-8, 8, display.WHITE)
field_bottom = display.Line(8, screen_height-8, screen_width-8, screen_height-8, display.WHITE)

field = (field_top, field_bottom)
def draw_scene():
    global paddle1_y, paddle2_y, ball_x, ball_y, ball_speed_x, ball_speed_y, score_player, score_ai
    scoreboard = display.Text(f"{score_player} : {score_ai}", display.WIDTH/2, 10, display.WHITE, justify=display.TOP_CENTER)
    # Draw paddles
    paddle1 = display.Rectangle(10, int(paddle1_y - paddle_height / 2), paddle_width, int(paddle1_y + paddle_height / 2), display.WHITE)
    paddle2 = display.Rectangle(screen_width - 10 - paddle_width, int(paddle2_y - paddle_height / 2), screen_width - 10, int(paddle2_y + paddle_height / 2), display.WHITE)
    # Draw ball
    ball = display.Rectangle(int(ball_x - ball_size / 2), int(ball_y - ball_size / 2), int(ball_x + ball_size / 2), int(ball_y + ball_size / 2), display.GREEN)

    display.show(field, paddle1, paddle2, ball, scoreboard)
    # time.sleep(1)

def update_positions():
    global paddle1_y, paddle2_y, ball_x, ball_y, ball_speed_x, ball_speed_y
    
    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # Move AI paddle
    if ball_y > paddle2_y + ai_paddle_speed:
        paddle2_y += ai_paddle_speed
    elif ball_y < paddle2_y - ai_paddle_speed:
        paddle2_y -= ai_paddle_speed
    
    # Collision with walls
    if ball_y - ball_size // 2 < 0 or ball_y + ball_size // 2 > screen_height:
        ball_speed_y *= -1
    # Collision with paddles
    if ball_x - ball_size // 2 < 10 + paddle_width and paddle1_y - paddle_height // 2 < ball_y < paddle1_y + paddle_height // 2:
        ball_speed_x *= -1
    elif ball_x + ball_size // 2 > screen_width - 10 - paddle_width and paddle2_y - paddle_height // 2 < ball_y < paddle2_y + paddle_height // 2:
        ball_speed_x *= -1

def main():
    global paddle1_y, paddle2_y, ball_speed_x, ball_speed_y, score_player, score_ai, paddle_speed, ball_x, ball_y
    i = 1
    while i < 1000:
        # Check touch state
        if touch.state(touch.A):
            paddle1_y -= paddle_speed  # Move up
        elif touch.state(touch.B):
            paddle1_y += paddle_speed  # Move down

        paddle1_y = max(paddle_height / 2, min(screen_height - paddle_height / 2, paddle1_y))
        paddle2_y = max(paddle_height / 2, min(screen_height - paddle_height / 2, paddle2_y))

        draw_scene()
        update_positions()

        if ball_x < 0:
            ball_x = int(screen_width / 2)
            ball_y = int(screen_height / 2)
            ball_speed_x *= -1
            score_ai += 1
        elif ball_x > screen_width:
            ball_x = int(screen_width / 2)
            ball_y = int(screen_height / 2)
            ball_speed_x *= -1
            score_player += 1

        i += 1
    
main()
