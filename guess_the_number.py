import random

# Computer randomly selects a number between 1 and 10
secret_number = random.randint(1, 10)
score = 100  # Start with 100 points 

print("Welcome to the game Guess the Number!")
print("I'm thinking about a number between 1 and 10. Can you guess which it is?")

while True:
    try_ = int(input("Add your number: "))

    if try_ < secret_number:
        print("Too low. Try again.")
        score -= 10  # Lose 10 points
    elif try_ > secret_number:
        print("Too high. Try again.")    
        score -= 10  # Lose 10 points
    else:
        print("Congratulations! You have guessed the number.")
        print(f"Your final score is: {score} points!")
        break  # Exit the loop when the player guesses correctly
