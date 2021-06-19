# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # GENE
# %% [markdown]
# The chromosome is made up of many genes. In our program we are using course, students, room and slot as our gene. So When these many genes will combine will make a chromosome.
#
# In other words, you can say this is our representation of the genes.
#
# Gene=(course, students, rooms, slot)

# %%
import data
import random as rnd
import numpy as np

# have to remove this line in end
# data.init_data()

# %%


class Gene:
    def __init__(self, course=None, room=None, slot=None, students=None,):
        # if there are None value then we will use random values
        if course is None:
            course = data.courses[rnd.randint(
                0, data.totalcourses(data.courses)-1)]
        if students is None:
            students = self.get_rand_students(course)
        if room is None:
            room = self.get_rand_rooms()
        if slot is None:
            slot = self.get_rand_slot()

        # copying to the self variables
        self.course = course
        self.room = room
        self.slot = slot
        self.students = students

    def __str__(self) -> str:
        return (
            "Gene[" +
            "course="+str(self.course)+", " +
            "rooms="+str(self.room)+", " +
            "slot="+str(self.slot)+", " +
            "students="+str(self.students) +
            "]"
        )

    # to get all students
    def get_students(self):
        return self.students

    def get_rand_rooms(self):
        return data.get_room(rnd.randint(0, data.totalrooms(data.rooms)-1), data.rooms)
        # totalrooms = data.totalrooms(data.rooms)
        # return [data.get_room(rnd.randint(0, totalrooms-1), data.rooms) for _ in range(rnd.randint(1, totalrooms-1))]

    def get_rand_slot(self):
        return rnd.randint(1, data.totalslots(data.slots))

    def get_rand_students(self, course):
        return np.array([rnd.randint(1, data.totalstudents(data.students) - 1)
                         for _ in range(len(data.get_course_students(course, data.regs)))])

# testing
# Gene()
