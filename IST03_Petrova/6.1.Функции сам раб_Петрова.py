# 1
def f_to_c(f_temp):
    c_temp = (f_temp - 32) * 5 / 9
    return c_temp


f100_in_celsius = f_to_c(100)
print(f"100°F = {f100_in_celsius:.2f}°C")


def c_to_f(c_temp):
    f_temp = c_temp * 9 / 5 + 32
    return f_temp


c0_in_fahrenheit = c_to_f(0)
print(f"0°C = {c0_in_fahrenheit:.2f}°F")


# 2
def get_force(mass, acceleration):
    return mass * acceleration


train_mass = 22680
train_acceleration = 10
train_distance = 100
train_force = get_force(train_mass, train_acceleration)
print(f"Сила поезда: {train_force}")

print(f"Поезд GE поставляет {train_force} ньютонов силы")


def get_energy(mass, c=3 * 10 ** 8):
    return mass * c ** 2


bomb_mass = 1
bomb_energy = get_energy(bomb_mass)
print(f"\nЭнергия бомбы: {bomb_energy}")

print(f"1 кг бомбы составляет {bomb_energy} Джоулей")


def get_work(mass, acceleration, distance):
    force = get_force(mass, acceleration)
    work = force * distance
    return work


train_work = get_work(train_mass, train_acceleration, train_distance)
print(f"\nРабота поезда: {train_work}")

print(f"Поезд выполняет {train_work} Джоулей за {train_distance} метров.")


# 3
def clothes_preferences():
    clothes = "домашняя одежда"

    print("У меня большой гардероб")
    print(f"Утром лучше всего подходит {clothes}")
    print(f"Днём лучше всего подходит {clothes}")
    print(f"Вечером лучше всего подходит {clothes}")
    print(f"Ночью лучше всего подходит {clothes}")


def meal_preferences():
    meal = "домашняя еда"

    print("\nмои предпочтения в еде")
    print(f"На завтрак лучше всего подходит {meal}")
    print(f"На обед лучше всего подходит {meal}")
    print(f"На ужин лучше всего подходит {meal}")


clothes_preferences()
meal_preferences()


# 4
def security_check(username, arm_number):
    db = {"Дмитрий": 1, "Ангелина": 2, "Василий": 3, "Екатерина": 4}
    if username not in db:
        print("Пользователь не найден")
        return
    if db[username] == arm_number:
        print("Добро пожаловать!")
    elif username == "Дмитрий":
        print("Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!")
    else:
        print("Логин или пароль не верный, попробуйте еще раз")


security_check("Дмитрий", 2)
security_check("Ангелина", 2)

#5
def get_grade(score):
    if score >= 4.0:
        return "A"
    elif score >= 3.0:
        return "B"
    elif score >= 2.0:
        return "C"
    elif score >= 1.0:
        return "D"
    else:
        return "F"

student_score = float(input("Введите средний балл студента: "))
grade = get_grade(student_score)
print(f"Средний балл: {grade}")