"""
John Conway's Game of Life
Rules:
    We have a grid consisting of cells. A cell can either be dead or alive.
    - a neighbor to a cell is a cell that is adjacent on the grid
    - a living cell dies if it has less than 2 living neighbors
    - a dead cell with exactly 3 living neighbors will be reborn
    - a living cell with more than 3 living neighbors will die
"""

class Cell:
    pos               = (-1, -1) # position on the grid
    is_alive          = False
    is_alive_next_gen = False

    def __init__(self, x, y):
        self.pos = (x, y)

    def __str__(self):
        return "cell at (" + str(self.pos[0]) + "," + str(self.pos[1]) + ")"

    def isAlive(self):
        return True if self.is_alive else False

    def update(self):
        if self.is_alive_next_gen:
            self.is_alive = True
        else: 
            self.is_alive = False
        self.is_alive_next_gen = False

"""
Draws a square on the screen using the global SCREEN object
"""
def drawCell(cell):
    xPos = cell.pos[0] * 32
    yPos = cell.pos[1] * 32
    color = COLOR_ALIVE if cell.is_alive else COLOR_DEAD
    pygame.draw.rect(SCREEN, color, (xPos, yPos, 30, 30))


"""
Grid is 32 x 32 cells
"""
def initCells(container):
    for colIndex in range(32):
        for rowIndex in range(32):
            container.append(Cell(rowIndex, colIndex))

"""
Update all the cells for the next generation
"""
def updateCells():
    # pass all cells and set flag for next generation
    for cell in cells:
        if willBeAlive(cell, cells):
            cell.is_alive_next_gen = True
        else:
            cell.is_alive_next_gen = False
    # process flag and update the cells
    for cell in cells:
        cell.update() 


def countLivingNeighbors(cell, container):
    x = cell.pos[0]
    y = cell.pos[1]
    neighborsPositions = [
        (x - 1, y - 1), # top left
        (x - 1, y    ), # left
        (x - 1, y + 1), # bottom left
        (x,     y + 1), # bottom
        (x + 1, y + 1), # bottom right
        (x + 1, y    ), # right
        (x + 1, y - 1), # top right
        (x,     y - 1), # top
    ]

    neighbors_list = []
    for pos in neighborsPositions:
        neighbor = getCellAtIndex(pos)
        if neighbor.__class__.__name__ != 'Cell':
            pass
        else:
            neighbors_list.append(neighbor)

    count = 0
    for cell in neighbors_list:
        if cell.isAlive():
            count = count + 1
        else:
            pass
    return count

"""
Returns weather the cell will be alive in the next generation
"""
def willBeAlive(cell, container):
    c = countLivingNeighbors(cell, container)
    if cell.isAlive():
        # cell will die of loneliness
        if c < 2 or c > 3:
            return False
        else:
            return True
    else:
        # cell will be resurrected
        if c == 3:
            return True
        else:
            return False

"""
Returns cell array index based on the cell position on the grid.
If the index exeeds the bounds of the grid, return negative value
"""
def getCellsIndex(pos):
    # return false if not on the grid
    if 0 <= pos[0] <= 31 and 0 <= pos[1] <= 31:
        return pos[1] * 32 + pos[0]
    else:
        return -1
"""
Return cell reference from cells global by passing the grid position
"""
def getCellAtIndex(pos):
    # return cell or void
    idx = getCellsIndex(pos)
    if idx < 0:
        return
    else:
        return cells[idx]

def test():
    # resurrect some cells and check if counting alive neighbors works
    """
    getCellAtIndex((0, 0)).is_alive = True
    getCellAtIndex((1, 0)).is_alive = True
    getCellAtIndex((1, 2)).is_alive = True
    """
    getCellAtIndex((1, 1)).is_alive = True
    getCellAtIndex((1, 2)).is_alive = True
    getCellAtIndex((1, 3)).is_alive = True
    print(countLivingNeighbors(getCellAtIndex((0,1)), cells))
    



import sys, pygame
pygame.init()

"""
Globals
"""
SIZE = WIDTH, HEIGHT = 1024, 1024
SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()

cells = []

COLOR_BLACK = (0, 0, 0)
COLOR_ALIVE = (0, 120, 0)
COLOR_DEAD  = (90, 90, 90)

# init cell grid (32 x 32 cells)
initCells(cells)
test()

# Game Loop
while True:
    # User Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    # FPS
    CLOCK.tick(1)

    # Erase the screen
    SCREEN.fill(COLOR_BLACK)

    # Draw all the cells
    for cell in cells:
        drawCell(cell)

    # Update cells for next generation
    updateCells()

    # Update the visible display
    pygame.display.flip()

