"""
The gameboard for the Connect-N game.

This module keeps the board state of the game. This game supports R rows, C columns, and
a requirement of N in a line to win.  Traditionally, all of these values are fixed to:

    R == 6
    C == 7
    N == 4

Our version of the game allows variations on some or all of these parameters.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
import introcs
from a6consts import *

#### TASK 2 ####
class Board:
    """
    A class to represent a game board.

    This class stores the current state of the game board, namely what pieces
    are filled in, as well as the state of the game. Game pieces are
    represented as color strings. An empty board location corresponds to the
    empty string.
    """
    # HIDDEN ATTRIBUTES
    # Attribute _width: The number of columns in the game board
    # Invariant: _width is an int > 0
    #
    # Attribute _height: The number of rows in the game board
    # Invariant: _height is an int > 0
    #
    # Attribute: _streak: Minimum-length run of same color-pieces needed to win
    # Invariant: _streak is an int > 0 and <= min(_width,_height)
    #
    # Attribute _board: a 2d table storing the game pieces.
    # Invariant: _board is a 2d table of size _height by _width, containing
    #            strings. These strings are empty or a valid color name.
    #
    # Attribute _moves: The saved moves in the game
    # Invariant: _moves is a list of (int,int) tuples and has length less than
    #            _width*_height. It's length is equal to the number of non-empty
    #            places in the board.

    #### PART A ####
    def getWidth(self):
        """
        Returns the width (i.e. number of columns) in this board.
        """
        return self._width

    def getHeight(self):
        """
        Returns the height (i.e. number of rows) in this board.
        """
        return self._height

    def getStreak(self):
        """
        Returns the number of pieces in a row necessary to win

        The pieces can be horizontal, vertical, or diagonal, but they must all
        be the same color.
        """
        return self._streak

    def __init__(self,rows=6,cols=7,streak=4):
        """
        Initializes a board with the given dimensions and win-streak.

        The board should be initialized as empty, meaning that the color for
        all board locations is the empty string. There are NO saved moves at
        the beginning, so that list is empty.

        The default values define a traditional Connect 4 setup.

        Parameter rows: The number of rows in the board (DEFAULT 6)
        Precondition: rows is an int > 0

        Parameter cols: The number of columns in the board (DEFAULT 7)
        Precondition: cols is an int > 0

        Parameter streak: The number of pieces in a line necessary to win
        (DEFAULT 4)
        Precondition: streak is an int > 0 and <= min(rows,cols)
        """
        assert isinstance(rows,int)
        assert rows > 0
        assert isinstance(cols,int)
        assert cols > 0
        assert isinstance(streak,int)
        assert streak > 0 and streak <= min(rows,cols)

        self._height = rows
        self._width = cols
        self._streak = streak
        self._board = [['' for x in range(cols)]for x in range(rows)]
        self.clear()

    def clear(self):
        """
        Clears the board of all pieces.

        The board will be rebuilt so that all locations are now the empty string.
        In addition, the list of moves will be reset to the empty list.
        """
        for rows in range(self._height):
            for cols in range(self._width):
                self._board[rows][cols] = ''
        self._moves = []

    def getColor(self,r,c):
        """
        Returns the piece color stored in the board at (r,c).

        The value returns is a string representing a color. If no piece
        occupies (r,c), this method will return the empty string.

        Parameter r: The row
        Precondition: r is an int and a valid row position in board

        Parameter c: The column
        Precondition: c is an int and a valid column position in board
        """
        assert isinstance(r,int)
        assert r < self._height
        assert isinstance(c,int)
        assert c < self._width

        if self._board[r][c] is None:
            return ''
        else:
            return self._board[r][c]


    def getMoveCount(self):
        """
        Returns the number of moves that have been made so far.

        This is equal to the number of pieces in the board.
        """
        return len(self._moves)

    def getLastMove(self):
        """
        Returns the last move made.

        The value will be in the format (row,column)
        """
        return self._moves[-1]

    #### PART B ####
    def findAvailableRow(self,col):
        """
        Returns the lowest row in column col that has no piece in it.

        If this column is full, this method returns the value of getHeight().

        Parameter col: The column
        Precondition: col is an int and a valid column in this board.
        """
        assert isinstance(col,int)
        assert 0 <= col < self._width

        for row in range(self._height):
            if self._board[row][col] == "":
                return row
        return self.getHeight()

    def isFullColumn(self,col):
        """
        Returns True if there is no available position in column c, False
        otherwise

        Parameter col: The column
        Precondition: col is an int and a valid column in this board.
        """
        assert isinstance(col,int)
        assert 0 <= col < self._width

        answer = self.findAvailableRow(col)
        return answer == self._height

    def isFullBoard(self):
        """
        Returns True if every location on the game board is full, False
        otherwise.

        The board is full is every location stores a non-empty string.
        """
        for col in range(self._width):
            if not self.isFullColumn(col):
                return False
        else:
            return True


    def place(self,column,color):
        """
        Returns the row that this color was placed in the given column.

        This is an interesting method that is both fruitful and mutable. It
        attempts to place the given color at the specified column. If
        successful, it updates the board and returns the row in which it was
        placed. But if that column is full, the board is not updated and this
        method returns -1 instead.

        When a piece is sucessfully placed (so this function does not
        return -1), we add (row,column) to the list of moves.

        Parameter column: The column to place the piece
        Precondition: column is an int and a valid column in this board.

        Parameter color: The piece color
        Precondition: color is a valid color string (i.e., either
        introcs.is_tkcolor or introcs.is_webcolor returns True).
        """
        assert introcs.is_tkcolor(color) or introcs.is_webcolor(color)
        assert isinstance(column,int)
        assert 0 <= column < self._width
        rows = self._height

        for row in range(self._height):
            if self._board[row][column]== '':
                self._board[row][column] = color
                self._moves.append((row,column))
                return row
        return -1

    def undoPlace(self):
        """
        Removes the last piece placed in the board.

        This method looks at the last element in the moves list. It erases that
        color from the board (by setting that position to the empty string) and
        removes it from the move list. If no moves have yet been made, this
        method does nothing.

        Calling this method multiple times will undo the entire board.
        """
        if len(self._moves) != 0:
            last_row, last_col = self._moves.pop()
            self._board[last_row][last_col] = ''
        else:
            pass



    # WE HAVE IMPLEMENTED THIS FUNCTION FOR YOU
    # DO NOT MODIFY THIS METHOD
    def __str__(self):
        """
        Returns the string representation of this board

        The string should be displayed as a 2D list of colors in row-major
        order STARTING FROM THE TOP ROW.  The left brackets of each row should
        be aligned, and every entry should be padded to ensure a uniform width
        in the display.

        For example, suppose we have a 3x3 board with the following state:

            [['red','blue','red'],['','blue','red'],['','red','blue']]

        Then the string should be

            "[['    ', 'red ','blue'],\n ['    ','blue','red '],\n ['red ','blue','red ']]"

        Note the newlines (\n) after each row. That is because when you print
        this string, it will look like this:

            [['    ','red ','blue'],
             ['    ','blue','red '],
             ['red ','blue','red ']]

        This is useful for debugging, since it allows us to see each row of the
        board on its own line.

        There should be no spaces after the commas or brackets.
        """
        # Find padding:
        pad = 0
        for r in self._board:
            for c in range(len(r)):
                if len(r[c]) > pad:
                    pad = len(r[c])

        # Now print, with last row at the top, to match the visuals of
        # a physical board
        result = '['
        for row in range(self._height-1,-1,-1):
            if row < self._height-1:
                result += ' '  # to line up everything with the top row
            result += '['
            for col in range(self._width):
                result += repr(self._board[row][col].ljust(pad))
                result += ','
            result = result[:-1]
            result += '],\n'
        result = result[:-2]
        result += ']'

        return result


#### TASK 4 ####

    # EXAMPLE: This function has been provided for your reference.
    # Use it to help you write the other functions
    def findVertical(self,r,c,leng):
        """
        Returns the endpoints (r1,c1,r2,c2) for a vertical win (or None if does
        not exist).

        This function looks for a vertical win when a piece is dropped at
        (r,c). That means, when this method is called, there MUST be a piece
        at (r,c). The function then looks for the longest vertical run of that
        color in the board.

        Note that as a piece is always played at the top, the run can only
        include pieces below this one in the same column.

        The value returned is of the form (r1,c1,r2,c2) where (r1,c1) is the
        topmost position (the same as (r,c)) and (r2,c2) is the bottom-most.
        However, it only returns this value if the length of this sequence is
        >= leng. Otherwise, it returns None.

        Parameter r: The row of the last placed piece
        Precondition: r is an int and a valid row in the board; there is a
        color in (r,c)

        Parameter c: The column of the last placed piece
        Precondition: c is an int and a valid column in the board; there is a
        color in (r,c)

        Parameter leng: The minimum length to count as a "win"
        Precondition: leng is an int > 0
        """
        assert type(r) == int
        assert type(c) == int
        assert type(leng) == int and leng > 0
        assert in_range(self,r,c)
        assert self._board[r][c] != None

        color = self._board[r][c]

        # We are looping over rows in column c starting at position r
        r2 = r

        # Loop until we go out of bounds, or find a different color
        while r2 >= 0 and self._board[r2][c] == color:
            r2 = r2-1       # We are going downwards

        # The loop ALWAYS guarantees we went one too far (out of bounds or wrong color).
        # Back up one.
        r2 = r2+1

        # Only return the tuple if it is long enough
        if dist(self,r,c,r2,c) >= leng:
            return (r,c,r2,c)
        else:
            return None

    # IMPLEMENT THESE METHODS
    #### PART D ####
    def findAcross(self,r,c,leng):
        """
        Returns the endpoints (r1,c1,r2,c2) for a horizontal win (or None if
        does not exist).

        This function looks for a horizontal win when a piece is dropped at
        (r,c). That means, when this method is called, there MUST be a piece at
        (r,c). The function then looks for the longest horizontal run of that
        color in the board.

        The value returned is of the form (r1,c1,r2,c2) where (r1,c1) is the
        left-most position of the run, and (r2,c2) is the right-most. As this
        is a horizontal run, r1 = r2 = r, while c1 <= c <= c2.

        This method only returns this value if the length of this sequence is
        >= leng. Otherwise, it returns None.

        Parameter r: The row of the last placed piece
        Precondition: r is an int and a valid row in the board; there is a
        color in (r,c)

        Parameter c: The column of the last placed piece
        Precondition: c is an int and a valid column in the board; there is a
        color in (r,c)

        Parameter leng: The minimum length to count as a "win"
        Precondition: leng is an int > 0
        """
        # HINTS:
        # 1. Use two while-loops, one searching the left of (r,c) and the other the right
        # 2. The while loops should continue until you go out of bounds or the board
        #    color does not match the color of the original piece
        # 3. The position should end where the colors match, so you need to "back up"
        # 2. The while loops should continues until the board color does not match the
        #    color of the original piece
        # 3. Make sure you stop the loop before the column goes out of bounds
        # 4. Use dist to make sure the length of the run is long enough

        #assert stuff
        assert isinstance(r, int)
        assert isinstance(c, int)
        assert isinstance(leng, int) and leng > 0
        assert in_range(self,r,c)
        assert self._board[r][c] != None

        color = self._board[r][c]

        # Loop until we go out of bounds, or find a different color
        c2 = c
        while c2 < self.getWidth() and self._board[r][c2] == color:
            c2 = c2+ 1       # going right
        c3 = c
        while c3 >= 0 and self._board[r][c3] == color:
            c3 = c3 -1      # going left
        # Go back to board
        c2 = c2 - 1
        c3 = c3 + 1
        # Only return the tuple if it is long enough
        if dist(self,r,c3,r,c2) >= leng:
            return (r,c3,r,c2)
        else:
            return None


    def findSWNE(self,r,c,leng):
        """
        Returns the endpoints (r1,c1,r2,c2) for a SWNE diagonal win (or None if
        does not exist).

        The runs returned by this method will go from the "southwest" to the
        "northeast", on a line that goes through board position (r,c). The run
        must be at least as long as leng (though it can be longer). If a leng
        run is found, this method returns the endpoints of the diagonal run.
        Otherwise, it returns None.

        Parameter r: The row of the last placed piece
        Precondition: r is an int and a valid row in the board; there is a
        color in (r,c)

        Parameter c: The column of the last placed piece
        Precondition: c is an int and a valid column in the board; there is a
        color in (r,c)

        Parameter leng: The minimum length to count as a "win"
        Precondition: leng is an int > 0
        """
        # HINTS:
        # 1. Use two while-loops, one searching the SW of (r,c) and the other the NE
        # 2. The while loops should continue until you go out of bounds or the board
        #    color does not match the color of the original piece
        # 3. The position should end where the colors match, so you need to "back up"
        # 4. Use dist to make sure the length of the run is long enough
        assert isinstance(r, int)
        assert isinstance(c, int)
        assert isinstance(leng, int) and leng > 0
        assert in_range(self,r,c)
        assert self._board[r][c] != None

        color = self._board[r][c]

        r5 = r
        c5 = c
        while r5 < self.getHeight() and c5 < self.getWidth()\
         and self._board[r5][c5] == color:
            r5 = r5 + 1       # going up and right
            c5 = c5 + 1

        r4 = r
        c4 = c
        while r4 >= 0 and c4 >= 0 and self._board[r4][c4] == color:
            r4 = r4 - 1       # going down and left
            c4 = c4 - 1

        #Make sure it's in board
        r5 = r5 - 1
        c5 = c5 - 1
        r4 = r4 + 1
        c4 = c4 + 1

        if dist(self,r4,c4,r5,c5) >= leng:
            return (r4,c4,r5,c5)
        else:
            return None

    def findNWSE(self,r,c,leng):
        """
        Returns the endpoints (r1,c1,r2,c2) for a NWSE diagonal win (or None if
        does not exist).

        The runs returned by this method will go from the "northwest" to the
        "southeast", on a line that goes through board position (r,c). The run
        must be at least as long as leng (though it can be longer). If a leng
        run is found, this method returns the endpoints of the diagonal run.
        Otherwise, it returns None.

        Parameter r: The row of the last placed piece
        Precondition: r is an int and a valid row in the board; there is a
        color in (r,c)

        Parameter c: The column of the last placed piece
        Precondition: c is an int and a valid column in the board; there is a
        color in (r,c)

        Parameter leng: The minimum length to count as a "win"
        Precondition: leng is an int > 0
        """
        # HINTS:
        # 1. Use two while-loops, one searching the NW of (r,c) and the other the SE
        # 2. The while loops should continue until you go out of bounds or the board
        #    color does not match the color of the original piece
        # 3. The position should end where the colors match, so you need to "back up"
        # 4. Use dist to make sure the length of the run is long enough
        assert isinstance(r, int)
        assert isinstance(c, int)
        assert isinstance(leng, int) and leng > 0
        assert in_range(self,r,c)
        assert self._board[r][c] != None

        color = self._board[r][c]

        r3 = r
        c3 = c
        while r3 >= 0 and c3 < self.getWidth()\
         and self._board[r3][c3] == color:
            r3 = r3 - 1       # going down and right
            c3 = c3 + 1

        r6 = r
        c6 = c
        while r6 < self.getHeight() and c6 >= 0 and\
         self._board[r6][c6] == color:
            r6 = r6 + 1       # going up and left
            c6 = c6 - 1
        #Make sure it's in board
        r3 = r3 + 1
        c3 = c3 - 1
        r6 = r6 - 1
        c6 = c6 + 1

        if dist(self,r6,c6,r3,c3) >= leng:
            return (r6,c6,r3,c3)
        else:
            return None

    def findWins(self,r,c):
        """
        Returns the endpoints (r1,c1,r2,c2) of a win (or None if does not exist).

        This method searches for a win containing (r,c). It uses findVertical,
        findAcross, findSWNE, and findNWSE as helpers with getStreak() as the
        minimum win length. In the case of multiple wins, it returns the first
        one found in this order: vertical, across, SWNE, and finally NWSE.

        Parameter r: The row of the last placed piece
        Precondition: r is an int and a valid row in the board; there is a color
        in (r,c)

        Parameter c: The column of the last placed piece
        Precondition: c is an int and a valid column in the board; there is a color
        in (r,c)
        """
        assert isinstance(c, int)
        assert isinstance(r, int)
        assert in_range(self,r,c)
        assert self._board[r][c] != None

        if self.findVertical(r,c,self.getStreak()) != None:
            return self.findVertical(r,c,self.getStreak())
        elif self.findAcross(r,c,self.getStreak()) != None:
            return self.findAcross(r,c,self.getStreak())
        elif self.findSWNE(r,c,self.getStreak()) != None:
            return self.findSWNE(r,c,self.getStreak())
        elif self.findNWSE(r,c,self.getStreak()) != None:
            return self.findNWSE(r,c,self.getStreak())
        else:
            return None


#### HELPER FUNCTIONS ####
# DO NOT MODIFY
def in_range(board,r,c):
    """
    Returns True (r,c) is a valid board position, False otherwise.

    Parameter board: The game board
    Precondition: board is a Board object

    Parameter r: The candidate row
    Precondition: r is an int

    Parameter c: The candidate column
    Precondition: c is an int
    """
    return 0 <= r < board.getHeight() and 0 <= c < board.getWidth()


def dist(board,r1,c1,r2,c2):
    """
    Returns the number of board positions between (r1,c1) and (r2,c2)

    The number computed includes those endpoints. Assuming the arguments are
    valid board coordinates, the smallest value that can be returned is 1, when
    (r1,c1) == (r2,c2).

    Distance is computed in all directions, horizontally, vertically, and
    diagonally. This is necessary for checking wins. However, if the endpoints
    do not form a valid diagonal (say (1,1) to (2,3)) then the number received
    may be unexpected.

    The positions that lie between the two endpoints do not have to be filled.

    Parameter board: The game board
    Precondition: board is a Board object

    Parameter r1: The initial row
    Precondition: r1 is an int and a valid row position in board

    Parameter c1: The initial column
    Precondition: c1 is an int and a valid column position in board

    Parameter r2: The final row
    Precondition: r2 is an int and a valid row position in board

    Parameter c2: The final column
    Precondition: c2 is an int and a valid column position in board
    """
    assert type(r1) == int and type(c1) == int
    assert type(r2) == int and type(c2) == int
    assert in_range(board,r1,c1) and in_range(board,r2,c2)
    if (r1 != r2):
        return abs(r1-r2) + 1
    else:
        return abs(c1-c2) + 1
