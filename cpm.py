class Task:
    name = None
    duration = 0
    early_start = 0
    early_finish = 0
    late_start = 0
    late_finish = 0
    slack = 0
    is_critical = None
    dependencies = []

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.dependencies = []
        self.is_critical = False

    def add_dependency(self, dependency):
        self.dependencies.append(dependency)


class Cpm:
    def get_input(self,tasks):
        no_of_task = int(input("Enter no. of task"))

        for i in range(no_of_task):
            name = input("Enter name of the task : ")
            duration = int(input("\nEnter duration of the task : "))
            dependency_names = str(input("\nEnter dependency of the task : "))

            list_of_dependency = dependency_names.split(',')

            add_task = Task(name.strip(), duration)
            tasks.append(add_task)

            # print("list : ",list_of_dependency)

            if i == 0:
                continue

            dependency_found = False

            for name_dependency in list_of_dependency:
                if not name_dependency.strip():
                    return print("dep should not be empty")
                else:
                    for task in tasks:
                        if task.name == name_dependency.strip():
                            add_task.add_dependency(task)
                            dependency_found = True

                    if not dependency_found:
                        print("Task does not exist")

    def display_tasks(self,tasks):
        for task in tasks:
            print("\n\nname : ",task.name)
            print("duration : ",task.duration)
            print("Early_start : ",task.early_start)
            print("Early_finish : ",task.early_finish)
            print("Late_start :",task.late_start)
            print("Late_finish :",task.late_finish)
            print("SLACK TIME : ",task.slack)
            for name in task.dependencies:
                print(name.name, end = "  ")


    def calculateCPM(self, tasks):       
        tasks[0].early_start = 0
        tasks[0].early_finish = tasks[0].duration
        max_finish_time = 0

        for j in range(1, len(tasks)):
            current_task = tasks[j]

            for task_dependency in current_task.dependencies:
                max_finish_time = max(max_finish_time, task_dependency.early_finish)

            current_task.early_start = max_finish_time
            current_task.early_finish = max_finish_time + current_task.duration

        
        last_task = tasks[len(tasks)-1]
        last_task.late_finish = last_task.early_finish
        last_task.late_start = last_task.late_finish - last_task.duration


        
# Backward Pass
        for k in range(len(tasks)-2, -1 , -1):
            current_task = tasks[k]
            check_late_finish = 0

            for search_task in tasks:
                if current_task in search_task.dependencies:
                        if current_task.late_finish == 0:   
                                current_task.late_finish = search_task.late_start
                                current_task.late_start = current_task.late_finish - current_task.duration                       
                                print("hello loop",current_task.name)
                        else:
                                check_late_finish = search_task.late_start
                                current_task.late_finish = min(current_task.late_finish,check_late_finish)
                                current_task.late_start = current_task.late_finish - current_task.duration


            
            current_task.slack = current_task.late_finish - current_task.early_finish

            if(current_task.slack == 0):
                 current_task.is_critical = True
                                

c = Cpm()
tasks = []
c.get_input(tasks=tasks)
c.calculateCPM(tasks = tasks)
c.display_tasks(tasks)
