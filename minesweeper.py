from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import random
from base64 import b64encode, b64decode
from device_profiler import DeviceProfiler
import xmlrpc.client
from object_encoder import ObjectEncoder, as_python_object
from code_sync import CodeSync
from profiler import *
import sys
from constants import *

class Minesweeper():

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        return self.mines_found == self.mines


class Sentence():

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if len(self.cells) == self.count:
            return self.cells
        return None

    def known_safes(self):
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        newCells = set()
        for item in self.cells:
            if item != cell:
                newCells.add(item)
            else:
                self.count -= 1
        self.cells = newCells

    def mark_safe(self, cell):
        newCells = set()
        for item in self.cells:
            if item != cell:
                newCells.add(item)
        self.cells = newCells


class MinesweeperAI():

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.remote_count = 0
        self.local_count = 0
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []
        self.sentenceList = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        # Mark cell as safe and add to moves_made
        self.mark_safe(cell)
        self.moves_made.add(cell)

        # Create and Add sentence to knowledge
        neighbors, count = self.get_cell_neighbors(cell, count)

        # Ex:{A,B,C} = 2 where A,B,C is each a tuple of (i, j) coordinates and 2 is the number of mines
        sentence = Sentence(neighbors, count)
        self.knowledge.append(sentence)

        self.sentenceList.append(sentence)

    def conclusion(self):

        # Conclusion
        for sentence in self.sentenceList:

            new_inferences = []
            for s in self.knowledge:
                if s == sentence:
                    continue
                elif s.cells.issuperset(sentence.cells):
                    setDiff = s.cells-sentence.cells
                    # Known safes
                    if s.count == sentence.count:
                        for safeFound in setDiff:
                            self.mark_safe(safeFound)
                    # Known mines
                    elif len(setDiff) == s.count - sentence.count:
                        for mineFound in setDiff:
                            self.mark_mine(mineFound)
                    # Known inference
                    else:
                        new_inferences.append(
                            Sentence(setDiff, s.count - sentence.count)
                        )
                elif sentence.cells.issuperset(s.cells):
                    setDiff = sentence.cells-s.cells
                    # Known safes
                    if s.count == sentence.count:
                        for safeFound in setDiff:
                            self.mark_safe(safeFound)
                    # Known mines
                    elif len(setDiff) == sentence.count - s.count:
                        for mineFound in setDiff:
                            self.mark_mine(mineFound)
                    # Known inference
                    else:
                        new_inferences.append(
                            Sentence(setDiff, sentence.count - s.count)
                        )

            self.knowledge.extend(new_inferences)
            self.remove_dups()
            self.remove_sures()

        self.sentenceList.clear()

    def make_safe_move(self):

        code_sync_obj = CodeSync(self.sentenceList, self.knowledge,
                                 self.mines, self.safes)

        task = self.conclusion
        obj = dumps(code_sync_obj, cls=ObjectEncoder)
        # TODO: check units
        data_size = sys.getsizeof(obj) / 1024

        profiler = Profiler(task=task, data_size=data_size)

        local_exec_cost = profiler.get_local_execution_cost()
        local_exec_cost = round(local_exec_cost, 3)
        remote_exec_cost = profiler.get_remote_execution_cost()
        remote_exec_cost = round(remote_exec_cost, 3)

        print("Local Execution Cost : ", local_exec_cost, "ms")
        print("Remote Execution Cost: ", remote_exec_cost, "ms")

        flag = 0

        if local_exec_cost < remote_exec_cost:
            self.local_count += 1
            print("Local Execution")
            self.conclusion()
        else:
            print("Remote Execution")
            try:
                server = xmlrpc.client.ServerProxy(
                    Constants.getInstance().SERVER_URL)
            except:
                print("Error in connecting to the remote server!")
                self.local_count += 1
                print("Local Execution")
                self.conclusion()
                flag = 1
            if(flag == 0):
                self.remote_count += 1
                csRemote = server.safe_move_remote(obj)
                try:
                    csResult = loads(csRemote, object_hook=as_python_object)
                except:
                    print("Error in loading the object from the server!")
                    exit()
                    
                # print(csResult.mines, csResult.safes, csResult.knowledge, csResult.sentenceList)
                self.sentenceList = csResult.sentenceList
                self.knowledge = csResult.knowledge
                self.mines = csResult.mines
                self.safes = csResult.safes

        print("Local Count: ", self.local_count)
        print("Remote Count: ", self.remote_count)

        safeCells = self.safes - self.moves_made
        if not safeCells:
            return None

        # print(f"Pool: {safeCells}")
        move = safeCells.pop()
        return move

    def make_random_move(self):
        # self.conclusion()
        all_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.mines and (i, j) not in self.moves_made:
                    all_moves.add((i, j))
        # No moves left
        if len(all_moves) == 0:
            return None
        # Return available
        move = random.choice(tuple(all_moves))
        return move

    def get_cell_neighbors(self, cell, count):
        i, j = cell
        neighbors = []

        for row in range(i-1, i+2):
            for col in range(j-1, j+2):
                if (row >= 0 and row < self.height) \
                        and (col >= 0 and col < self.width) \
                        and (row, col) != cell \
                        and (row, col) not in self.safes \
                        and (row, col) not in self.mines:
                    neighbors.append((row, col))
                if (row, col) in self.mines:
                    count -= 1

        return neighbors, count

    def remove_dups(self):
        unique_knowledge = []
        for s in self.knowledge:
            if s not in unique_knowledge:
                unique_knowledge.append(s)
        self.knowledge = unique_knowledge

    def remove_sures(self):
        final_knowledge = []
        for s in self.knowledge:
            final_knowledge.append(s)
            if s.known_mines():
                for mineFound in s.known_mines():
                    self.mark_mine(mineFound)
                final_knowledge.pop(-1)
            elif s.known_safes():
                for safeFound in s.known_safes():
                    self.mark_safe(safeFound)
                final_knowledge.pop(-1)
        self.knowledge = final_knowledge
