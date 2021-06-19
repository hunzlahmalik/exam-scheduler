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

'''No need for this
beacause the course will be unique
'''
# def one_exam_in_one_slot(chromosome):
#     '''
#     One course exam should be in a slot
#     And after that slot or before that slot there should
#     be no exam of the course
#     '''

#     chromosome = Chromosome

#     courses = chromosome.get_courses()
#     slots = chromosome.get_slots()

#     slotcourse = [(slot, course) for slot, course in zip(slots, courses)]

#     # unique slot room and there counts
#     _, counts = np.unique(slotcourse, axis=0, return_counts=True)

#     # counting of duplicate exams in one slot and one room
#     dups = sum(counts)-len(counts)

#     return dups


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

    Counting the conflics, more means bad
    '''

    # # Note: Also test the current gene from which the student is selected, because the same student might be repeated in a single class
    # score = 0
    # i = j = 0

    # while i < len(chromosome.genes):
    #     for student in chromosome.genes[i].students:
    #         for genes in chromosome:
    #             if genes == chromosome.genes[i]:
    #                 continue
    #             if genes.start_time == chromosome.genes[i].start_time and genes.day == chromosome.genes[i].day:
    #                 if student in genes.students:
    #                     # print('Student in multiple exam')
    #                     continue
    #                 else:
    #                     score += 10
    #     i += 1

    # return score
    return 0


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
            "rooms"
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
        constraints_score += constraint['function'](
            chromosome)*constraint['weight']
        # if constraints_score < 1000:
        #     if constraint["fields"] not in mutate_fields:
        #         mutate_fields += constraint["fields"]

    # Assigning the calculated fitness to the chromosome
    chromosome.fitnessval = constraints_score

    return constraints_score, mutate_fields
