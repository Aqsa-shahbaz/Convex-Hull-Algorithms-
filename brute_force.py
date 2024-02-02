from typing import List, Tuple
import tkinter as tk
import time 
def orientation(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> float:
        val =  ((p3[1] - p2[1]) * (p2[0] - p1[0])) - ((p2[1] - p1[1]) * (p3[0] - p2[0]))
        return val

# Function to find convex hull using brute force approach
def brute_force(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    n = len(points)
    if n < 3:
        return []

    hull = []
    for i in range(n-1):
        for j in range(i + 1, n):
            valid = True
            left = right = False
            p1 = points[i]
            p2 = points[j]
            for k in range(n):
                if k == i or k == j:
                    continue
                val = orientation(p1,p2,points[k])
                if val > 0:
                    left = True  #counter clockwise 
                elif val < 0 :
                    right = True
                else :
                    if points[k] < p1 or points[k] > p2:
                        valid = False
                        break
            
                if right and left :
                    valid =False 
                    break

            if valid:
                    hull.append(p1)
                    hull.append(p2)

    return hull

class Drawing:
    # Initialize the main application window and canvas
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull - Brute Force")
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="black")
        self.canvas.pack()
        self.start_time = None
        self.end_time = None
        # Canvas for displaying execution time
        self.canvas_execution = tk.Canvas(self.root, width=500, height=50)
        self.canvas_execution.pack()
        self.execution_label = self.canvas_execution.create_text(250, 25, text="", font=("Arial", 12))

        self.points = []
        # Binding mouse click to add points
        self.canvas.bind("<Button-1>", self.add_point)

        self.draw_button = tk.Button(self.root, text="Compute Convex Hull", command=self.draw_convex_hull)
        self.draw_button.pack()

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white")

    def draw_convex_hull(self):
        # Function to draw convex hull based on the points collected
        self.start_time = time.time()
        n = len(self.points)
        if n < 3:
            message = "At least 3 points are required to draw the convex hull."
            self.canvas_execution.itemconfig(self.execution_label, text=message)
            return

        hull_points = brute_force(self.points)
        if hull_points:
            for i in range(0, len(hull_points), 2):
                x1, y1 = hull_points[i]
                x2, y2 = hull_points[i + 1]
                self.canvas.create_line(x1, y1, x2, y2, fill="red")

        self.end_time = time.time()  
        execution_time = self.end_time - self.start_time
        complexity = "O(n^3)"
        space_complexity = "O(nd+1)"  
        self.canvas_execution.itemconfig(
            self.execution_label, 
            text=f"Execution time: {execution_time:.2f} seconds\nTime Complexity: {complexity}, Space Complexity: {space_complexity}\n"
        )
        self.draw_button.config(state=tk.DISABLED)
        self.root.after(500 * (len(hull_points) + 1), self.close_window)
 
#Close the window after 5 seconds 
    def close_window(self):
        self.root.after(5000, self.root.destroy)


root = tk.Tk()
app = Drawing(root)
root.mainloop()
