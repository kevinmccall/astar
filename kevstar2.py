from collections import namedtuple
from dataclasses import dataclass

class UntraversablePathException(Exception):
    pass


@dataclass(eq=False)
class Cell:
    x : int
    y : int
    gcost : int = -1
    hcost : int = -1
    fcost : int = -1
    previous = None

    def set_fcost(self, gcost, hcost):
        self.gcost = gcost
        self.hcost = hcost
        self.fcost = gcost + hcost
    
    def get_pos(self):
        return (self.x, self.y)

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Cell) and __o.x == self.x and __o.y == self.y

class Grid:
    def __init__(self, x_size, y_size) -> None:
        self.x_size = x_size
        self.y_size = y_size
        self.unwalkable_cells = set()

    def a_star(self, start_pos, end_pos):
        if start_pos in self.unwalkable_cells or end_pos in self.unwalkable_cells:
            raise UntraversablePathException("Starting cells are unwalkable.")
        
        point_a = Cell(*start_pos)
        point_b = Cell(*end_pos)
        path = []
        to_check = [point_a]
        exhausted = []
        head = point_a
        while head != point_b:
            valid_neighbors = self.get_walkable_neighbors(head)
            for neighbor in valid_neighbors:
                if neighbor in to_check:
                    continue
                if neighbor not in exhausted:
                    gcost = self.get_distance(point_a, neighbor)
                    hcost = self.get_distance(neighbor, point_b)
                    if (neighbor.fcost == -1 or neighbor.fcost > gcost + hcost):
                        neighbor.set_fcost(gcost, hcost)
                        neighbor.previous = head
                    to_check.append(neighbor)
            exhausted.append(head)
            to_check.remove(head)
            if len(to_check) == 0:
                raise UntraversablePathException("No valid path.")
            head = min(to_check, key=lambda x: x.fcost)
        while head != None:
            path.insert(0, head.get_pos())
            head = head.previous
        return path
    
    def get_walkable_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x, y) == (0,0):
                    continue
                neighbor_cell = Cell(cell.x + x, cell.y + y)
                if self.is_cell_valid(neighbor_cell) and self.is_cell_walkable(cell):
                    neighbors.append(neighbor_cell)
        return neighbors
                
    def get_distance(self, cell1, cell2):
        x_diff = abs(cell1.x - cell2.x)
        y_diff = abs(cell1.y - cell2.y)
        # if x_diff > y_diff:
        #     return (x_diff - y_diff) * 10 + y_diff * 14
        # else:
        #     return (y_diff - x_diff) * 10 + y_diff * 14
        
        return abs(x_diff - y_diff) * 10 + min(x_diff, y_diff) * 14

    def is_cell_valid(self, cell : Cell):
        return cell.x >= 0 and cell.x < self.x_size and cell.y >= 0 and cell.y < self.y_size

    def is_cell_walkable(self, cell : Cell):
        return cell.get_pos() not in self.unwalkable_cells
    
    def add_unwalkable_cell(self, cell_pos):
        self.unwalkable_cells.add(cell_pos)
    
    def remove_unwalkable_cell(self, cell_pos):
        try:
            self.unwalkable_cells.remove(cell_pos)
        except KeyError:
            print("tried removing invalid walls")

def main():
    g = Grid(10,10)
    point_a = (0, 0)
    point_b = (8, 3)

    for point in g.a_star(point_a, point_b):
        print(point)

if __name__ == '__main__':
    main()