from argon2 import PasswordHasher
from getpass import getpass

password = getpass("Enter password: ")
ph = PasswordHasher()
hashed_password = ph.hash(password)

with open("password.txt", "w") as f:
    f.write(hashed_password)
    print("password saved to password.txt")