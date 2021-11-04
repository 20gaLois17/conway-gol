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

    """
    :param x: column index
    :param y: row index
    """
    def __init__(self, x, y):
        self.pos = (x, y)
        self.is_alive = False
        self.is_alive_next_gen = False

    def __str__(self):
        return f"cell at ({str(self.pos[0])}, {str(self.pos[1])})"

    def isAlive(self):
        return self.is_alive

    def setAlive(self, a):
        self.is_alive = a

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
    rows          = int
    columns       = int
    cellPadding   = int
    cellBoxWidth  = float
    cellBoxHeight = float
    cells         = []

    """
    :param columns: number of grid columns
    :param rows: number of grid rows
    :param cellPadding: padding (in px) between cells
    """
    def __init__(self, columns, rows, cellPadding):
        # set sensible boundaries
        if not (4 <= columns < 128 and 4 <= rows < 128):
            print("exceeding sensible grid dimensions")
            return

        self.cells         = []
        self.columns       = columns
        self.rows          = rows
        self.cellPadding   = cellPadding
        self.cellBoxWidth  = HEIGHT / self.columns
        self.cellBoxHeight = HEIGHT / self.rows

        # initialise cells
        for colIndex in range(self.rows):
            for rowIndex in range(self.columns):
                self.cells.append(Cell(rowIndex, colIndex))


    """
    Returns the cell by column and row index on the grid, if not out of bound
    :param x: the column index for the cell
    :param y: the row index for the cell
    """
    def getCell(self, x, y):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            return self.cells[y * self.columns + x]

    """
    Draws all cells to the screen, dead or alive cells will have different colors
    """
    def draw(self):
        for cell in self.cells:
            cellWidth = self.cellBoxWidth - self.cellPadding
            cellHeight = self.cellBoxHeight - self.cellPadding
            x = cell.pos[0] * self.cellBoxWidth
            y = cell.pos[1] * self.cellBoxHeight
            pygame.draw.rect(SCREEN, cell.getColor(), (x, y, cellWidth, cellHeight))

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

    """
    Find neighbors to given cell on the grid and cound the living ones to
    be able to decide the cell's fate
    """
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
            if neighbor.__class__.__name__ != "Cell":
                pass
            elif neighbor.isAlive():
                count += 1

        return count

    """
    Handle Click Event
    :param pos: Position of the Click on the screen
    """
    def click(self, pos):
        x = int(pos[0] // (WIDTH / self.columns))
        y = int(pos[1] // (HEIGHT / self.rows))
        cell = grid.getCell(x, y)
        if cell:
            cell.setAlive(not cell.is_alive)
        else:
            print("no cell found")

class State:
    run   = bool
    frame = int
    grid  = None

    def __init__(self, grid):
        self.stop()
        self.frame = 0
        self.grid = grid

    """
    Right now the game refreshes at 60 fps.
    To make the change on the grid over time more readable, we only update
    the cells once per second (every 60 frames)
    """
    def nextFrame(self):
        if not self.run: return

        self.frame = (self.frame + 1) % 60
        if self.frame == 0:
            self.grid.prepareCellsForNextGen()
            self.grid.updateCellsForNextGen()

    def go(self):
        self.run = True
        pygame.display.set_caption("Game of Life")

    def stop(self):
        self.run = False
        pygame.display.set_caption("Game of Life -- PAUSED --")

"""
User Input
"""
def handleInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYUP:
            # toggle stop / go
            if event.key == 32:
                if state.run:
                    state.stop()
                else:
                    state.go()

            # double number of cells on the grid
            if event.key == 45:
                state.stop()
                grid.__init__(grid.columns * 2 , grid.rows * 2, 1)

            # half number of cells on the grid
            if event.key == 61:
                state.stop()
                grid.__init__(grid.columns // 2, grid.rows // 2, 1)


        # TODO: Draw figure with mouse instead of clicking every cell
        if event.type == pygame.MOUSEBUTTONUP:
            grid.click(event.pos)

import sys, pygame
pygame.init()


# Globals
SIZE   = WIDTH, HEIGHT = 1024, 1024
SCREEN = pygame.display.set_mode(SIZE)
CLOCK  = pygame.time.Clock()

# Init
grid  = Grid(16, 16, 1)
state = State(grid)

# Game Loop
while True:
    # User Input
    handleInput()

    # FPS
    CLOCK.tick(60)

    # Erase the screen
    SCREEN.fill((0, 0, 0))

    # Draw all the cells
    grid.draw()

    state.nextFrame()

    # Update the visible display
    pygame.display.flip()
