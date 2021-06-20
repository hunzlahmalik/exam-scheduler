#### function
def neighbourhood_operator(chromosome):
    chromosome=Chromosome()
    course=np.random.choice(chromosome.get_courses())
    slot=np.random.choice(chromosome.get_slots())
    room=np.random.choice(chromosome.get_rooms())
    students=chromosome.get_students_of_course(course)
    gen=Gene(course,room,slot,students)
    return gen
### usage 
chromosome.append(neighbourhood_operator(chromosome))

