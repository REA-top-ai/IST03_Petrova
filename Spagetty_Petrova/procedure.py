def add_money(amout, client, client_balance):
    client_balance += amout
    print(f"Client {client} add {amout}. Balance is {client_balance}")
    return client_balance
def payment(amout, client, client_balance):
    if client_balance >= amout:
        client_balance -= amout
        print(f"Client {client} pay {amout}. Balance is {client_balance}")
    else:
        print(f"Not enought money. Balance is {client_balance}")
    return client_balance
if __name__ == "__main__":
    client1 = "Alice"
    client1_balance = 1000
    client2 = "Bob"
    client2_balance = 500
    client1_balance = add_money(200, client1, client1_balance)
    client2_balance = add_money(300, client2, client2_balance)
    client1_balance = payment(300, client1, client1_balance)
    client2_balance = payment(200, client2, client2_balance)