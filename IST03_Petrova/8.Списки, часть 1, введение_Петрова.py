#1
products = ["торт", 1]
print(products)

#2
household_chemicals = [["стиральный порошок", 1],["средство для мытья посуды", 1]]
print(household_chemicals)

#3
Names = ['Ben', 'Holly', 'Ann']
dogs_names = ['Sharik', 'Gab', 'Beethoven']

names_and_dogs_names = zip(Names, dogs_names)

list_of_names_and_dogs_names = list(names_and_dogs_names)
print(list_of_names_and_dogs_names)

#4
orders = ['маргаритки', 'васильки']
print("Начальные заказы:", orders)

orders.append('тюльпаны')
print("После добавления тюльпанов:", orders)

orders.append('розы')
print("После добавления роз:", orders)

print("\nВсе заказы, которые получила Мария сегодня:")
print(orders)

#5
orders = ['маргаритка', 'лютик', 'львиный зев', 'гардения', 'лилия']
new_orders = orders + ['сирень', 'ирис']
print("Обновленный список заказов:", new_orders)

broken_prices = [5, 3, 4, 5, 4] + [4]
print("Исправленный broken_prices:", broken_prices)

#6
list1 = range(0, 9)
print("list1:", list(list1))

list2 = range(0, 8)
print("list2:", list(list2))

#7
list1 = range(5, 16, 3)
print("list1:", list(list1))

list2 = range(0, 40, 5)
print("list2:", list(list2))

