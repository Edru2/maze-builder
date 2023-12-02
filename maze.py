from tkinter import Tk, BOTH, Canvas
import time
import random

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__canvas = Canvas(self.__root, bg ="white", width = width, height = height)
        self.__canvas.pack(fill="both", expand=True)
        self.__root.title = "Hello World"
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.geometry(f"{width}x{height}")

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


    def wait_for_close(self):
        self.__running = True
        while(self.__running):
            self.redraw()
    
    def close(self):
        self.__running = False

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, canvas, fill_color):
        canvas.create_line(
                self.start.x,self.start.y,self.end.x,self.end.y, fill=fill_color, width=2
                )
        canvas.pack(fill="both", expand=True)

class Cell():
    def __init__(self, _win=None):
        self.has_left_wall = True 
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self.visited = False
        self._win = _win

    def draw(self, x1, y1, x2, y2):
        if self.has_left_wall:
            self._win.draw_line(Line(Point(x1,y1),Point(x1,y2)), "black")
        else:
            self._win.draw_line(Line(Point(x1,y1),Point(x1,y2)), "white")

        if self.has_right_wall:
            self._win.draw_line(Line(Point(x2,y1),Point(x2,y2)), "black")
        else:
            self._win.draw_line(Line(Point(x2,y1),Point(x2,y2)), "white")

        if self.has_top_wall:
            self._win.draw_line(Line(Point(x1,y1),Point(x2,y1)), "black")
        else:
            self._win.draw_line(Line(Point(x1,y1),Point(x2,y1)), "white")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(x1,y2),Point(x2,y2)), "black")
        else:
            self._win.draw_line(Line(Point(x1,y2),Point(x2,y2)), "white")

        self._x1,self._x2,self._y1,self._y2 = x1, x2, y1, y2

    def draw_move(self, to_cell, undo=False):
        lineColor = undo == True and "grey" or "red"
        mid_x = (self._x1 + self._x2) //2
        mid_y = (self._y1 + self._y2) //2
        mid_x1 = (to_cell._x1 + to_cell._x2) //2
        mid_y1 = (to_cell._y1 + to_cell._y2) //2

        line = Line(Point(mid_x, mid_y), Point(mid_x1, mid_y1))
        self._win.draw_line(line, lineColor)


class Maze():
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win = None,
            seed = None,
        ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = seed
        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                cell = Cell(self.win)
                row.append(cell)
            self._cells.append(row)
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self.win is None:
            return
        cell = self._cells[i][j]
        pos_x = (self.x1) + j * (self.cell_size_x)
        pos_y = (self.y1) + i * (self.cell_size_y)
        pos_x2 = (self.x1) + j * (self.cell_size_x) + (self.cell_size_x)
        pos_y2 = (self.y1) + i * (self.cell_size_y) + (self.cell_size_y)


        cell.draw(pos_x, pos_y, pos_x2, pos_y2)
        self._animate()

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        maze_entrance = self._cells[0][0]
        maze_exit = self._cells[len(self._cells)-1][len(self._cells[0])-1]
        maze_entrance.has_left_wall = False
        maze_entrance.has_right_wall = False
        maze_exit.has_left_wall = False
        maze_exit.has_right_wall = False
        self._draw_cell(0,0)
        self._draw_cell(len(self._cells)-1,len(self._cells[0])-1)

    def _break_walls_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True
        while True: 
            possible_directions = []
            if i > 0:
                left_cell = self._cells[i-1][j]
                if not left_cell.visited:
                    possible_directions.append(left_cell)
            if j > 0:
                top_cell = self._cells[i][j-1]
                if not top_cell.visited:
                    possible_directions.append(top_cell)
            if i < len(self._cells)-1:
                right_cell = self._cells[i+1][j]
                if not right_cell.visited:
                    possible_directions.append(right_cell)
            if j < len(self._cells[0])-1:
                bottom_cell = self._cells[i][j+1]
                if not bottom_cell.visited:
                    possible_directions.append(bottom_cell)
            if len(possible_directions) <= 0:
                self._draw_cell(i, j)
                return
            random_room = random.choice(possible_directions)
            k,l = i,j
            if current._x1 == random_room._x2:
                current.has_left_wall = False
                random_room.has_right_wall = False
                l-=1
            if current._x2 == random_room._x1:
                current.has_right_wall = False
                random_room.has_left_wall = False
                l+=1
            if current._y1 == random_room._y2:
                current.has_top_wall = False
                random_room.has_bottom_wall = False
                k-=1
            if current._y2 == random_room._y1:
                current.has_bottom_wall = False
                random_room.has_top_wall = False       
                k+=1
            self._draw_cell(i,j)
            self._draw_cell(k,l)
            self._break_walls_r(k,l)

    def _reset_cells_visited(self):
        for cell_list in self._cells:
            for cell in cell_list:
                cell.visited = False

    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self, i, j):
        self._animate()
        current = self._cells[i][j]
        current.visited = True
        if current == self._cells[len(self._cells)-1][len(self._cells[0])-1]:
            return True
        while True:
            if i > 0:
                top_cell = self._cells[i-1][j]
                if not top_cell.visited and not top_cell.has_bottom_wall:
                    current.draw_move(top_cell)
                    if self._solve_r(i-1,j):
                        return True
                    current.draw_move(top_cell, True)
            if j > 0:
                left_cell = self._cells[i][j-1]
                if not left_cell.visited and not left_cell.has_right_wall:
                    current.draw_move(left_cell)
                    if self._solve_r(i,j-1):
                        return True
                    current.draw_move(left_cell, True)
            if i < len(self._cells)-1:
                bottom_cell = self._cells[i+1][j]
                if not bottom_cell.visited and not bottom_cell.has_top_wall:
                    current.draw_move(bottom_cell)
                    if self._solve_r(i+1,j):
                        return True
                    current.draw_move(bottom_cell, True)
            if j < len(self._cells[0])-1:
                right_cell = self._cells[i][j+1]
                if not right_cell.visited and not right_cell.has_left_wall:
                    current.draw_move(right_cell)
                    if self._solve_r(i, j+1):
                        return True
                    current.draw_move(right_cell, True)
            return False





def main():
    win = Window(800, 700)
    maze = Maze(10,10,12,10,50,50,win)
    maze._break_entrance_and_exit()
    maze._break_walls_r(0,0)
    maze._reset_cells_visited()
    maze.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()
