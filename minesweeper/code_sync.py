import psutil
import os
import time


class CodeSync:
    def __init__(self, sentenceList, knowledge, mines, safes):
        self.sentenceList = sentenceList
        self.knowledge = knowledge
        self.mines = mines
        self.safes = safes

    # Getters
    def get_sentenceList(self):
        return self.sentenceList

    def get_knowledge(self):
        return self.knowledge

    def get_mines(self):
        return self.mines

    def get_safes(self):
        return self.safes

    def get_code_sync(self):
        return self

    # Setters
    def set_sentenceList(self, sentenceList):
        self.sentenceList = sentenceList

    def set_knowledge(self, knowledge):
        self.knowledge = knowledge

    def set_mines(self, mines):
        self.mines = mines

    def set_safes(self, safes):
        self.safes = safes
