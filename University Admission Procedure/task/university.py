import re


def format_input_data(txt):
    """
    Function that will change given student information into usable format.

    :param (str) txt: Student information containing name, exam scores (physics, chemistry,
                      math, computer science) and students priorities:
                        "Jermine Brunton 84 81 73 92 Physics Engineering Mathematics"

                        Department: Physics     = avg of physics & math score
                                    Chemistry   = chemistry score
                                    Mathematics = math score
                                    Engineering = avg computer science & math score
                                    Biotech     = avg chemistry & physics score
                      This score is overruled when special exam is higher than department exam.


    :return (tuple):  Student info:
                    Name, scores for department of priority, department priority:
                        tuple("Jermine Brunton, tuple(84, 92, 73),
                        tuple("Physics Engineering Mathematics")
    """
    map_dept_index = ("Physics", "Chemistry", "Mathematics",
                      "Engineering", "Biotech")

    pattern = r"(?<=[\D]) (?=\d)|(?<=\d) (?=[\D])"
    name, scores, depts = re.split(pattern, txt, 2)
    depts = depts.split()
    scores_input = tuple(map(float, scores.split()))

    map_score_calculation = ((0, 2), (1, 1), (2, 2), (2, 3), (0, 1))
    scores = [max((scores_input[i] + scores_input[j]) / 2, scores_input[4]) for i, j in map_score_calculation]

    score = []
    for d in depts:
        index_d = map_dept_index.index(d)
        score.append(scores[index_d])

    return name, tuple(depts), tuple(score)


class Department:
    """
    This is a class to register students to a Department.
    """

    def __init__(self, name, max_students):
        """
        Constructor for Department class.

        :param (str) name: Name of department
        :param (int) max_students: Max number of students for department.
        """
        self.name = name
        self.max_students = max_students
        self.accepted_students = []

    def assign_students(self, student_list, prio):
        """
        Method that will add students to self.accepted_students, based on student's score, name
        and max_student allowed to Department.

        If a student is accepted, this method will change Student.assigned_score.

        :param (list) student_list: a list of students (class Student) not assigned.
        :param (int) prio: priority of students choise of department --> Student.depts[x]

        """

        student_list.sort(key=lambda x: (-x.scores[prio], x.name))
        if len(student_list) <= self.max_students:
            i = len(student_list)
        else:
            i = self.max_students

        self.accepted_students.extend(student_list[:i])
        for s in student_list[:i]:
            s.assigned_score = s.scores[prio]

        self.max_students = max(0, self.max_students - len(student_list))

    def __str__(self):
        self.accepted_students.sort(key=lambda x: (-x.assigned_score, x.name))
        student_output = "\n".join(f"{s.name} {s.assigned_score}" for s in self.accepted_students)
        return student_output


class Student:
    """
    This class creates students.
    """
    def __init__(self, name, depts, scores):
        """
        Constructor of Student class.

        :param (str) name: Name of student.
        :param (tuple) depts: Priority of departments. First item has the first priority.
        :param (float) scores: Scores of subjects, first item is score of department first prio.

        self.assigned_score will be changed (float) when student is assigned to a department.

        """
        self.name = name
        self.depts = depts
        self.scores = scores
        self.assigned_score = None


def main():
    max_students_subject = int(input())
    with open("applicant_list_7.txt") as f:
        students = f.readlines()

    student_list = [Student(*format_input_data(s)) for s in students]
    map_departments = ("Biotech", "Chemistry", "Engineering", "Mathematics", "Physics")
    departments = {dep: Department(dep, max_students_subject) for dep in map_departments}

    for prio in range(3):
        s_to_assign = {dep: [] for dep in map_departments}
        not_assigned = [s for s in student_list if not s.assigned_score]

        while not_assigned:
            temp_student = not_assigned.pop()
            s_to_assign[temp_student.depts[prio]].append(temp_student)

        for dep in map_departments:
            departments[dep].assign_students(s_to_assign[dep], prio)

    for dep in map_departments:
        with open(f"{dep}.txt", "w") as f:
            f.write(str(departments[dep]))


if __name__ == "__main__":
    main()
