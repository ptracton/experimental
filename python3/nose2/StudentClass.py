#!/usr/bin/env python3


class Student:

    """
    Simple Student class to demonstrate testing
    """

    def __init__(self, name=None, course=None):
        '''
        constructor
        '''
        self.name = name
        self.course = course
        self.list_of_grades = []
        self.gradeValue = 0
        return

    def addGrade(self, grade=None):
        '''
        Add a grade value to the list of grades
        '''
        if grade is not None:
            self.list_of_grades.append(grade)
        return

    def calculateGrade(self):
        '''
        calculate the student letter grade based on
        the sum of the list_of_grades divided by the length
        of list_of_grades
        '''
        if len(self.list_of_grades):
            sum = 0
            for x in self.list_of_grades:
                sum = sum + x
            self.gradeValue = sum / len(self.list_of_grades)
        else:
            self.gradeValue = 0
        return


class Test_Student:

    def __init__(self):
        pass

    @classmethod
    def setUp(self):
        print("Setup")
        self.empty_student = Student()
        self.phil_student = Student(name="Phil", course="Python")

    @classmethod
    def tearDown(self):
        print("Tear Down")
        del(self.empty_student)
        del(self.phil_student)

    def test_ctor(self):
        '''
        Test constructor method
        '''
        assert self.empty_student.name == None
        assert self.empty_student.course == None
        assert self.empty_student.gradeValue == 0
        assert self.empty_student.list_of_grades == []

        assert self.phil_student.name == "Phil"
        assert self.phil_student.course == "Python"
        assert self.phil_student.gradeValue == 0
        assert self.phil_student.list_of_grades == []

    def test_calculateGrade(self):
        '''
        Test grade calculation method
        '''
        self.phil_student.calculateGrade()
        assert self.phil_student.gradeValue == 0

        self.phil_student.addGrade(90)
        self.phil_student.calculateGrade()
        assert self.phil_student.gradeValue == 90

        self.phil_student.addGrade(80)
        self.phil_student.addGrade(70)
        self.phil_student.addGrade(65)
        self.phil_student.addGrade(100)
        self.phil_student.calculateGrade()
        assert self.phil_student.gradeValue == 81

    def test_addGrade(self):
        '''
        Test adding a grade in
        '''
        self.phil_student.addGrade(90)
        assert self.phil_student.gradeValue == 0
        assert len(self.phil_student.list_of_grades) == 1
        self.phil_student.addGrade(95)
        assert self.phil_student.gradeValue == 0
        assert len(self.phil_student.list_of_grades) == 2


if __name__ == "__main__":
    import nose2 # pragma: no cover        
    import nose2.tools # pragma: no cover        
    nose2.main() # pragma: no cover        
#    nose2.tools.decorators.with_setup(Test_Student.setup)
#    nose2.tools.decorators.with_teardown(Test_Student.teardown)    
