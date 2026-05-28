client1 = "Alice"
client1_balance = 1000
client2 = "Bob"
client2_balance = 500
amout = 200
client1_balance += amout
print(f"Client {client1} add {amout}. Balance is {client1_balance}")
amout = 300
client2_balance += amout
print(f"Client {client2} add {amout}. Balance is {client2_balance}")
amout = 200
if client2_balance >= amout:
    client2_balance -= amout
    print(f"Client {client2} pay {amout}. Balance is {client2_balance}")
else:
    print(f"Not enought money. Balance is {client2_balance}")
amout = 300
if client1_balance >= amout:
    client1_balance -= amout
    print(f"Client {client1} pay {amout}. Balance is {client1_balance}")
else:
    print(f"Not enought money. Balance is {client1_balance}")