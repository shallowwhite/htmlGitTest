import requests
from bs4 import BeautifulSoup
import random

def get_star_wars_characters():
    url = "https://en.wikipedia.org/wiki/List_of_Star_Wars_characters"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extracting character names from the table on the page
        table = soup.find('table', {'class': 'wikitable'})
        rows = table.find_all('tr')[1:]
        characters = [row.find_all('td')[0].text.strip().upper() for row in rows]
        return characters

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def choose_word(characters):
    return random.choice(characters)

def display_word(word, guessed_letters):
    display = ""
    for char in word:
        if char == " " or char in guessed_letters:
            display += char
        else:
            display += "_"
    return display

def hangman():
    print("Welcome to Star Wars Hangman!")
    star_wars_characters = get_star_wars_characters()

    if not star_wars_characters:
        print("Failed to retrieve Star Wars characters. Exiting.")
        return

    word_to_guess = choose_word(star_wars_characters).upper()
    guessed_letters = set()
    attempts = 6

    while attempts > 0:
        print("\nAttempts left:", attempts)
        print(display_word(word_to_guess, guessed_letters))

        guess = input("Guess a letter: ").upper()

        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue

        guessed_letters.add(guess)

        if guess not in word_to_guess:
            attempts -= 1
            print("Incorrect guess!")
        else:
            print("Correct guess!")

        if all(char in guessed_letters or char == " " for char in word_to_guess):
            print("Congratulations! You guessed the word:", word_to_guess)
            break

    if attempts == 0:
        print("Sorry, you ran out of attempts. The correct word was:", word_to_guess)

if __name__ == "__main__":
    hangman()
