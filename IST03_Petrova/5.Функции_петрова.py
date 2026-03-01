def create_spreadsheet(title, row_count=1000):
    return 'Создание электронной таблицы с именем ' + title + ' with ' + str(row_count) + ' lines'

print(create_spreadsheet('Приложения',10))