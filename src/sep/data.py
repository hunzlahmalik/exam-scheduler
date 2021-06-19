# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np

# %% [markdown]
# ### To call for the first time data

# %%


def init_data(capfile=None, dayslotfile=None, regsfile=None):
    if capfile is None:
        capfile = "../db/Capacity.csv"
    if dayslotfile is None:
        dayslotfile = "../db/DaysSlots.csv"
    if regsfile is None:
        regsfile = "../db/R_Data.csv"

    #  importing ROOMS CAPACITY
    global rooms
    rooms = pd.read_csv(capfile, names=['RoomID', 'Capacity'], dtype=np.int64)

    #  importing DAY SLOTS
    global slots
    slots = pd.read_csv(dayslotfile, dtype=np.int64)

    #  importing REGISTRATION data
    global regs
    regs = pd.read_csv(regsfile)
    regs = regs.groupby('SID\CID').sum()
    regs = regs.astype(bool)

    #  STUDENTS
    global students
    students = regs.index.to_numpy()
    students

    #  COURSES
    global courses
    courses = regs.columns
    courses = np.array(courses, np.int64)
    courses


# %% [markdown]
# ### Some helpful functions

# %%

def totalrooms(roomsdf):
    return roomsdf['RoomID'].size


def totalstudents(studentsdf):
    return studentsdf.size


def totalslots(slotsdf):
    return slotsdf['Slots'].sum()


def totalcourses(coursesdf):
    return courses.size

# Related to room


def get_room_cap(roomid, roomsdf):
    return roomsdf.loc[roomsdf['RoomID'] == roomid].iloc[0, 1]


def set_room_cap(roomid, capacity, roomsdf):
    roomsdf.loc[roomsdf['RoomID'] == roomid].iloc[0, 1] = capacity


def get_room(index, roomsdf):
    return roomsdf.iloc[index, 0]

# Related to courses


def get_course_students(courseid, registrationdf):
    return registrationdf.loc[registrationdf[str(courseid)] == True].index


def get_student_courses(studentid, registrationdf):
    lst = registrationdf.loc[studentid]
    lst = lst.to_frame()
    return lst[lst[studentid] == True].index.to_numpy(dtype=np.int64)


def student_taking_course(studentid, courseid, registrationdf) -> bool:
    return registrationdf.loc[studentid][str(courseid)]
