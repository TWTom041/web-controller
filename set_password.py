from argon2 import PasswordHasher
from getpass import getpass
import os

dirname = os.path.dirname(__file__)

password = getpass("Enter password: ")
ph = PasswordHasher()
hashed_password = ph.hash(password)

with open(os.path.join(dirname, "password.txt"), "w") as f:
    f.write(hashed_password)
    print("password saved to password.txt")