import tkinter as tk
import random

window = tk.Tk()
window.title("Snake Game")
window.geometry("400x400")

# Game variables
snake_length = 10  # initial length of the snake
food_x = random.randint(0, 39) * 10  # x-coordinate of the food
food_y = random.randint(0, 39) * 10  # y-coordinate of the food
snake_body = [(200, 200)]  # list to store the snake body with initial position
direction = "right"  # direction the snake is moving
score = 0  # score of the player
game_over = False
game_running = False

# Game canvas
canvas = tk.Canvas(window, width=400, height=400, bg="black")
canvas.pack()

# Game objects
def draw_objects():
    # Food
    food_rect = canvas.create_rectangle(food_x, food_y, food_x + 10, food_y + 10, fill="#bd93f9")

    # Snake body
    for i in range(len(snake_body) - 1):
        x, y = snake_body[i]
        body_rect = canvas.create_rectangle(x, y, x + 10, y + 10, fill="#ffffff")

    # Snake head
    x, y = snake_body[-1]
    head_oval = canvas.create_oval(x, y, x + 10, y + 10, fill="#ff0000")

    # "Game Over" message if the game is over
    if game_over:
        canvas.create_text(200, 200, text=f"Game Over!\nYour final score: {score}\nPress Enter to Start", fill="#bd93f9", font=("Helvetica", 20))

# User input and move the snake
def on_key_press(event):
    global direction, game_running, game_over
    if game_over:
        if event.keysym == "Return":
            restart_game()
    else:
        if event.keysym == "Return" and not game_running:
            game_running = True
            game_loop()
        elif event.keysym == "Right":
            direction = "right"
        elif event.keysym == "Left":
            direction = "left"
        elif event.keysym == "Up":
            direction = "up"
        elif event.keysym == "Down":
            direction = "down"

# Update the game state
def update_game():
    global snake_body, food_x, food_y, score, game_over
    if not game_running:
        return False

    # Move the snake
    if direction == "right":
        new_head = (snake_body[-1][0] + 10, snake_body[-1][1])
    elif direction == "left":
        new_head = (snake_body[-1][0] - 10, snake_body[-1][1])
    elif direction == "down":
        new_head = (snake_body[-1][0], snake_body[-1][1] + 10)
    else:
        new_head = (snake_body[-1][0], snake_body[-1][1] - 10)

    snake_body.append(new_head)

    # Check for collision with walls
    if any([x < 0 or x >= 400 or y < 0 or y >= 400 for x, y in snake_body]):
        game_over = True
        return False

    # Check for collision with itself
    if new_head in snake_body[:-1]:
        game_over = True
        return False

    # Check for food collision
    if new_head == (food_x, food_y):
        score += 1
        food_x = random.randint(0, 39) * 10
        food_y = random.randint(0, 39) * 10
    else:
        # If no food collision, remove the last segment of the snake to maintain its length
        snake_body.pop(0)

    return True

# Step 7: Main game loop
window.bind("<KeyPress>", on_key_press)  # Bind key presses to the on_key_press function

def game_loop():
    global game_running
    if game_running:
        canvas.delete(tk.ALL)  # Clear the canvas before drawing
        draw_objects()
        if update_game():
            window.after(100, game_loop)  # Call game_loop() again after 100 milliseconds
        else:
            game_running = False
            canvas.delete(tk.ALL)  # Clear the canvas before drawing
            draw_objects()  # Draw the "Game Over" screen after the game ends

    
def restart_game():
    global snake_body, food_x, food_y, direction, score, game_over, game_running
    game_running = False
    snake_body = [(200, 200)]
    food_x = random.randint(0, 39) * 10
    food_y = random.randint(0, 39) * 10
    direction = "right"
    score = 0
    game_over = False
    canvas.delete(tk.ALL)  # Clear the canvas before drawing
    

# Start the game
canvas.create_text(200, 200, text="Press Enter to Start", fill="white", font=("Helvetica", 20))

window.mainloop()
