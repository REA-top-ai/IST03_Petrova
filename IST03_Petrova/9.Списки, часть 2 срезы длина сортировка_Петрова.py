#1
list1 = range(2, 20, 2)
list1_len = len(list1)
print(f"list1 (шаг 2): {list(list1)}")
print(f"Длина list1: {list1_len}")
print()

list1 = range(2, 20, 3)
list1_len = len(list1)
print(f"list1 (шаг 3): {list(list1)}")
print(f"Длина list1: {list1_len}")

#2
shopping_list = ['яйца', 'масло', 'молоко', 'огурцы', 'сок', 'хлопья']
print(f"Длина списка покупок: {len(shopping_list)}")

last_element = shopping_list[-1]
print(f"Последний элемент (индекс -1): {last_element}")

element5 = shopping_list[5]
print(f"Элемент с индексом 5: {element5}")

print(f"\nelement5: {element5}")
print(f"last_element: {last_element}")
print(f"Они равны? {element5 == last_element}")

#3
suitcase = ['рубашка', 'рубашка', 'брюки', 'брюки', 'пижамы', 'книги']
beginning = suitcase[0:2]
print("beginning (первые 2 элемента):", beginning)
print("Количество элементов в списке suitcase:", len(suitcase))
print()

beginning = suitcase[0:4]
print("beginning (первые 4 элемента):", beginning)
print()

middle = suitcase[2:4]
print("middle (два средних элемента):", middle)

print("\n=== ПОЛНЫЙ АНАЛИЗ СПИСКА ===")
print(f"Весь список suitcase: {suitcase}")
print(f"Длина списка: {len(suitcase)}")
print(f"Индексы элементов: 0, 1, 2, 3, 4, 5")
print()

print("Элементы по индексам:")
for i, item in enumerate(suitcase):
    print(f"  индекс {i}: {item}")

#4
suitcase = ['рубашка', 'футболка', 'носки', 'очки', 'пижама', 'книги']
start = suitcase[0:3]

print("Весь чемодан:", suitcase)
print("Первые 3 элемента (start):", start)

#5
votes = ['Jake', 'Jake', 'Laurie', 'Laurie', 'Laurie', 'Jake', 'Jake', 'Jake', 'Laurie', 'Cassie', 'Cassie', 'Jake', 'Jake', 'Cassie', 'Laurie',
         'Cassie', 'Jake', 'Jake', 'Cassie', 'Laurie']

jake_votes = votes.count('Jake')
print(f"Количество голосов за Jake: {jake_votes}")

#6
addresses = ['221 B Baker St.', '42 Wallaby Way', '12 Grimmauld Place', '742 Evergreen Terrace','1600 Pennsylvania Ave', '10 Downing St.']

print("Сортировка адресов\n")

print("Исходный список адресов:")
print(addresses)
print()

addresses.sort()
print("После сортировки (.sort()):")
print(addresses)
print()

addresses.sort(reverse=True)
print("После сортировки в обратном порядке (.sort(reverse=True)):")
print(addresses)
print()

addresses = ['221 B Baker St.', '42 Wallaby Way', '12 Grimmauld Place', '742 Evergreen Terrace','1600 Pennsylvania Ave', '10 Downing St.']

sorted_addresses = sorted(addresses)
print("Оригинальный список (не изменился):")
print(addresses)
print()
print("Новый отсортированный список (sorted()):")
print(sorted_addresses)

#7
games = ['Portal', 'Minecraft', 'Pacman', 'Tetris', 'The Sims', 'Pokemon']
games_sorted = sorted(games)
print("Исходный список games:")
print(games)
print("Отсортированный список games_sorted:")
print(games_sorted)
print(f"games: {games}")
print(f"games_sorted: {games_sorted}")
print(f"games == games_sorted? {games == games_sorted}")