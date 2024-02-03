import tkinter as tk 
import time 
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
def orientation(p, q, r): 
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y) 
    if val == 0: 
        return 0
    elif val > 0: 
        return 1
    else: 
        return 2
def convex_hull(points):
    # Sort the points by x-coordinate
    points.sort(key=lambda p: (p.x, p.y))

    # Initialize upper and lower hulls
    upper = [points[0], points[1]]
    lower = [points[0], points[1]]

    # Compute the upper hull
    for i in range(2, len(points)):
        upper.append(points[i])
        while len(upper) > 2 and orientation(upper[-3], upper[-2], upper[-1]) == 1:
            upper.pop(-2)

    # Compute the lower hull
    for i in range(2, len(points)):
        lower.append(points[i])
        while len(lower) > 2 and orientation(lower[-3], lower[-2], lower[-1]) == 2:
            lower.pop(-2)

    # Concatenate upper and lower hulls to form the convex hull
    convex_hull = upper + lower[1:-1]
    return convex_hull


class Drawing:
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull - Incremental Algorithm")

        self.points = []
        self.convex_hull = []
        self.start_time = None
        self.end_time = None
        self.canvas = tk.Canvas(self.root, width=500, height=500,bg = "Black")
        self.canvas.pack()
        self.canvas_execution = tk.Canvas(self.root, width=500, height=50)
        self.canvas_execution.pack()
        self.execution_label = self.canvas_execution.create_text(250, 25, text="", font=("Arial", 12))


        self.canvas.bind("<Button-1>", self.add_points)

        self.draw_button = tk.Button(self.root, text="Draw Convex Hull", command=self.draw_convex_hull)
        self.draw_button.pack()

    def add_points(self, event):
        x, y = event.x, event.y
        self.points.append(Point(x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white")

    def draw_convex_hull(self):
        self.start_time = time.time()
        self.convex_hull = convex_hull(self.points)
        points = [(point.x, point.y) for point in self.convex_hull]

        self.canvas.delete("convex_hull")  # Clear previous hull if any

        hull = self.convex_hull  # Make a copy for manipulation
        n = len(hull)

        # If there are less than 3 points, display a message on the canvas
        if n < 3:
            message = "Convex hull requires at least 3 points."
            self.canvas_execution.itemconfig(self.execution_label, text=message)
            return

        # Find the leftmost point to start the convex hull
        leftmost = min(hull, key=lambda p: p.x)

        p = hull.index(leftmost)
        hull_points = []

        while True:
            hull_points.append(p)
            q = (p + 1) % n
            for i in range(n):
                if orientation(hull[p], hull[i], hull[q]) == 2:
                    q = i
            p = q
            if p == 0:
                break

        for i in range(len(hull_points)):
            j = (i + 1) % len(hull_points)
            x0, y0 = hull[hull_points[i]].x, hull[hull_points[i]].y
            x1, y1 = hull[hull_points[j]].x, hull[hull_points[j]].y
            self.canvas.create_line(x0, y0, x0, y0, fill="red")
            self.root.after(500 * (i + 1), self.draw_line, x0, y0, x1, y1)
            
        self.root.after(500 * (len(hull_points) + 1), self.close_window)

    def draw_line(self, start_x, start_y, end_x, end_y):
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="red")

    def close_window(self):
        self.end_time = time.time()  # Record end time when drawing is completed
        execution_time = self.end_time - self.start_time  # Calculate execution time
        self.draw_button.config(state=tk.DISABLED)
        self.canvas_execution.itemconfig(self.execution_label, text=f"Execution time: {execution_time:.2f} seconds\nTime Complexity: O(nlogn), Space Complexity: O(n)")

        # Add Quit button to close canvas
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy)
        self.quit_button.pack()
    

root = tk.Tk()
app = Drawing(root)
root.mainloop()
