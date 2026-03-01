
#1
fir = (6*6-1 == 8 + 1)
sec = (13-7 != (3*2)+1)
thir = (3*(2-1) == 4-1)
print("Задание 1:", "1.",fir, "2.",sec, "3.",thir)

#2
a = (6*6-1 >= 8 + 1)
b = (13-7 <= (3*2)+1)
c = (3*(2-1) > 4-1)
print("Задание 2:", "1.",a, "2.",b, "3.",c)

#3
bool_variable = "true"
print("Задание 3:")
print(type(bool_variable)) #-> строка, поэтому и не логическая. Не имеет значений T/F
bool_variable_2 = True
print(type(bool_variable_2)) #-> лог переменная

#4
user_name = input('Введите имя:')
if user_name == 'Дмитрий':
    print('Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!')
else:
    print("Добро пожаловать")

enter_number = 1
passw = 'network'
while enter_number <= 3:
    m = input('Введите пароль:')
    if m != passw:
        if enter_number == 3:
            print('Вы превысили максимальное число попыток. Ваша учетная запись заблокирована. Для разблокировки обратитеь в службу поддержки.')
            break
        print("Попробуйте еще раз, у вас осталось", 3-enter_number, 'попыток.')
        enter_number += 1
    else:
        print('Добро пожаловать!')
        break
#5
statement_one = ((2+2+2 >= 6) and (-1 * -1 < 0))
statement_two = ((4*2 <= 8) and (7 - 1 == 6))
print(statement_one, statement_two)


#6
fir = ((2-1 >3) or (-5*2 == -10))
sec = ((9 + 5 <= 15) or (7 != 4+3))
print(fir,sec)

#7
grade = float(input('Введите балл:'))
if grade >= 4.0:
    print('A')
elif 4 > grade >= 3:
    print('B')
elif 3 > grade >= 2:
    print('C')
elif 2 > grade >= 1:
    print('D')
else:
    print('F')
