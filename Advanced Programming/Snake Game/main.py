#Importing modules
import tkinter as tk
import random

class SnakeGame: # Game class
    def __init__(self):

        # Making GUI
        self.root = tk.Tk()
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="black")
        self.canvas.pack()
        self.score = 0
        self.label = tk.Label(self.root, text="Points:{}".format(self.score),font=('consolas', 20))
        self.label.pack()

        # Initialising Dimensions of Game
        self.WIDTH = 400
        self.HEIGHT = 400
        self.SPEED = 300
        self.SPACE_SIZE = 20

        # Snake's and Food's coordinates
        self.snake_body = [(0, 0)]
        self.direction = "right"
        self.food = self.spawn_food()
        self.root.bind("<Key>", self.on_key_press)


        self.display()


    # Controlling area
    def display(self):
        self.move_snake()
        if self.check_collision():
            self.game_over()
        else:
            self.canvas.after(self.SPEED, self.display)

    # Making movement
    def move_snake(self):
        head = self.snake_body[0]
        x, y = head

        if self.direction == "up":
            y -= self.SPACE_SIZE
        elif self.direction == "down":
            y += self.SPACE_SIZE
        elif self.direction == "left":
            x -= self.SPACE_SIZE
        elif self.direction == "right":
            x += self.SPACE_SIZE

        self.snake_body.insert(0, (x, y))
        self.canvas.delete("snake")

        for parts in self.snake_body:
            x, y = parts
            self.canvas.create_rectangle(
                x, y, x + 20, y + 20, fill="white", tag="snake"
            )

        if head == self.food:
            self.score += 1
            self.label.config(text="Score: {}".format(self.score))
            self.canvas.delete("food")  # Delete the food
            self.food = self.spawn_food()
        else:
            self.snake_body.pop()


    # Creating food at random coordinate
    def spawn_food(self):
        x = random.randint(0,(self.WIDTH / self.SPACE_SIZE)-1) * self.SPACE_SIZE
        y = random.randint(0,(self.HEIGHT / self.SPACE_SIZE)-1) * self.SPACE_SIZE
        self.canvas.create_oval(x, y, x + self.SPACE_SIZE, y + self.SPACE_SIZE, fill="#FFFFFF", tag="food")
        return (x, y)

    # Checking Snake is in the canvas 
    def check_collision(self):
        head = self.snake_body[0]
        x, y = self.snake_body[0]

        if (
            x < 0
            or x >= self.HEIGHT
            or y < 0
            or y >= self.WIDTH
            or head in self.snake_body[1:]
        ):
            return True

        return False

    # End the game
    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            200, 200, text="Game Over", fill="white", font=("Arial", 24)
        )

    # Getting directions
    def on_key_press(self, event):
        key = event.keysym
        if (
            (key == "Up" and self.direction != "down")
            or (key == "Down" and self.direction != "up")
            or (key == "Left" and self.direction != "right")
            or (key == "Right" and self.direction != "left")
        ):
            self.direction = key.lower()


if __name__ == "__main__":
    game = SnakeGame()
    game.root.mainloop()
