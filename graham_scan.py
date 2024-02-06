import tkinter as tk
from math import atan2
import time 

class Point :
    def __init__(self):
        self.x=None
        self.y=None
    
    def set_points (self,x,y):
        self.x=x
        self.y=y

    # Find the leftmost point #y-axis
    def Left_index(self,points):
        start = 0
        for i in range(1, len(points)):
            if points[i].y < points[start].y or (points[i].y == points[start].y and points[i].x < points[start].x):
                start = i
        return start

    # Calculate polar angle
    def polar_angle(self,p0, p):
        return atan2(p.y - p0.y, p.x - p0.x)

    # Get the next point in the stack
    def next_to_top(stack):
        top = stack.pop()
        next_top = stack[-1]
        stack.append(top)
        return next_top
    
    # Determine orientation of three points
    def orientation(self,p, q, r):
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if val == 0:
                return 0  # colinear
        return 1 if val > 0 else 2  # clock or counterclock wise
    
    # graham's scan algorithm for convex hull
    def Convexhull(self, points, n):
        if n < 3:
            return []

        # Find the leftmost point
        p0_index = self.Left_index(points)
        p0 = points[p0_index]

        # Sort points based on polar angle with respect to p0
        points[0], points[p0_index] = points[p0_index], points[0]
        points[1:] = sorted(points[1:], key=lambda a: (self.polar_angle(p0, a), -a.y, a.x))

        stack = [points[0], points[1], points[2]]

        for i in range(3, n):
            while len(stack) > 1 and self.orientation(stack[-2], stack[-1], points[i]) != 2:
                stack.pop()
            stack.append(points[i])

        return stack

class Drawing :
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull - Graham's Scan")
        self.start_time =None
        self.end_time = None

        # Canvas for drawing points
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg= "black")
        self.canvas.pack()

        # Canvas for displaying execution time
        self.canvas_execution = tk.Canvas(self.root, width=500, height=50)
        self.canvas_execution.pack()
        self.execution_label = self.canvas_execution.create_text(250, 25, text="", font=("Arial", 12))

        self.points = []

        self.canvas.bind("<Button-1>", self.add_points)
        self.draw_button = tk.Button(self.root, text="Draw Convex Hull", command=self.draw_convex_hull)
        self.draw_button.pack()

    # Close the window and display execution time
    def close_window(self):
        self.end_time = time.time()  # Record end time when drawing is completed
        execution_time = self.end_time - self.start_time  # Calculate execution time
        self.draw_button.config(state=tk.DISABLED)
        self.canvas_execution.itemconfig(self.execution_label, text=f"Execution time: {execution_time:.2f} seconds\nTime complexity: O(nlogn), Space Complexity: O(n)")

        # Add Quit button to close canvas
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy)
        self.quit_button.pack()

    # Add points on mouse click
    def add_points(self,event):
        x, y = event.x, event.y
        new_point = Point()
        new_point.set_points(x,y)  
        self.points.append(new_point)
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white")

    # Draw the convex hull
    def draw_convex_hull(self):
        self.start_time = time.time()
        point_objects = [point for point in self.points]

        # If less than 3 points are entered, display a message
        if len(point_objects) < 3:
            message = "Convex hull requires at least 3 points."
            self.canvas_execution.itemconfig(self.execution_label, text=message)
            return

        convex_points = Point().Convexhull(point_objects, len(point_objects))
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
