import tkinter as tk
import time

class Point: 
    def __init__(self, x, y): 
        self.x = x 
        self.y = y 

# Find the leftmost point
def Left_index(points): 
    start = 0
    for i in range(1, len(points)):
        if points[i].y < points[start].y or (points[i].y == points[start].y and points[i].x < points[start].x):
            start = i
    return start

# Check orientation of ordered triplet
def orientation(p, q, r): 
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y) 
    if val == 0: 
        return 0
    elif val > 0: 
        return 1
    else: 
        return 2

# Jarvis March algorithm for convex hull
def convexHull(points, n): 
    if n < 3: 
        return
    l = Left_index(points) 
    hull = [] 
    p = l 
    q = 0
    while(True): 
        hull.append(p) 
        q = (p + 1) % n 
        for i in range(n): 
            if(orientation(points[p], points[i], points[q]) == 2): 
                q = i 
        p = q 
        if(p == l): 
            break
    return [points[i] for i in hull]

# Class to draw points and convex hull
class Drawing:
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull - Jarvis March")
        self.start_time = None
        self.end_time = None

        # Canvas for drawing points
        self.canvas = tk.Canvas(self.root, width=500, height=500,bg = "black")
        self.canvas.pack()

        # Canvas for displaying execution time
        self.canvas_execution = tk.Canvas(self.root, width=500, height=50)
        self.canvas_execution.pack()
        self.execution_label = self.canvas_execution.create_text(250, 25, text="", font=("Arial", 12))

        self.points = []

        self.canvas.bind("<Button-1>", self.add_point)

        self.draw_button = tk.Button(self.root, text="Draw Convex Hull", command=self.draw_convex_hull)
        self.draw_button.pack()

    # Add point on mouse click
    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append(Point(x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white")  
    
    # Close the window and display execution time
    def close_window(self):
        self.end_time = time.time()  
        execution_time = self.end_time - self.start_time
        complexity = "O(nh)"
        sapce_complexity = "O (n+h)" # n = Total no. of points ,h=Total no. of points lie on the hull
        self.draw_button.config(state=tk.DISABLED)
        self.canvas_execution.itemconfig(self.execution_label, text=f"Execution time: {execution_time:.2f} seconds\nTime Complexity: {complexity} , Space Complexity: {sapce_complexity}\n")
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy)
        self.quit_button.pack()

    # Draw the convex hull
    def draw_convex_hull(self):
        self.start_time = time.time()
        n = len(self.points)
        if n < 3:
            message = "At least 3 points are required to draw the convex hull."
            self.canvas_execution.itemconfig(self.execution_label, text=message)
            return

        convex_points = convexHull(self.points, n)
        if convex_points:
            hull_coords = [(point.x, point.y) for point in convex_points]
            for i in range(len(hull_coords)):
                start_x, start_y = hull_coords[i]
                end_x, end_y = hull_coords[(i + 1) % len(hull_coords)]
                self.canvas.create_line(start_x, start_y, start_x, start_y, fill="red")
                self.root.after(500 * (i + 1), self.draw_line, start_x, start_y, end_x, end_y)
            self.root.after(500 * (len(hull_coords) + 1), self.close_window)
       
    # Draw lines between hull points
    def draw_line(self, start_x, start_y, end_x, end_y):
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="red")

root = tk.Tk()
app = Drawing(root)
root.mainloop()
