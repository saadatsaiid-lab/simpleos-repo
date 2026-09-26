import tkinter as tk
import random
import time


class SpaceDefender:

    NAME = "Saasat Space Defender"
    ICON = "🚀"
    APP_ID = "space_defender"

    def __init__(self, desktop):
        self.desktop = desktop
        self.running = False
        self.score = 0
        self.lives = 3
        self.level = 1
        self.last_time = time.time()

    def launch(self):
        # بررسی اینکه پنجره والد (desktop) وجود دارد
        if not self.desktop:
            raise ValueError("پنجره والد (desktop) به درستی مقداردهی نشده است.")

        # ✅ اصلاح اصلی: استفاده مستقیم از self.desktop به عنوان پنجره والد
        self.window = tk.Toplevel(self.desktop)

        self.window.title("🚀 Saasat Space Defender")
        self.window.geometry("800x600")
        self.window.resizable(False, False)

        self.canvas = tk.Canvas(
            self.window,
            width=800,
            height=600,
            bg="#050816",
            highlightthickness=0
        )
        self.canvas.pack()

        self.score_text = self.canvas.create_text(
            20, 20,
            anchor="nw",
            text="Score: 0",
            fill="white",
            font=("Segoe UI", 16, "bold")
        )

        self.lives_text = self.canvas.create_text(
            650, 20,
            anchor="nw",
            text="Lives: 3",
            fill="white",
            font=("Segoe UI", 16, "bold")
        )

        self.player_x = 400
        self.player_y = 530

        self.player = self.canvas.create_polygon(
            self.player_x, self.player_y - 25,
            self.player_x - 20, self.player_y + 20,
            self.player_x, self.player_y + 10,
            self.player_x + 20, self.player_y + 20,
            fill="#38bdf8",
            outline="white"
        )

        self.bullets = []
        self.enemies = []
        self.stars = []
        self.keys = set()

        for _ in range(70):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            star = self.canvas.create_oval(
                x, y, x + 2, y + 2,
                fill="white",
                outline=""
            )
            self.stars.append(star)

        self.window.bind("<KeyPress>", self.key_down)
        self.window.bind("<KeyRelease>", self.key_up)
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.running = True

        self.spawn_enemy()
        self.game_loop()

        self.window.focus_force()

    def key_down(self, event):
        self.keys.add(event.keysym.lower())
        if event.keysym.lower() == "space":
            self.shoot()

    def key_up(self, event):
        self.keys.discard(event.keysym.lower())

    def shoot(self):
        if not self.running:
            return

        x = self.player_x
        bullet = self.canvas.create_rectangle(
            x - 3, self.player_y - 30,
            x + 3, self.player_y - 10,
            fill="#facc15",
            outline=""
        )
        self.bullets.append(bullet)

    def spawn_enemy(self):
        if not self.running:
            return

        x = random.randint(30, 770)
        size = random.randint(15, 25)

        enemy = self.canvas.create_oval(
            x - size, -size,
            x + size, size,
            fill="#ef4444",
            outline="#fca5a5",
            width=2
        )
        self.enemies.append(enemy)

        delay = max(250, 900 - self.level * 60)
        self.window.after(delay, self.spawn_enemy)

    def move_player(self):
        speed = 8

        if "left" in self.keys or "a" in self.keys:
            self.player_x -= speed
        if "right" in self.keys or "d" in self.keys:
            self.player_x += speed

        self.player_x = max(25, min(775, self.player_x))

        self.canvas.coords(
            self.player,
            self.player_x, self.player_y - 25,
            self.player_x - 20, self.player_y + 20,
            self.player_x, self.player_y + 10,
            self.player_x + 20, self.player_y + 20
        )

    def move_bullets(self):
        speed = 12

        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -speed)
            coords = self.canvas.coords(bullet)

            if not coords:
                self.bullets.remove(bullet)
                continue

            if coords[3] < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)

    def move_enemies(self):
        speed = 2.5 + self.level * 0.4

        for enemy in self.enemies[:]:
            self.canvas.move(enemy, 0, speed)
            coords = self.canvas.coords(enemy)

            if not coords:
                continue

            if coords[1] > 600:
                self.canvas.delete(enemy)
                self.enemies.remove(enemy)
                self.lose_life()

    def collision(self):
        for bullet in self.bullets[:]:
            bullet_coords = self.canvas.coords(bullet)
            if not bullet_coords:
                continue

            bx = (bullet_coords[0] + bullet_coords[2]) / 2
            by = (bullet_coords[1] + bullet_coords[3]) / 2

            for enemy in self.enemies[:]:
                enemy_coords = self.canvas.coords(enemy)
                if not enemy_coords:
                    continue

                ex = (enemy_coords[0] + enemy_coords[2]) / 2
                ey = (enemy_coords[1] + enemy_coords[3]) / 2

                distance = ((bx - ex) ** 2 + (by - ey) ** 2) ** 0.5
                enemy_size = (enemy_coords[2] - enemy_coords[0]) / 2

                if distance < enemy_size + 5:
                    self.canvas.delete(bullet)
                    self.canvas.delete(enemy)

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)

                    self.score += 10
                    self.level = 1 + self.score // 100
                    self.update_hud()
                    break

    def lose_life(self):
        self.lives -= 1
        self.update_hud()
        if self.lives <= 0:
            self.game_over()

    def update_hud(self):
        self.canvas.itemconfig(
            self.score_text,
            text=f"Score: {self.score}"
        )
        self.canvas.itemconfig(
            self.lives_text,
            text=f"Lives: {self.lives}"
        )

    def game_loop(self):
        if not self.running:
            return

        self.move_player()
        self.move_bullets()
        self.move_enemies()
        self.collision()

        self.window.after(16, self.game_loop)

    def game_over(self):
        self.running = False

        self.canvas.create_rectangle(
            180, 210, 620, 390,
            fill="#020617",
            outline="#ef4444",
            width=3
        )
        self.canvas.create_text(
            400, 260,
            text="GAME OVER",
            fill="#ef4444",
            font=("Segoe UI", 36, "bold")
        )
        self.canvas.create_text(
            400, 315,
            text=f"Score: {self.score}",
            fill="white",
            font=("Segoe UI", 20)
        )
        self.canvas.create_text(
            400, 355,
            text="Close the window to exit",
            fill="#94a3b8",
            font=("Segoe UI", 12)
        )

    def close(self):
        self.running = False
        try:
            self.window.destroy()
        except Exception:
            pass
