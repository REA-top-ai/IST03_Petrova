#1
import datetime

current_time = datetime.datetime.now()
print(current_time)

#2
import random
random_list = [random.randint(1, 100) for i in range(101)]
randomer_number = random.choice(random_list)
print(randomer_number)

#3
import matplotlib.pyplot as plt
import random

number_a = range(1, 13)
number_b = [random.randint(0, 1000) for i in range(12)]
plt.plot(number_a, number_b)
plt.show()

#4
employees = [
    {"ФИО": "Иванов Иван Иванович", "Должность": "Менеджер", "Дата найма": "22.10.2013", "Оклад": 250000, "Пол": "М"},
    {"ФИО": "Сорокина Екатерина Матвеевна", "Должность": "Аналитик", "Дата найма": "12.03.2020", "Оклад": 75000, "Пол": "Ж"},
    {"ФИО": "Струков Иван Сергеевич", "Должность": "Старший программист", "Дата найма": "23.04.2012", "Оклад": 150000, "Пол": "М"},
    {"ФИО": "Корнеева Анна Игоревна", "Должность": "Ведущий программист", "Дата найма": "22.02.2015", "Оклад": 120000, "Пол": "Ж"},
    {"ФИО": "Старчиков Сергей Анатольевич", "Должность": "Младший программист", "Дата найма": "12.11.2021", "Оклад": 50000, "Пол": "М"},
    {"ФИО": "Бутенко Артем Андреевич", "Должность": "Архитектор", "Дата найма": "12.02.2010", "Оклад": 200000, "Пол": "М"},
    {"ФИО": "Савченко Алина Сергеевна", "Должность": "Старший аналитик", "Дата найма": "13.04.2016", "Оклад": 100000, "Пол": "Ж"}
]

from datetime import datetime
now = datetime.now()

def get_exp(date):
    return (now - datetime.strptime(date, "%d.%m.%Y")).days / 365

print("Премия программистам:")
for e in employees:
    if "программист" in e["Должность"].lower():
        print(f"{e['ФИО']}: {e['Оклад']*0.03:.0f} руб.")

print("Премии к 8 марта и 23 февраля:")
for e in employees:
    print(f"{e['ФИО']}: 2000 руб. ({'8 марта' if e['Пол']=='Ж' else '23 февраля'})")

print("Индексация:")
for e in employees:
    proc = 7 if get_exp(e["Дата найма"]) > 10 else 5
    print(f"{e['ФИО']}: +{e['Оклад']*proc/100:.0f} руб. ({proc}%)")

print("К отпуску:")
for e in employees:
    if get_exp(e["Дата найма"]) > 0.5:
        print(f"Да{e['ФИО']}")

#5
import random

user_numbers = [123, 45, 678, 91, 234, 567, 890, 12, 345, 678, 901, 234, 567, 890, 123, 456, 789, 987, 654, 321]
secret_number = random.randint(1, 9)
print(f"Загаданное число: {secret_number}")

print("Выигрышные номера:")
count = 0

for num in user_numbers:
    digit_sum = sum(int(d) for d in str(abs(num)))
    if digit_sum % secret_number == 0:
        print(f"  {num} (сумма цифр: {digit_sum})")
        count += 1
        if count >= 5:
            print("Достигнуто максимальное количество победителей!")
            break
if count == 0:
    print("Выигрышных номеров нет")