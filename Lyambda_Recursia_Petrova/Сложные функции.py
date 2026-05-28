tables = {
    1: {
        'name': 'Jiho',
        'vip_status': False,
        'order': ('Orange Juice', 'Apple Juice')
    },
    2: {},
    3: {},
    4: {},
    5: {},
    6: {},
    7: {},
}
def assign_table(table_num, name, *order, vip_status=False, ):
    keys = ['name', 'vip_status']
    tables[table_num] = {key: value for key, value in zip(keys, [name, vip_status])}
    return tables


assign_table(6, 'Yohi', vip_status=False)
assign_table(4, "Karla")

def assign_and_print_order(table_num, *order_items):
    if 'order' not in tables[table_num]:
        tables[table_num]['order'] = ()
    if not tables[table_num]['order']:
        tables[table_num]['order'] = order_items
    for i in tables[table_num]['order']:
        print(i)


assign_and_print_order(1)

assign_table(2, 'Arwa', vip_status=True)
assign_and_print_order(2, 'Стейк', 'Морской окунь', 'Бутылка вина')

print(tables)