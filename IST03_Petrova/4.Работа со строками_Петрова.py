#1
first_name = "Виталий"
last_name = "Красилов"
new_account = last_name[0:5]
temp_password = last_name[2:6]
print(f"Логин: {new_account}")
print(f"Пароль: {temp_password}")

#2
def account_generator(first_name, last_name):
    username = first_name[:3] + last_name[:3]
    return username

first_name = "Виталий"
last_name = "Красилов"

new_account = account_generator(first_name, last_name)
print(f"Новое имя пользователя: {new_account}")

#3
def password_generator(first_name, last_name):
    password = first_name[-3:] + last_name[-3:]
    return password

first_name = "Виталий"
last_name = "Красилов"

t_password = password_generator(first_name, last_name)
print(f"Временный пароль: {t_password}")

#4
company_motto = "Мечты сбываются"
second_to_last = company_motto[-2]
print(f"Предпоследний символ: '{second_to_last}'")

final_word = company_motto[-4:]
print(f"Последние 4 символа: '{final_word}'")

#5
first_name = "Ооб"
last_name = "Дейли"
print(f"Исходное имя: {first_name} {last_name}")

#Исправление имени
fixed_first_name = "Р" + first_name[1:]
print(f"Исправленное имя: {fixed_first_name} {last_name}")

#6
password = "theycallme\"crazy\"91"
print(password)

#7
poem_title = "spring storm"
poem_author = "William Carlos Williams"

poem_title_fixed = poem_title.title()

print(poem_title)
print(poem_title_fixed)