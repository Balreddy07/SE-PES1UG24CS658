import os
import pygame

try:
    from .paddle import Paddle
    from .ball import Ball
    from .brick import Brick
except ImportError:
    from game.paddle import Paddle
    from game.ball import Ball
    from game.brick import Brick

__all__ = ["GameEngine"]

# Game Engine

WHITE = (255, 255, 255)
BG = (15, 15, 25)
BRICK_COLORS = [
    (200, 60, 60),
    (200, 140, 60),
    (200, 200, 60),
    (80, 180, 80),
    (80, 140, 200),
]

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.paddle = Paddle(width // 2 - 50, height - 30, 100, 14)

        self.ball = Ball(width // 2, height - 50, radius=8)
        self.ball.vx, self.ball.vy = 4, -4

        self.rows, self.cols = 5, 8
        self.font = pygame.font.SysFont("Arial", 28)
        self.title_font = pygame.font.SysFont("Arial", 46, bold=True)
        self.sub_font = pygame.font.SysFont("Arial", 22)
        self.option_font = pygame.font.SysFont("Arial", 20)

        self.difficulty = "medium"
        self.base_speed = 4
        self._init_sounds()
        self.restart_game("medium")

    def _init_sounds(self):
        self.sound_paddle = None
        self.sound_brick = None
        self.sound_wall = None
        self.sound_win = None
        self.sound_lose = None

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sound_dir = os.path.join(base_dir, "assets", "sounds")

            def load_sound(name):
                path = os.path.join(sound_dir, name)
                if os.path.exists(path):
                    return pygame.mixer.Sound(path)
                return None

            self.sound_paddle = load_sound("paddle.wav")
            self.sound_brick = load_sound("brick.wav")
            self.sound_wall = load_sound("wall.wav")
            self.sound_win = load_sound("win.wav")
            self.sound_lose = load_sound("lose.wav")
        except Exception:
            pass

    def _play_sound(self, sound):
        if sound is not None:
            try:
                if pygame.mixer.get_init():
                    sound.play()
            except Exception:
                pass

    def restart_game(self, difficulty="medium"):
        self.difficulty = difficulty
        if difficulty == "easy":
            paddle_width = 130
            self.base_speed = 3
        elif difficulty == "hard":
            paddle_width = 70
            self.base_speed = 6
        else:  # "medium"
            paddle_width = 100
            self.base_speed = 4

        self.paddle = Paddle(self.width // 2 - paddle_width // 2, self.height - 30, paddle_width, 14)
        self.ball = Ball(self.width // 2, self.height - 50, radius=8)
        self.ball.vx, self.ball.vy = self.base_speed, -self.base_speed

        self.bricks = self._build_bricks(self.rows, self.cols)
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.result = None

    def _build_bricks(self, rows, cols):
        bricks = []
        margin, gap, top = 30, 6, 60
        brick_w = (self.width - margin * 2 - gap * (cols - 1)) // cols
        brick_h = 22
        for r in range(rows):
            for c in range(cols):
                x = margin + c * (brick_w + gap)
                y = top + r * (brick_h + gap)
                bricks.append(Brick(x, y, brick_w, brick_h))
        return bricks

    def handle_event(self, event):
        if self.game_over and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_1, pygame.K_e):
                self.restart_game("easy")
            elif event.key in (pygame.K_2, pygame.K_m):
                self.restart_game("medium")
            elif event.key in (pygame.K_3, pygame.K_h):
                self.restart_game("hard")
            elif event.key in (pygame.K_4, pygame.K_q, pygame.K_ESCAPE):
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_input(self):
        if self.game_over:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.move(-self.paddle.speed, self.width)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.move(self.paddle.speed, self.width)

    def _resolve_collision(self, rect):
        """
        Determines the side of collision with `rect`, reverses the appropriate velocity
        component (vx for horizontal, vy for vertical), and repositions the ball to prevent sticking.
        """
        ball_rect = self.ball.rect()
        if not ball_rect.colliderect(rect):
            return False

        # Previous position before this frame's move
        prev_x = self.ball.x - self.ball.vx
        prev_y = self.ball.y - self.ball.vy
        prev_rect = pygame.Rect(
            prev_x - self.ball.radius,
            prev_y - self.ball.radius,
            self.ball.radius * 2,
            self.ball.radius * 2,
        )

        from_above = prev_rect.bottom <= rect.top
        from_below = prev_rect.top >= rect.bottom
        from_left = prev_rect.right <= rect.left
        from_right = prev_rect.left >= rect.right

        overlap_left = ball_rect.right - rect.left
        overlap_right = rect.right - ball_rect.left
        overlap_top = ball_rect.bottom - rect.top
        overlap_bottom = rect.bottom - ball_rect.top

        # Distinguish horizontal vs vertical collision
        if (from_above or from_below) and not (from_left or from_right):
            side = "vertical"
        elif (from_left or from_right) and not (from_above or from_below):
            side = "horizontal"
        else:
            # Corner collision or already overlapping: compare penetration depths
            pen_x = overlap_left if self.ball.vx > 0 else overlap_right
            pen_y = overlap_top if self.ball.vy > 0 else overlap_bottom
            if pen_x < pen_y:
                side = "horizontal"
            elif pen_y < pen_x:
                side = "vertical"
            else:
                side = "both"

        if side in ("horizontal", "both"):
            hit_left = from_left or (not from_right and overlap_left < overlap_right)
            self.ball.vx = -abs(self.ball.vx) if hit_left else abs(self.ball.vx)
            self.ball.x = (rect.left - self.ball.radius) if hit_left else (rect.right + self.ball.radius)

        if side in ("vertical", "both"):
            hit_top = from_above or (not from_below and overlap_top < overlap_bottom)
            self.ball.vy = -abs(self.ball.vy) if hit_top else abs(self.ball.vy)
            self.ball.y = (rect.top - self.ball.radius) if hit_top else (rect.bottom + self.ball.radius)

        return True

    def update(self):
        if self.game_over:
            return

        self.ball.move()

        # Wall collisions with clamping to prevent sticking
        hit_wall = False
        if self.ball.x - self.ball.radius <= 0:
            self.ball.vx = abs(self.ball.vx)
            self.ball.x = self.ball.radius
            hit_wall = True
        elif self.ball.x + self.ball.radius >= self.width:
            self.ball.vx = -abs(self.ball.vx)
            self.ball.x = self.width - self.ball.radius
            hit_wall = True

        if self.ball.y - self.ball.radius <= 0:
            self.ball.vy = abs(self.ball.vy)
            self.ball.y = self.ball.radius
            hit_wall = True

        if hit_wall:
            self._play_sound(self.sound_wall)

        # Paddle collision
        if self._resolve_collision(self.paddle.rect()):
            self._play_sound(self.sound_paddle)

        # Brick collisions
        for brick in self.bricks:
            if brick.alive and self._resolve_collision(brick.rect()):
                brick.alive = False
                self.score += 1
                self._play_sound(self.sound_brick)
                break

        if self.ball.y - self.ball.radius > self.height:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
                self.result = "lose"
                self._play_sound(self.sound_lose)
            else:
                self._reset_ball()

        if all(not b.alive for b in self.bricks):
            self.game_over = True
            self.result = "win"
            self._play_sound(self.sound_win)

    def _reset_ball(self):
        self.ball.x, self.ball.y = self.width // 2, self.height - 50
        self.ball.vx, self.ball.vy = self.base_speed, -self.base_speed

    def render(self, screen):
        screen.fill(BG)

        pygame.draw.rect(screen, WHITE, self.paddle.rect())
        pygame.draw.circle(screen, WHITE, (int(self.ball.x), int(self.ball.y)), self.ball.radius)

        for i, brick in enumerate(self.bricks):
            if brick.alive:
                row = i // self.cols
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                pygame.draw.rect(screen, color, brick.rect())

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(lives_text, (self.width - 130, 10))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((10, 10, 20, 225))
            screen.blit(overlay, (0, 0))

            title_text = "YOU WIN!" if self.result == "win" else "GAME OVER"
            title_color = (80, 220, 100) if self.result == "win" else (240, 70, 70)

            title_surf = self.title_font.render(title_text, True, title_color)
            title_rect = title_surf.get_rect(center=(self.width // 2, 130))
            screen.blit(title_surf, title_rect)

            score_surf = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = score_surf.get_rect(center=(self.width // 2, 185))
            screen.blit(score_surf, score_rect)

            prompt_surf = self.sub_font.render("Select Difficulty to Play Again:", True, (255, 215, 0))
            prompt_rect = prompt_surf.get_rect(center=(self.width // 2, 250))
            screen.blit(prompt_surf, prompt_rect)

            options = [
                ("[1] Easy    - Slower Ball & Larger Paddle", (140, 220, 140)),
                ("[2] Medium  - Normal Speed & Paddle", (180, 200, 240)),
                ("[3] Hard    - Faster Ball & Smaller Paddle", (240, 160, 140)),
                ("[Q] / [ESC] Exit Game", (180, 180, 190)),
            ]

            start_y = 295
            line_spacing = 38
            for i, (text, color) in enumerate(options):
                opt_surf = self.option_font.render(text, True, color)
                opt_rect = opt_surf.get_rect(center=(self.width // 2, start_y + i * line_spacing))
                screen.blit(opt_surf, opt_rect)