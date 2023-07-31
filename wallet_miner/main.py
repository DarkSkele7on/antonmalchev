import secrets
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import bitcoin

def generate_btc_private_key():
    return secrets.token_bytes(32)

def check_balance(btc_address):
    api_url = f'https://blockstream.info/api/address/{btc_address}/utxo'
    max_retries = 5
    retry_delay = 5  # seconds

    for retry in range(max_retries):
        try:
            response = requests.get(api_url)
            if response.status_code == 429:
                print(f"Rate limited. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
                continue

            response.raise_for_status()
            data = response.json()
            balance = sum(utxo['value'] for utxo in data) / 100000000.0
            return balance
        except requests.RequestException as e:
            print(f"Failed to check balance for address: {btc_address}. Error: {e}")
            return 0

    print(f"Max retries exceeded. Could not check balance for address: {btc_address}")
    return 0

def process_address(attempt):
    btc_private_key = generate_btc_private_key()
    btc_address = bitcoin.privkey_to_address(btc_private_key)
    balance = check_balance(btc_address)

    print(f"Wallet {attempt}")
    print(f"Private Key: {btc_private_key.hex()}")
    print(f"Address: {btc_address}")
    print(f"Balance: {balance} BTC\n")

    return attempt, btc_private_key, btc_address, balance

def main():
    max_attempts = 10000
    found = False

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_address, attempt) for attempt in range(1, max_attempts + 1)]

        for future in as_completed(futures):
            attempt, btc_private_key, btc_address, balance = future.result()

            if balance > 0:
                with open('btc_addresses_with_balance.txt', 'w') as file:
                    file.write(f"Wallet {attempt}\n")
                    file.write(f"Private Key: {btc_private_key.hex()}\n")
                    file.write(f"Address: {btc_address}\n")
                    file.write(f"Balance: {balance} BTC\n")
                    file.write("\n")
                found = True
                break

    if not found:
        print("No address with a balance found.")

if __name__ == "__main__":
    main()
