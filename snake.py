import tkinter as tk
import random

CELL = 20
COLS, ROWS = 30, 24
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
SPEED_MS = 200

class SnakeGame:
    def __init__(self, root):
        self.root = root
        root.title("贪吃蛇")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#111827", highlightthickness=0)
        self.canvas.pack()
        self.status = tk.Label(root, text="方向键 / WASD 移动　空格暂停　R 重新开始", font=("Microsoft YaHei UI", 10))
        self.status.pack(fill="x")
        root.bind("<KeyPress>", self.on_key)
        self.restart()

    def restart(self):
        self.snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2 - 2, ROWS // 2)]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.score = 0
        self.paused = False
        self.game_over = False
        self.spawn_food()
        self.draw()
        self.tick()

    def spawn_food(self):
        choices = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in self.snake]
        self.food = random.choice(choices) if choices else None

    def on_key(self, event):
        key = event.keysym.lower()
        if key == "r":
            self.restart()
            return
        if key == "space" and not self.game_over:
            self.paused = not self.paused
            self.draw()
            return
        directions = {"up": (0, -1), "w": (0, -1), "down": (0, 1), "s": (0, 1),
                      "left": (-1, 0), "a": (-1, 0), "right": (1, 0), "d": (1, 0)}
        new = directions.get(key)
        if new and new != (-self.direction[0], -self.direction[1]):
            self.next_direction = new

    def tick(self):
        if not self.game_over and not self.paused:
            self.direction = self.next_direction
            dx, dy = self.direction
            head = (self.snake[0][0] + dx, self.snake[0][1] + dy)
            eating = head == self.food
            body = self.snake if eating else self.snake[:-1]
            if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS) or head in body:
                self.game_over = True
            else:
                self.snake.insert(0, head)
                if eating:
                    self.score += 10
                    self.spawn_food()
                    if self.food is None:
                        self.game_over = True
                else:
                    self.snake.pop()
            self.draw()
        self.root.after(SPEED_MS, self.tick)

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_text(10, 10, anchor="nw", text=f"得分：{self.score}", fill="white", font=("Arial", 14, "bold"))
        if self.food:
            x, y = self.food
            self.canvas.create_oval(x*CELL+3, y*CELL+3, (x+1)*CELL-3, (y+1)*CELL-3, fill="#ef4444", outline="")
        for i, (x, y) in enumerate(self.snake):
            pad = 2
            self.canvas.create_rectangle(x*CELL+pad, y*CELL+pad, (x+1)*CELL-pad, (y+1)*CELL-pad,
                                         fill="#34d399" if i == 0 else "#10b981", outline="")
        if self.paused or self.game_over:
            msg = "游戏结束！按 R 重新开始" if self.game_over else "已暂停　按空格继续"
            self.canvas.create_rectangle(45, HEIGHT//2-35, WIDTH-45, HEIGHT//2+35, fill="#000000", outline="")
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text=msg, fill="white", font=("Microsoft YaHei UI", 18, "bold"))

if __name__ == "__main__":
    window = tk.Tk()
    SnakeGame(window)
    window.mainloop()
