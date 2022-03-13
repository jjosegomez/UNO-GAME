from enum import IntEnum, auto
from random import Random

# Card colors
class Color (IntEnum):
  BLUE = 0
  GREEN = 1
  RED = 2
  YELLOW = 3
  NONE = 4 # e.g., Wild

# Card types
class CardType (IntEnum):
  NUMBER = 0 # no special effect
  REVERSE = 1
  SKIP = 2
  DRAW_TWO = 3
  WILD = 4
  WILD_DRAW_FOUR = 5

# Class representing a card in Uno
# All cards have a type, most have a color, and many have a number
class Card:
  def __init__(self, color, type, num = -1):
    self.color = color
    self.type = type
    self.number = num
  
  # Returns whether this card is wild
  def is_wild(self):
    return self.type == CardType.WILD or self.type == CardType.WILD_DRAW_FOUR

  # Returns type
  def get_type(self):
    return self.type

  # Returns number (if type == NUMBER)
  def get_number(self):
    return self.number

  # Returns color (NONE if wild)
  def get_color(self):
    return self.color

  # Print this card
  def __str__(self):
    if self.color == Color.NONE:
      return f"{self.type.name.replace('_', ' ')}"
    elif self.type == CardType.NUMBER:
      return f"{self.color.name} {self.number}"
    else:
      return f"{self.color.name} {self.type.name.replace('_', ' ')}"
  def __repr__(self):
    return self.__str__()

# Class representing a deck of Uno cards
class Deck:
  # Build and shuffle Uno cards
  def __init__(self):
    self.deck = []
    for color in Color:
      if color != Color.NONE:
        # 1 zero of each color
        self.deck.append(Card(color, CardType.NUMBER, 0))
        # 2 each of 1-9 for each color
        for i in range(1, 10):
          self.deck.append(Card(color, CardType.NUMBER, i))
          self.deck.append(Card(color, CardType.NUMBER, i))
        # 2 of each special card for each color
        for type in [CardType.SKIP, CardType.REVERSE, CardType.DRAW_TWO]:
            self.deck.append(Card(color, type))
            self.deck.append(Card(color, type))
    # 4 wilds and 4 wild draw 4's
    for i in range(4):
      self.deck.append(Card(Color.NONE, CardType.WILD))
      self.deck.append(Card(Color.NONE, CardType.WILD_DRAW_FOUR))
    # Shuffle until top card is not wild
    while self.deck[-1].is_wild():
      self.shuffle()

  # Return number of cards
  def get_size(self):
    return len(self.deck)

  # Shuffle
  def shuffle(self):
    rand = Random()
    rand.shuffle(self.deck)

  # Removes and returns top (last) card
  def draw(self):
    top = self.deck[-1]
    self.deck.pop()
    return top

  # Shuffles discard pile into deck, leaving the top (last) card in the discard
  def shuffle_discard_pile(self, discard):
    self.deck += discard[:-1]
    top = discard[-1]
    discard.clear()
    discard.append(top)
    self.shuffle()

# Class representing the publically available information about a game of Uno
# Stores discard pile (including top card), currently called color (if top card
# is wild), and number of cards each player has
class PublicGameState:
  def __init__(self, discard, color, numcards):
    self.color = color
    self.discard = discard
    self.handsizes = numcards

  # Returns top card on the discard pile
  def get_top_card(self):
    return self.discard[-1]

  # Returns called color (relevant if top card is wild)
  def get_called_color(self):
    return self.color

  # Changes the called color (when playing a wild)
  def set_called_color(self, color):
    self.color = color

  # Returns the discard pile
  def get_discard_pile(self):
    return self.discard

  # Returns hand sizes
  # First entry is next player; last entry is current player
  def get_hand_sizes(self):
    return self.handsizes

  # Rotates the hands when turn ends
  def next_turn(self):
    self.handsizes = [self.handsizes[-1]] + self.handsizes[:-1]

  # Reverses the hands (when Reverse is played)
  # Current player stays at end
  def reverse(self):
    self.handsizes = self.handsizes[:-1:-1] + [self.handsizes[-1]]

  # Called when a player is disqualified
  def disqualify_player(self):
    # Removes current player from hand size
    self.handsizes.pop()
    # Rotate so that next player is current
    self.next_turn()

  # Adjusts hand size of current player
  def draw_cards(self, n = 1):
    self.handsizes[-1] += n

  # Adds card to top of discard pile
  # Adjusts hand size of current player
  # Resets called color
  def play_card(self, card):
    self.handsizes[-1] -= 1
    self.discard.append(card)
    self.color = Color.NONE

