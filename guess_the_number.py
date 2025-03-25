import random

# La computadora elige un número aleatorio
secret_number = random.randint(1, 10)

print("Welcome to the game Guess the Number!")
print("I'm thinking about a number between 1 and 10. Can you guess which it is?")

while True:
    try_ = int(input("Add your number: "))

    if try_ < secret_number:
        print("Too low. Try again.")
    elif try_ > secret_number:
        print("Too high. Try again.")
    else:
        print("Congratulations! You have guessed the number.")
        break
