import tkinter as tk
import random

class DinoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Dino Game")
        
        self.canvas = tk.Canvas(root, width=800, height=400, bg="lightblue")
        self.canvas.pack()
        
        self.dino = self.canvas.create_rectangle(50, 350, 100, 400, fill="green")
        self.obstacles = []
        self.score = 0
        
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack()
        
        self.is_jumping = False
        self.jump_speed = 0
        self.gravity = 1
        self.jump_strength = -15
        
        self.game_over = False
        
        self.root.bind("<space>", self.jump)
        
        self.create_obstacle()
        self.move_obstacles()
        self.game_loop()
    
    def jump(self, event):
        if not self.is_jumping and not self.game_over:
            self.is_jumping = True
            self.jump_speed = self.jump_strength
    
    def create_obstacle(self):
        obstacle = self.canvas.create_rectangle(800, 350, 810, 400, fill="red")
        self.obstacles.append(obstacle)
        self.root.after(random.randint(2000, 4000), self.create_obstacle)
    
    def move_obstacles(self):
        if not self.game_over:
            for obstacle in self.obstacles:
                self.canvas.move(obstacle, -10, 0)
                if self.canvas.coords(obstacle)[2] < 0:
                    self.canvas.delete(obstacle)
                    self.obstacles.remove(obstacle)
                    self.score += 1
                    self.update_score()
            
            self.root.after(50, self.move_obstacles)
    
    def game_loop(self):
        if not self.game_over:
            self.apply_gravity()
            self.check_collisions()
            self.root.after(20, self.game_loop)
    
    def apply_gravity(self):
        if self.is_jumping or self.canvas.coords(self.dino)[3] < 400:
            self.canvas.move(self.dino, 0, self.jump_speed)
            self.jump_speed += self.gravity
        
        if self.canvas.coords(self.dino)[3] >= 400:
            self.canvas.coords(self.dino, 50, 350, 100, 400)
            self.is_jumping = False
            self.jump_speed = 0
    
    def check_collisions(self):
        if not self.game_over:
            dino_coords = self.canvas.coords(self.dino)
            for obstacle in self.obstacles:
                if self.check_overlap(dino_coords, self.canvas.coords(obstacle)):
                    self.end_game()
                    break
    
    def check_overlap(self, dino_coords, obstacle_coords):
        return not (dino_coords[2] < obstacle_coords[0] or
                    dino_coords[0] > obstacle_coords[2] or
                    dino_coords[3] < obstacle_coords[1] or
                    dino_coords[1] > obstacle_coords[3])
    
    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
    
    def end_game(self):
        self.game_over = True
        self.canvas.create_text(400, 200, text="Game Over", font=("Arial", 30), fill="black")
        self.root.after(2000, self.root.destroy)

# Create the main window
root = tk.Tk()
game = DinoGame(root)

# Run the application
root.mainloop()