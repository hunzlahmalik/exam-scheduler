# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from gene import *
import random as rnd
import numpy as np


# %%
class Chromosome:
    def __init__(self, genes=None, fitnessval=None, rng=None):
        # filling random values if None
        if rng is None:
            rng = rnd.randint(30, 50)
        if genes is None:
            genes = [Gene() for _ in range(0, rng)]
        if fitnessval is None:
            fitnessval = 0

        self.genes = np.array(genes)
        self.fitnessval = fitnessval

    # for genes list indexing
    def __getitem__(self, index):
        return self.genes[index]

        # for printing
    def __str__(self) -> str:
        return (
            "Chrom[" +
            "Genes="+str(len(self.genes))+", " +
            "Fitness="+str(self.fitnessval) +
            "]"
        )

    def __repr__(self) -> str:
        return self.__str__()

    # Courses of every gene
    def get_courses(self):
        return np.array([gene.course for gene in self.genes])

    def get_slots(self):
        return np.array([gene.slot for gene in self.genes])

    def get_rooms(self):
        return np.array([gene.room for gene in self.genes])

    def get_room_students(self, roomid):
        return np.array([gene.students for gene in self.genes if gene.room == roomid])

    def get_all_students(self):
        return np.concatenate([gene.students for gene in self.genes])

# testing
# c = Chromosome()
# c.get_all_students()
# print(c)
