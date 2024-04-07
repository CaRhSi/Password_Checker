import hashlib
import requests
import argparse


def password_hash(password):
    hpass = hashlib.sha1(password.encode())
    textPass = hpass.hexdigest()
    return textPass


def API_check(password):
    print('Checking...')
    link = ('https://api.pwnedpasswords.com/range/' + password[:5])
    headers = {'Add-Padding': 'true'}
    response = requests.get(link, headers=headers)
    response_text = response.text
    response_text_lines = response_text.splitlines()
    for i in range(len(response_text_lines)):
        item = response_text_lines[i]
        if item[:35].lower() == password[5:]:
            return item[36:]
    return False

def main():
    parser = argparse.ArgumentParser(description='Checks if your password has been in a data breach')
    parser.add_argument('--show-hash', nargs='?', const=True, help='Show hash value')
    args = parser.parse_args()

    while True:
        password = input("Enter your password (or 'exit' to quit): ")
        if password == 'exit':
            print('Goodbye!')
            break
        hashed = password_hash(password)
        if args.show_hash is not None:
            print('Your hashed password is', hashed)
        result = API_check(hashed)
        if result == False:
            print("Good news! Your password hasn't been pwned.")
        else:
            print('Your password has been pwned! The password "' + password + '" appears ' + str(result) + ' times in data breaches.')


if __name__ == "__main__":
    main()