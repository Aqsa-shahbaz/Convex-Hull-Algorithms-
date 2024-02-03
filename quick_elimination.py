import tkinter as tk
import time 

# Function to compute the convex hull using Quickhull algorithm
def quickhull_convex_hull(points):
    # Helper function to find the hull
    def find_hull(p1, p2, points):
        if not points:
            return []

        max_distance = -1
        farthest_point = None

        # Find the farthest point from the line p1p2
        for point in points:
            distance = (p2[0] - p1[0]) * (point[1] - p1[1]) - (p2[1] - p1[1]) * (point[0] - p1[0])
            if distance > max_distance:
                max_distance = distance
                farthest_point = point

        if not farthest_point:
            return []

        convex_hull = []

        points.remove(farthest_point)

        # Determine points on the correct side of p1p2
        for point in points:
            if (p2[0] - p1[0]) * (point[1] - p1[1]) - (p2[1] - p1[1]) * (point[0] - p1[0]) > 0:
                convex_hull.append(point)

        # Recursively find the left and right convex hull
        convex_hull_left = find_hull(p1, farthest_point, convex_hull)
        convex_hull_right = find_hull(farthest_point, p2, convex_hull)

        return [p1] + convex_hull_left + [farthest_point] + convex_hull_right + [p2]

    if len(points) < 3:
        return points

    # Find the leftmost and rightmost points
    min_x = min(points, key=lambda p: p[0])
    max_x = max(points, key=lambda p: p[0])

    # Compute the convex hull
    convex_hull = find_hull(min_x, max_x, points)
    convex_hull += find_hull(max_x, min_x, points)

    return convex_hull

# Class for drawing points and convex hull
class Drawing:
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull - Quickhull")
        self.start_time = None
        self.end_time = None
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg = "Black")
        self.canvas.pack()
        self.canvas_execution = tk.Canvas(self.root, width=500, height=50)
        self.canvas_execution.pack()

        self.execution_label = self.canvas_execution.create_text(250, 25, text="", font=("Arial", 12))

        self.points = []

        self.canvas.bind("<Button-1>", self.add_point)
        self.draw_button = tk.Button(self.root, text="Draw Convex Hull", command=self.draw_convex_hull)
        self.draw_button.pack()

    # Close the window and display execution time
    def close_window(self):
        self.end_time = time.time()  # Record end time when drawing is completed
        execution_time = self.end_time - self.start_time  # Calculate execution time
        self.draw_button.config(state=tk.DISABLED)
        self.canvas_execution.itemconfig(self.execution_label, text=f"Execution time: {execution_time:.2f} seconds\nTime Complexity: O(n^2), Space Complexity: O(n)")

        # Add Quit button to close canvas
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy)
        self.quit_button.pack()

    # Add point on mouse click
    def add_point(self, event):
        x, y = event.x, event.y
        new_point = (x, y)
        self.points.append(new_point)
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white")
    
    # Draw the convex hull
    def draw_convex_hull(self):
        self.start_time = time.time()
        n = len(self.points)

        if n < 3:
            message = "At least 3 points are required to draw the convex hull."
            self.canvas_execution.itemconfig(self.execution_label, text=message)
            return

        convex_hull = quickhull_convex_hull(self.points)
        
        if convex_hull:
            hull_coords = list(convex_hull)
            hull_coords.append(hull_coords[0])  # Close the convex hull

            for i in range(len(hull_coords) - 1):
                start_x, start_y = hull_coords[i]
                end_x, end_y = hull_coords[i + 1]
                self.canvas.create_line(start_x, start_y, start_x, start_y, fill="red")
                self.root.after(500 * (i + 1), self.draw_line, start_x, start_y, end_x, end_y)
            self.root.after(500 * (len(hull_coords) + 1), self.close_window)

    # Draw lines between hull points
    def draw_line(self, start_x, start_y, end_x, end_y):
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="red")

root = tk.Tk()
app = Drawing(root)
root.mainloop()