# Class to represent an Uno player
# Stores an ID and a hand of cards
class UnoPlayer:
  def __init__(self, name):
    self.name = name
    self.hand = []

  # Returns ID
  def get_name(self):
    return self.name
  
  # Returns # cards in hand
  def get_num_cards(self):
    return len(self.hand)

  # Adds a card to hand
  def add_card(self, card):
    self.hand.append(card)

  # Discards a card (after choosing a legal card to play)
  def remove_card(self, card):
    if card in self.hand:
      self.hand.remove(card)

  # Returns the card that the player wants to play
  # Return None to draw and pass turn
  def choose_card(self, state):
    return None

  # Returns the color that the player wants to declare when a wild is played
  def call_color(self, state):
    return Color.YELLOW


# Class representing a game of Uno
# Keeps track of players, deck, current player, which way play is moving, and
# public game state (discard pile, hand sizes, etc.)
class Uno:
  INITIAL_CARDS_PER_PLAYER = 7
  
  # Creates an Uno game with the given players
  def __init__(self, players):
    # For each player "p", search for class "p" in "p".py and instantiates that class
    self.players = []
    for p in players:
      exec(f'from {p.lower()} import {p}')
      exec(f'self.players.append({p}("{p}"))')
    
    # Shuffle players
    rand = Random()
    rand.shuffle(self.players)

    # Start at first player, going "left"
    self.curr_player = 0
    self.dir_play = 1

    # Initialize deck and deal 7 cards to each player
    self.deck = Deck()
    for i in range(Uno.INITIAL_CARDS_PER_PLAYER):
      for p in self.players:
        p.add_card(self.deck.draw())

    # Flip card from to create initial discard pile
    # Set initial hand sizes to 7
    self.game_state = PublicGameState([self.deck.draw()], Color.NONE, [Uno.INITIAL_CARDS_PER_PLAYER for p in self.players])

  # Plays a game of Uno
  def play(self):
    while True:
      # Prompt current player to play a card 
      player = self.players[self.curr_player]
      card = player.choose_card(self.game_state)

      # Disqualify them if they enter an illegal move
      # Code redacted

      # Draw a card if they pass
      if card == None:
        self.draw(1)
      else:
        # Play the card from their hand
        self.game_state.play_card(card)
        player.remove_card(card)

        # Special effects for non-NUMBER cards
        if card.get_type() == CardType.REVERSE:
          self.reverse()
        elif card.get_type() == CardType.SKIP:
          self.skip()
        elif card.get_type() == CardType.DRAW_TWO:
          self.skip()
          self.draw(2)
        elif card.get_type() == CardType.WILD:
          self.wild()
        elif card.get_type() == CardType.WILD_DRAW_FOUR:
          self.wild()
          self.skip()
          self.draw(4)

        # If current player has no cards, return their name
        if self.player_won():
          return player.get_name()

      # Advance to next player after drawing or playing a card
      self.skip()

  # Returns the top card of the deck
  # Reshuffles discard pile into deck if empty
  def get_card(self):
    if self.deck.get_size() == 0:
      self.deck.shuffle_discard_pile(self.game_state.get_discard_pile())
    if self.deck.get_size() == 0:
      raise Exception("Players have drawn all available cards!")
    return self.deck.draw()

  # Current player draws n cards from deck
  def draw(self, n):
    for i in range(n):
      self.players[self.curr_player].add_card(self.get_card())
    self.game_state.draw_cards(n)

  # Moves to the next player's turn
  def skip(self):
    # Mod ensures index is 0 to (# players - 1)
    self.curr_player = (self.curr_player + self.dir_play) % len(self.players)
    self.game_state.next_turn()

  # Reverses direction of play
  def reverse(self):
    self.dir_play = -self.dir_play
    self.game_state.reverse()

  # Prompts current player to call a color
  # Disqualifies them if they try to call Color.NONE
  def wild(self):
    color = self.players[self.curr_player].call_color(self.game_state)
    if color != Color.NONE:
      self.game_state.set_called_color(color)
    else:
      self.disqualify_player()

  # Disqualifies current player
  # They keep their cards (not shuffled into deck)
  def disqualify_player(self):
    print(f"Player {self.players[self.curr_player].get_name()} disqualified")
    self.players = self.players[:self.curr_player] + self.players[self.curr_player + 1:]
    # Reset current player to 0 if disqualifying last player
    self.curr_player = self.curr_player % len(self.players)
    self.game_state.disqualify_player()

  # Returns whether the current player has won
  def player_won(self):
    if len(self.players[self.curr_player].hand) == 0:
      return True
    # elif len(self.players[self.curr_player].hand) == 1:
    #  print("Uno!")
    else:
      return False

if __name__ == '__main__':
  # Create a game with 2 human players
  players = ['Group23Human','Group23Ai'] # Replace names of players
  game = Uno(players)
  winner = game.play()
  print("{winner} wins!")
