from transaction import TESTNET_URL_OFFICIAL, Account, RestClient, FaucetClient, TESTNET_URL, FAUCET_URL
import random
import threading
import time
import csv

##setup
rest_client = RestClient(TESTNET_URL)
rest_client_official = RestClient(TESTNET_URL_OFFICIAL)
faucet_client = FaucetClient(FAUCET_URL, rest_client)
accounts = []
benchmarks = []

def init_account():
    account = Account()
    faucet_client.fund_account(account.address(), 5000)
    faucet_client.fund_account(account.address(), 5000)
    print(account.address())
    with open('signing_keys.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(account.signing_key.__bytes__())
    accounts.append(account)

def test(index):
    range_var = len(accounts)
    account = accounts[index]
    for i in range(range_var):
        start = time.time()
        to = accounts[i].address()
        if account.address() != to:
            tx_hash = rest_client.transfer(account, to, 1)
            rest_client.wait_for_transaction(tx_hash)
            end = time.time()
            print("transaction finished", tx_hash, end-start)
            benchmarks.append((tx_hash, start, end ))

if __name__ == "__main__":
    threads = []
    test_users = 1000

    for test_user in range(test_users):
        init_account()

    for i in range(len(accounts)):
        t = threading.Thread(target=test, args = (i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    with open("out.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(benchmarks)