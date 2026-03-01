#1
board_games = ['Settlers of Catan', 'Carcassone', 'Power Grid', 'Agricola', 'Scrabble']
sport_games = ['football', 'football - American', 'hockey', 'baseball', 'cricket']

print("НАСТОЛЬНЫЕ ИГРЫ")
for game in board_games:
    print(game)

print("ВИДЫ СПОРТА")
for sport in sport_games:
    print(sport)

#2
promise = "I will not chew gum in class"
for i in range(5):
    print(promise)

#3
students_period_A = ["Alex", "Briana", "Cheri", "Daniele"]
students_period_B = ["Dora", "Minerva", "Alexa", "Obie"]

print("ОБЪЕДИНЕНИЕ СПИСКОВ")

print("Исходные списки:")
print(f"students_period_A: {students_period_A}")
print(f"students_period_B: {students_period_B}")
print()

print("Добавляем студентов из A в B:")
for student in students_period_A:
    students_period_B.append(student)
    print(f"  Добавлен: {student}")

print(f"Результат:")
print(f"students_period_B: {students_period_B}")
print(f"Длина students_period_B: {len(students_period_B)}")

#4
dog_breeds_available_for_adoption = ['french_bulldog', 'dalmatian', 'shihtzu', 'poodle', 'collie']
dog_breed_I_want = 'dalmatian'

for breed in dog_breeds_available_for_adoption:
    print(breed)
    if breed == dog_breed_I_want:
        print("У них есть собака, которую я хочу!")
        break

#5
sales_data = [[12, 17, 22], [2, 10, 3], [5, 12, 13]]
scoops_sold = 0

for store in sales_data:
    for scoops in store:
        scoops_sold += scoops

print(scoops_sold)
