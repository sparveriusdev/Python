import os
import time
import sys
import termios
import tty
import chime

# Configuración inicial
WIDTH = 64
HEIGHT = 32
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_dir = [1, 1]
paddle1_pos = HEIGHT // 2
paddle2_pos = HEIGHT // 2
PADDLE_SIZE = 4
score_a = 0
score_b = 0
WINNING_SCORE = 2

# Colores ANSI
GREEN = '\033[32m'
RESET = '\033[0m'

def clear_screen():
    os.system('clear')

def print_board():
    clear_screen()
    score_text = f"Jugador A: {score_a} - Jugador B: {score_b}"
    print(f"{GREEN}{score_text.center(WIDTH)}{RESET}")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x == 0 or x == WIDTH - 1:
                print(f'{GREEN}|{RESET}', end='')
            elif y == 0 or y == HEIGHT - 1:
                print(f'{GREEN}-{RESET}', end='')
            elif (x == ball_pos[0] and y == ball_pos[1]):
                print(f'{GREEN}o{RESET}', end='')
            elif x == 1 and (paddle1_pos <= y < paddle1_pos + PADDLE_SIZE):
                print(f'{GREEN}|{RESET}', end='')
            elif x == WIDTH - 2 and (paddle2_pos <= y < paddle2_pos + PADDLE_SIZE):
                print(f'{GREEN}|{RESET}', end='')
            else:
                print(' ', end='')
        print()

def move_ball():
    global ball_pos, ball_dir, score_a, score_b

    next_x = ball_pos[0] + ball_dir[0]
    next_y = ball_pos[1] + ball_dir[1]

    if next_x == 1:
        if paddle1_pos <= next_y < paddle1_pos + PADDLE_SIZE:
            ball_dir[0] = -ball_dir[0]
            play_sound_hit()
        else:
            score_b += 1
            reset_ball()
            return
    elif next_x == WIDTH - 2:
        if paddle2_pos <= next_y < paddle2_pos + PADDLE_SIZE:
            ball_dir[0] = -ball_dir[0]
            play_sound_hit()
        else:
            score_a += 1
            reset_ball()
            return

    if next_y <= 0 or next_y >= HEIGHT - 1:
        ball_dir[1] = -ball_dir[1]

    ball_pos[0] += ball_dir[0]
    ball_pos[1] += ball_dir[1]

def reset_ball():
    global ball_pos, ball_dir
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_dir = [1, 1]

def reset_game():
    global score_a, score_b, paddle1_pos, paddle2_pos
    score_a = 0
    score_b = 0
    paddle1_pos = HEIGHT // 2
    paddle2_pos = HEIGHT // 2
    reset_ball()

def move_paddle(paddle, direction):
    global paddle1_pos, paddle2_pos

    if paddle == 1:
        if 0 < paddle1_pos + direction < HEIGHT - PADDLE_SIZE:
            paddle1_pos += direction
    else:
        if 0 < paddle2_pos + direction < HEIGHT - PADDLE_SIZE:
            paddle2_pos += direction

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def check_winner():
    if score_a >= WINNING_SCORE:
        play_sound_win()
        print(f"{GREEN}Jugador A ha ganado!{RESET}".center(WIDTH))
        return True
    elif score_b >= WINNING_SCORE:
        play_sound_win()
        print(f"{GREEN}Jugador B ha ganado!{RESET}".center(WIDTH))
        return True
    return False

def play_sound_hit():
    chime.warning()

def play_sound_win():
    for _ in range(3):
        chime.success()

# Bucle principal del juego
while True:
    if check_winner():
        while True:
            key = get_key()
            if key == '\x1b':  # Esc key
                sys.exit()
            elif key == '\r':  # Enter key
                reset_game()
                break
    else:
        print_board()
        move_ball()

        key = get_key()
        if key == 'w':
            move_paddle(1, -1)
        elif key == 's':
            move_paddle(1, 1)
        elif key == 'i':
            move_paddle(2, -1)
        elif key == 'k':
            move_paddle(2, 1)
        elif key == '\x1b':  # Esc key
            sys.exit()
        elif key == '\r':  # Enter key
            reset_game()

        time.sleep(0.05)  # Ajustamos el tiempo de espera para mayor fluidez
