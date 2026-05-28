from abc import ABC, abstractmethod
class BankAccount(ABC):
    @abstractmethod
    def add_money(self,amout):
        pass
    @abstractmethod
    def payment(self,amout):
        self.add_money(amout)
        pass
class DepositBankAccount(BankAccount):
    def __init__(self, name):
        self.__name = name
        self.__balance = 0
    def add_money(self,amout):
        self.__balance += amout
        print(f"Client {self.__name} add {amout}. Balance is {self.__balance}")
    def payment(self,amout):
        if self.__balance >= amout:
            self.__balance -= amout
            print(f"Client {self.__name} pay {amout}. Balance is {self.__balance}")
        else:
            print(f"Not enought money. Balance is {self.__balance}")
class Client:
    def __init__(self,name):
        self.name = name
        self.balance = []
    def create_account(self,bank_id):
        new_account = DepositBankAccount(self.name,bank_id)
        self.account.append(new_account)