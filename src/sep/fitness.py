# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Fitness & Constraints
# %%
import data
from gene import *
from chromosome import *
# %% [markdown]
# ## Constraints
# %% [markdown]
# ### Hard Constrains

# %%


def one_exam_in_one_slot(chromosome):
    '''
    One course exam should be in a slot
    And after that slot or before that slot there should
    be no exam of the course
    More means bad
    '''

    courses = chromosome.get_courses()
    slots = chromosome.get_slots()

    courseslot = np.array([[course, slot]
                           for slot, course in zip(slots, courses)])

    # sorting
    courseslot = courseslot[courseslot[:, 0].argsort()]

    course_slots = np.split(courseslot[:, 1], np.unique(
        courseslot[:, 0], return_index=True)[1][1:])

    # now in course_slots. Course has list of slots in front of we
    # in our case it should be not longer than 1
    # counter the conflicts in which the slots are more than 1

    lst = [len(slots) for slots in course_slots]

    return sum(lst)-len(lst)


def one_room_have_one_exam(chromosome):
    '''
    One room should have one exam at a given time
    Count of the conflicts (more means bad)

    Will be checking the same_slot, same_room. Which means
    that at the given slot the room is beign used twice.
    We are not looking at the course because there should 
    be no duplicated in chromosome for the same room and same slot
    '''

    rooms = chromosome.get_rooms()
    slots = chromosome.get_slots()

    slotroom = [(slot, room) for slot, room in zip(slots, rooms)]

    # unique slot room and there counts
    _, counts = np.unique(slotroom, axis=0, return_counts=True)

    # counting of duplicate exams in one slot and one room
    dups = sum(counts)-len(counts)

    return dups


def student_one_exam_at_a_time(chromosome):
    '''
    At a given time, student can only give one exam

    In this I'll be also checking the duplication of student in the room
    and also in the course. Remeber the course can have multiple rooms within one slot.
    So in short I'll be looking for the same student in the same slot at multiple places

    Counting the conflics, more means bad
    '''

    dupstudents = 0  # duplicates of students in more than one slots
    dupexam = 0  # multiple exam of students at a time

    for i in range(len(chromosome.genes)):
        for student in chromosome.genes[i].students:
            for gene in chromosome:
                if gene == chromosome.genes[i] != gene.slot == chromosome.genes[i].slot:
                    if student in gene.students:  # multiple exam
                        dupexam += 1

        # counting duplicates of student in the same room
        dupstudents += len(chromosome.genes[i].students) - \
            len(set(chromosome.genes[i].students))

    return dupstudents+dupexam


def one_exam_per_course(chromosome):
    ''' 
    Every course should have one exam
    Not two Not zero, only one
    Count of the conflicts (more means bad)
    '''

    courses = chromosome.get_courses()

    uniquecourses, counts = np.unique(courses, return_counts=True)

    # counting the courses which don't have exam
    nocourseexam = len(data.courses)-len(uniquecourses)

    # counting of courses which have exam more than once
    dupcourseexam = sum(counts)-len(counts)

    return nocourseexam+dupcourseexam


def student_taking_correct_exam(chromosome):
    ''' 
    The Students must take every exam in which they are registered in
    Doesn't Count the number of missing courses for student XXX
    Count the number of missing student in courses
    more count means bad
    '''

    missing_students = 0  # number of students that are missing from exam

    for genes in chromosome:
        correct_sitting = 0
        for student in genes.students:
            stu_courses = data.get_student_courses(student, data.regs)
            if genes.course in stu_courses:
                correct_sitting += 1
        missing_students += len(genes.students)-correct_sitting

    return missing_students

# %%


def room_cap_enough_for_students(chromosome):
    '''
    Every Gene hae room and student
    In here we will just check that there should be enough
    capacity to hold those students 

    Counting conflicts, more means bad
    '''

    # [(room capacity , number of students)]
    roomcap_students = [(data.get_room_cap(gene.room, data.rooms), len(gene.students))
                        for gene in chromosome]

    extra_stu = 0  # counting of extra students in room
    empty_space = 0  # counting of empaty space in room

    for cap, stu in roomcap_students:
        if stu > cap:
            extra_stu += stu-cap
        else:
            empty_space += cap-stu

    # extrastudents+(empty spaces)/10 beacause it's not good to have empty rooms
    return extra_stu+empty_space//10

# %% [markdown]
# Combining constraints


# %%
HARD_CONSTRAINTS = [
    {
        '''
        One course exam should be in a slot
        And after that slot or before that slot there should
        be no exam of the course
        '''
        "name": "One course exam should be in a slot",
        "function": one_exam_in_one_slot,
        "weight": 1,
        "fields": [
            "rooms"
        ]
    },
    {
        '''
        rooms to course. The relation is 'n to 1'
        A course can be in many rooms
        But a room can only have one Course
        '''
        "name": "One room should have only one paper at a time",
        "function": one_room_have_one_exam,
        "weight": 1,
        "fields": [
            "rooms"
        ]
    },
    {
        '''
        A student can't have more than one exam at a time
        '''
        "name": "One student should have one exam at a time",
        "function": student_one_exam_at_a_time,
        "weight": 1,
        "fields": [
            "students"
        ]
    },
    {
        '''
        Every course should have exam
        '''
        "name": "Every Course should have Exam",
        "function": one_exam_per_course,
        "weight": 1,
        "fields": [
            "course"
        ]
    },
    {
        '''
        Every student should have exam of there registered courses
        '''
        "name": "Every Student should have Exam",
        "function": student_taking_correct_exam,
        "weight": 1,
        "fields": [
            "course"
        ]
    },

    {
        "name": "Rooms should have enough space for the present Course Students",
        "function": room_cap_enough_for_students,
        "weight": 1,
        "fields": [
            "students"
            # "rooms" XXX because if we keep changing room and students are 10000 than we
            # will be stuck in infinit loop
        ]
    }
]

# %% [markdown]
# ### Soft Constrains


# %% [markdown]
# ## Fitness

# %%


def cal_fitness(chromosome):
    constraints_score = 0  # scores for the constraint pass
    mutate_fields = []  # field that requires mutation

    # Checking Hard Constraints
    for constraint in HARD_CONSTRAINTS:
        score = constraint['function'](chromosome)*constraint['weight']
        constraints_score += score
        if score > 10:
            # threshold setting
            # score > 10 means bad score
            if constraint["fields"] not in mutate_fields:
                mutate_fields += constraint["fields"]

    # Assigning the calculated fitness to the chromosome
    # range is 0-1. 0 beign the lowest and 1 means the perfect
    actualfitness = 1 / ((1.0*constraints_score+1))
    chromosome.fitnessval = actualfitness

    return actualfitness, mutate_fields
