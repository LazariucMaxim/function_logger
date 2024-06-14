from advanced_logger import logger


path = 'test.log'


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        all_grades = sum(self.grades.values(), [])
        return f'''Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за домашние задание: {sum(all_grades)/len(all_grades)}
Завершенные курсы: {", ".join(self.finished_courses)}'''

    def __lt__(self, other):
        if isinstance(other, Student):
            self_all_grades = sum(self.grades.values(), [])
            self_average_grade = sum(self_all_grades)/len(self_all_grades)
            other_all_grades = sum(other.grades.values(), [])
            other_average_grade = sum(other_all_grades) / len(other_all_grades)
            return self_average_grade < other_average_grade
        print('Not a Student')

    def rate_lecture(self, lecturer, course, grade):
        if all((isinstance(lecturer, Lecturer),
                course in self.courses_in_progress,
                course in lecturer.courses_attached)):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        all_grades = sum(self.grades.values(), [])
        return f'''Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за лекции: {sum(all_grades)/len(all_grades)}'''

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            self_all_grades = sum(self.grades.values(), [])
            self_average_grade = sum(self_all_grades)/len(self_all_grades)
            other_all_grades = sum(other.grades.values(), [])
            other_average_grade = sum(other_all_grades) / len(other_all_grades)
            return self_average_grade < other_average_grade
        print('Not a Lecturer')


class Reviewer(Mentor):
    def __str__(self):
        return f'''Имя: {self.name}
Фамилия: {self.surname}'''

    def rate_homework(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


@logger(path)
def average_grade_of_students_on_the_course(course, students_list):
    all_grades = sum([student.grades[course] for student in students_list], [])
    return sum(all_grades)/len(all_grades)


@logger(path)
def average_grade_of_lecturers_on_the_course(course, lecturers_list):
    all_grades = sum([lecturer.grades[course] for lecturer in lecturers_list], [])
    return sum(all_grades) / len(all_grades)


student1 = Student('Some', 'Body', 'somegender')
student2 = Student('Every', 'Body', 'everygender')

lecturer1 = Lecturer('Lecture', 'Lectureson')
lecturer2 = Lecturer('Lecture', 'Lecturedaughter')

reviewer1 = Reviewer('Name', 'Surname')
reviewer2 = Reviewer('Imya''', 'Familiya')

student1.courses_in_progress.append('Python')
student1.finished_courses.append('Git')
student2.courses_in_progress.append('Python')
student2.finished_courses.append('Java')
lecturer1.courses_attached += ['Python', 'C++']
lecturer2.courses_attached += ['Python', 'Fullstack']
reviewer1.courses_attached += ['Python', 'DevOps']
reviewer2.courses_attached += ['Python', 'Data Science']

for grade in range(1,11):
    student1.rate_lecture(lecturer1, 'Python', grade)
    student1.rate_lecture(lecturer2, 'Python', grade)
    student2.rate_lecture(lecturer1, 'Python', grade)
    student2.rate_lecture(lecturer2, 'Python', grade)
    reviewer1.rate_homework(student1, 'Python', grade)
    reviewer1.rate_homework(student2, 'Python', grade)
    reviewer2.rate_homework(student1, 'Python', grade)
    reviewer2.rate_homework(student2, 'Python', grade)

print(average_grade_of_students_on_the_course('Python', (student1, student2)))
print(average_grade_of_lecturers_on_the_course('Python', (lecturer1, lecturer2)))
