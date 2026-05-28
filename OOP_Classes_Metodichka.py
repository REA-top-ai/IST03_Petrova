#Наследование
class Employee:
    new_id = 1

    def __init__(self):
        self.id = Employee.new_id
        Employee.new_id += 1

    def say_id(self):
        print(f"My id is {self.id}")

e1 = Employee()
e2 = Employee()
e1.say_id()
e2.say_id()

class Admin(Employee):
    pass

e3 = Admin()
e3.say_id()

#Задание на super()
class Admin(Employee):
    def say_id(self):
        super().say_id()
        print("I am an Admin")

e3 = Admin()
e3.say_id()

#Множественное наследование часть 1
class Manager(Admin):
    def say_id(self):
        print("I am in charge")
        super().say_id()

e4 = Manager()
e4.say_id()


#Абстракция
from abc import ABC, abstractmethod

class AbstractEmployee(ABC):
    new_id = 1

    def __init__(self):
        self.id = AbstractEmployee.new_id
        AbstractEmployee.new_id += 1

    @abstractmethod
    def say_id(self):
        pass

class Employee(AbstractEmployee):
    def say_id(self):
        print(f"ID: {self.id}")

e1 = Employee()
e1.say_id()

#инкапсуляция
class Employee:
    def __init__(self):
        self.id = 1
        self._id = 100
        self.__id = 200

e = dir(Employee())
print(e)

#геттеры, сеттеры, делитеры
class Employee:
    def __init__(self, name=None):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, name_string):
        self._name = name_string

    def del_name(self):
        del self._name