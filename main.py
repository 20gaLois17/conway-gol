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
    is_alive          = bool
    is_alive_next_gen = bool
    color_alive       = (0, 120, 0)
    color_dead        = (60, 60, 60)

    def __init__(self, x, y):
        self.pos = (x, y)
        self.is_alive = False
        self.is_alive_next_gen = False

    def __str__(self):
        return "cell at (" + str(self.pos[0]) + "," + str(self.pos[1]) + ")"

    def isAlive(self):
        return True if self.is_alive else False

    def toggle(self):
        self.is_alive = not self.is_alive

    def getColor(self):
        if self.isAlive():
            return self.color_alive
        else:
            return self.color_dead

    def update(self):
        if self.is_alive_next_gen:
            self.is_alive = True
        else:
            self.is_alive = False
        self.is_alive_next_gen = False


"""
Contains Cells and Game Logic
"""
class Grid:
    rows        = int 
    columns     = int 
    cellPadding = int 
    cells       = []

    """
    Initialise 32 x 32 grid
    """
    def __init__(self, columns, rows, cellPadding):
        self.rows = rows
        self.columns = columns
        self.cellPadding = cellPadding 
        for colIndex in range(self.columns):
            for rowIndex in range(self.rows):
                self.cells.append(Cell(rowIndex, colIndex))

    def getCell(self, x, y):
        print(x, y)
        if 0 <= x < self.columns and 0 <= y < self.rows:
            return self.cells[y * self.rows + x]

    # TODO: Clean this up
    def draw(self):
        for cell in self.cells:
            cellWidth = WIDTH / self.columns
            cellHeight = HEIGHT / self.rows
            cellBoxWidth = cellWidth - self.cellPadding
            cellBoxHeight = cellHeight - self.cellPadding
            x = cell.pos[0] * cellWidth
            y = cell.pos[1] * cellHeight
            pygame.draw.rect(SCREEN, cell.getColor(), (x, y, cellBoxWidth, cellBoxHeight))

    def updateCellsForNextGen(self):
        # process flag and update the cells
        for cell in self.cells:
            cell.update()

    """
    Implement the Rules of Conway's Game of Life
    """
    def prepareCellsForNextGen(self):
        for cell in self.cells:
            c = self.countLivingNeighbors(cell)
            if cell.isAlive():
                # cell will die of loneliness
                if c < 2 or c > 3:
                    cell.is_alive_next_gen = False

                # cell will survive this generation
                else:
                    cell.is_alive_next_gen = True
            else:
                # cell will be resurrected
                if c == 3:
                    cell.is_alive_next_gen = True

                else:
                    cell.is_alive_next_gen = False


    def countLivingNeighbors(self, cell):
        x = cell.pos[0]
        y = cell.pos[1]

        neighborPositions = [
            (x,     y - 1),    # top
            (x - 1, y    ),    # left
            (x + 1, y    ),    # right
            (x,     y + 1),    # bottom
            (x - 1, y - 1),    # top left
            (x + 1, y - 1),    # top right
            (x - 1, y + 1),    # bottom left
            (x + 1, y + 1),    # bottom right
        ]

        count = 0
        for pos in neighborPositions:
            neighbor = self.getCell(pos[0], pos[1])
            if neighbor.__class__.__name__ != 'Cell':
                pass
            elif neighbor.isAlive():
                count += 1

        return count

    def click(self, pos):
        x = pos[0] // (WIDTH // self.rows)
        y = pos[1] // (HEIGHT // self.columns)
        print(x)
        print(y)
        cell = grid.getCell(x, y)
        if cell:
            cell.toggle()
        else:
            print("no cell found")

class State:
    run = bool
    def __init__(self):
        self.run = False


"""
User Input
"""
def handleInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == 32:
                state.run = not state.run
        if event.type == pygame.MOUSEBUTTONUP:
            print(event)
            grid.click(event.pos)

import sys, pygame
pygame.init()

"""
Globals
"""
SIZE   = WIDTH, HEIGHT = 1024, 1024
SCREEN = pygame.display.set_mode(SIZE)
CLOCK  = pygame.time.Clock()

COLOR_BLACK = (0, 0, 0)

state = State()
grid  = Grid(8, 16, 2)

COUNTER = 0

# Game Loop
while True:
    # User Input
    handleInput()

    # Update Counter
    COUNTER = (COUNTER + 1) % 60

    # FPS
    CLOCK.tick(60)

    # Erase the screen
    SCREEN.fill(COLOR_BLACK)

    # Draw all the cells
    grid.draw()

    # Update cells for next generation every 60 frames
    
    if state.run and COUNTER == 0:
        grid.prepareCellsForNextGen()
        grid.updateCellsForNextGen()

    # Update the visible display
    pygame.display.flip()

