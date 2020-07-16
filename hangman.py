""" Hangman Game

This simulates a simple hangman game

Features
1. Select your topic of interest
2. Word definition after the word has been guessed.


"""
import os
import pprint
import random
from typing import List
import string

from requests import RequestException

HANGMAN_IMAGE = [
    '''
   +---+
       |
       |
       |
      ===
''',
    '''
   +---+
   O   |
       |
       |
      ===
''',
    '''
   +---+
   O   |
   |   |
       |
      ===
''',
    '''
   +---+
   O   |
  /|   |
       |
      ===
''',
    '''
   +---+
   O   |
  /|\  |
       |
      ===
''',
    '''
   +---+
   O   |
  /|\  |
  /    |
      ===
''',
    '''
   +---+
   O   |
  /|\  |
  / \  |
      ===
''']

from PyDictionary import PyDictionary
import requests


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.guessed_letters = []
        self.correct_letters = []
        self.missed_letters = []

    def set_as_won(self):
        self.score += 1

    def count_missed_letters(self):
        return len(self.missed_letters)

    def refresh(self):
        self.guessed_letters = []
        self.correct_letters = []
        self.missed_letters = []


class WordSource:
    SOURCE_API = 'https://api.datamuse.com/words'

    @classmethod
    def get_words(cls, topic):
        """
        Fetches a wordlist for the game based on a topic of interest
        :param topic:
        :return: List of words
        """
        params = dict(
            topics=topic,
            max=100
        )
        try:
            response = requests.get(
                url=WordSource.SOURCE_API,
                params=params
            )
            if response.ok:
                data = response.json()
                # List comprehension to just extract the single words from the dictionary
                word_list = [item['word'] for item in data if " " not in item['word']]
                return word_list
            else:
                print("Error fetching words.")
                return []

        except RequestException as e:
            print(f'Error {e}')


class Hangman:
    """
********************************************
                HANGMAN GAME
            Simple hangman game
Adapted from Invent with python
Written by Azeem Animashaun 2020
********************************************
   +---+
   O   |
  /|\  |
  / \  |
    ===

Features
1. Multiplayer support
1. Select your topic of interest e.g Words relating o music,sports , etc..
2. Word definition after the game
    """

    def __init__(self, players: List[Player], words, rounds):
        self.players = players
        self.current_player = players[0]
        self.number_of_rounds = rounds
        self.word_list = words
        self.correct_word = ''

    def get_random_word(self):
        # This function returns a random string from the passed list of strings.
        random_index = random.randint(0, len(self.word_list) - 1)
        return self.word_list.pop(random_index)

    def display_board(self):
        print(f"{self.current_player.name}'s Turn")
        # Display the hangman images based on the list index
        print(HANGMAN_IMAGE[self.current_player.count_missed_letters()])
        print('Missed letters:', end=' ')
        for letter in self.current_player.missed_letters:
            print(letter, end=' ')
        print('\n')
        blanks = '_' * len(self.correct_word)
        for i in range(len(self.correct_word)):  # Replace blanks with correctly guessed letters.
            if self.correct_word[i] in self.current_player.correct_letters:
                blanks = blanks[:i] + self.correct_word[i] + blanks[i + 1:]

        for letter in blanks:  # Show the secret word with spaces in between each letter.
            print(letter, end=' ')
        print()

    def add_correct_letter(self, letter):
        self.current_player.correct_letters.append(letter)

    def add_missed_letter(self, letter):
        self.current_player.missed_letters.append(letter)

    def add_guessed_letter(self, letter):
        self.current_player.guessed_letters.append(letter)

    def get_guess(self):
        # Returns the letter the player entered. This function makes sure the player entered a single  letter and not
        # something else.
        while True:
            print(' Guess a letter.')
            guess = input()
            guess = guess.lower()
            if len(guess) != 1:
                print(' Please enter a single letter.')
            elif guess in self.current_player.guessed_letters:
                print(' You have already guessed that letter. Choose again.')
            elif guess not in string.ascii_letters:
                print(' Please enter a LETTER.')
            else:
                return guess

    def start(self):
        for current_round in range(1, self.number_of_rounds + 1):
            print(f" ROUND {current_round}")
            for player in self.players:
                self.shuffle()
                player.refresh()
                self.current_player = player
                has_won_round = False

                while self.current_player.count_missed_letters() != len(HANGMAN_IMAGE) - 1:
                    # Player can still guess
                    self.display_board()
                    guess = self.get_guess()
                    self.add_guessed_letter(guess)
                    # letter is a valid
                    if guess in self.correct_word:
                        self.add_correct_letter(guess)
                        # Check if the player has won.
                        difference = set(self.correct_word) - set(self.current_player.guessed_letters)
                        if not difference:
                            has_won_round = True
                            self.current_player.set_as_won()
                            print(f" WON: {player.name} has won round {current_round}")
                            print(f" SECRET WORD : {self.correct_word}")
                            self.print_word_definition()
                            break
                    else:
                        # Player missed count increases
                        self.add_missed_letter(guess)
                    os.system('clear')

                if not has_won_round:
                    # Player has guessed too many times and lost.
                    print('You have ran out of guesses! ')
                    print(f'After {self.current_player.count_missed_letters()} missed guesses')
                    print(f'SECRET WORD {self.correct_word}')
                    self.print_word_definition()

                if current_round != self.number_of_rounds:
                    input('Next Player turn, Press any key to continue')
                os.system('clear')
        # Prints  Results
        print("Results:  ")
        for player in players:
            print(f"{player.name}= {player.score}")
        input("...")

    def shuffle(self):
        # Set a new word for the next player
        self.correct_word = self.get_random_word()

    def print_word_definition(self):
        meaning = PyDictionary().meaning(self.correct_word)
        if meaning:
            print('DEFINITION')
            pprint.pprint(meaning)

        else:
            print('Error fetching definition ')
        print("*" * 20)
        input("...")



def get_user_input(text, data_type=None):
    """
    Get input from console and parse correctly
    :param text:
    :param data_type:
    :return: any
    """
    while True:
        if data_type:
            value = data_type(input(text))

        else:
            value = eval(input(text))

        return value


while True:

    print(Hangman.__doc__)

    number_of_rounds = get_user_input("Number of rounds: ", int)

    if number_of_rounds <= 0:
        print("Rounds must be greater than 1")
        break

    number_of_players = get_user_input('Number of players: ', int)
    if number_of_players <= 0:
        print("Players must be greater than 1")
        break

    words = None
    while not words:
        topic_of_interest = get_user_input('Category of interest? (Music, Fashion, Sports, Comedy, etc): ', str)
        words = WordSource.get_words(topic_of_interest)
        if not words:
            print(f"No word list matching category:{topic_of_interest}")

    players = [Player(f"Player {count}") for count in range(1, number_of_players + 1)]
    game = Hangman(players, words, number_of_rounds)
    game.start()
