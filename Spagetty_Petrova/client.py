def create_id():
    return int(datetime.now().timestamp()*10000000)
def main():
    client1 = BankAccount("Alice")
    client2 = BankAccount("Bob")
    client1.create_account(create_id)
    client2.create_account(create_id)
    client1.accounts[0].add_money(200)
if __name__ == "__main__":
    main()