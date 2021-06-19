# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
from numpy.core.fromnumeric import choose
from chromosome import Chromosome


# %%
class Population:
    def __init__(self, chromosomes=None, rng=None) -> None:
        # filling random values if None
        if rng is None:
            rng = 10
        if chromosomes is None:
            chromosomes = [Chromosome() for _ in range(1, rng)]

        self.chromosomes = np.array(chromosomes)

    def __str__(self) -> str:
        return (
            self.chromosomes.__str__()
        )

    # for population indexing
    def __getitem__(self, index):
        return self.chromosomes[index]

    def get_best(self):
        if self.chromosomes.size == 0:
            return 0
        best_chromosome = self.chromosomes[0]
        for chromosome in self.chromosomes:
            if best_chromosome.fitnessval < chromosome.fitnessval:
                best_chromosome = chromosome
        return best_chromosome, best_chromosome.fitnessval
