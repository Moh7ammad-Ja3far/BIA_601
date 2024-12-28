import random

def Fitness(Schedule, DoctorsNumber, DoctorCapacities):
    DoctorLoad= [0] * DoctorsNumber
    for Doctor in Schedule:
        DoctorLoad[Doctor] += 1
    Penalty =0
    for i in range(DoctorsNumber):
        if DoctorLoad[i] > DoctorCapacities[i]:
            Penalty += (DoctorLoad[i] - DoctorCapacities[i])* 10
    Reward =0
    for i in range(DoctorsNumber):
        Reward -= abs(DoctorLoad[i] - DoctorCapacities[i])
    if Penalty== 0:
        return Reward
    else:
        return -Penalty

def EnforceCapacity(Schedule, DoctorsNumber, DoctorCapacities):
    DoctorLoad =[0] * DoctorsNumber
    for i in range(len(Schedule)):
        Doctor = Schedule[i]
        if DoctorLoad[Doctor]< DoctorCapacities[Doctor]:
            DoctorLoad[Doctor]+= 1
        else:
            for NewDoctor in range(DoctorsNumber):
                if DoctorLoad[NewDoctor] <DoctorCapacities[NewDoctor]:
                    Schedule[i]= NewDoctor
                    DoctorLoad[NewDoctor]+= 1
                    break
    return Schedule

def GeneticAlgorithm(PatientsNumber, DoctorsNumber, DoctorCapacities, Generations=100, PopulationSize=50):
    TotalCapacity =sum(DoctorCapacities)
    if PatientsNumber> TotalCapacity:
        UnscheduledPatients =list(range(TotalCapacity, PatientsNumber))
        PatientsNumber =TotalCapacity
    else:
        UnscheduledPatients= []
    BestSchedule=[random.randint(0, DoctorsNumber - 1) for _ in range(PatientsNumber)]
    BestSchedule=EnforceCapacity(BestSchedule, DoctorsNumber, DoctorCapacities)
    Population = []
    for _ in range(PopulationSize):
        Schedule = [random.randint(0, DoctorsNumber - 1) for _ in range(PatientsNumber)]
        Schedule= EnforceCapacity(Schedule, DoctorsNumber, DoctorCapacities)
        Population.append(Schedule)
    for Generation in range(Generations):
        FitnessScore= []
        for Individual in Population:
            FitnessScore.append(Fitness(Individual, DoctorsNumber, DoctorCapacities))
        Best = FitnessScore.index(max(FitnessScore))
        BestSchedule =Population[Best]
        if FitnessScore[Best] == 0:
            break
        NewPopulation= []
        for _ in range(PopulationSize// 2):
            Parent1, Parent2 = random.choices(Population, weights=FitnessScore, k=2)
            CrossoverPoint = random.randint(1, PatientsNumber- 1)
            Child1=Parent1[:CrossoverPoint]+Parent2[CrossoverPoint:]
            Child2=Parent2[:CrossoverPoint]+Parent1[CrossoverPoint:]
            if random.random()< 0.1:
                Child1[random.randint(0,PatientsNumber- 1)] =random.randint(0 , DoctorsNumber- 1)
            if random.random()< 0.1:
                Child2[random.randint(0,PatientsNumber- 1)] =random.randint(0 , DoctorsNumber- 1)
            Child1=EnforceCapacity(Child1, DoctorsNumber, DoctorCapacities)
            Child2=EnforceCapacity(Child2, DoctorsNumber, DoctorCapacities)
            NewPopulation.extend([Child1, Child2])
        Population= NewPopulation
    return BestSchedule, UnscheduledPatients
