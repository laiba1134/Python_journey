import random

def guess_number():
    no_to_guess = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    print("Guess the Number (1 to 100)")

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        if guess < 1 or guess > 100:
            print("Please guess within 1 to 100.")
            continue

        attempts += 1

        if guess < no_to_guess:
            print("Too low!")
        elif guess > no_to_guess:
            print("Too high!")
        else:
            print(f"Correct! You guessed it in {attempts} attempts.")
            return

    print(f"Out of attempts! The correct number was {no_to_guess}.")
while True:
    guess_number()
    restart = input("Do you want to restart the game? (yes/no): ").lower()
    if restart != "yes":
        print("Game session ended.")
        break
