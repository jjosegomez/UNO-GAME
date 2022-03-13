from uno import *

class Group23Human(UnoPlayer,Deck,PublicGameState):
    def init(self,name):
        UnoPlayer.init(self,name)
        self.name = name


    def choose_card(self,state):
        print(f'Current Top card: {state.get_top_card()}')
        #makes a enumerated list of the player's deck
        print('Your cards!')
        id = 0
        #To choose from list index
        ListChoose = 0

        #PART 1 For implementing SKIP
        if None in self.hand:
            self.hand.remove(None)

        #To print list with id
        for x in self.hand:
            print(f"{id}: {self.hand[ListChoose]}")
            id += 1
            ListChoose += 1

        #PART  For implementing SKIP     
        self.hand.append(None)
        print(str(id)+": Draw a card and skip your turn")
        
        #This code is to print the color when WILD or WILD_DRAW_FOUR is played.
        if state.get_top_card().type == CardType.WILD or state.get_top_card().type == CardType.WILD_DRAW_FOUR:
            if self.color == 0:
                print("Color called, BLUE!")
                state.get_top_card().color = Color.BLUE
                state.get_top_card().type = CardType.WILD
            if self.color == 1:
                print("Color called, GREEN!")
                state.get_top_card().color = Color.GREEN
                state.get_top_card().type = CardType.WILD
            if self.color == 2:
                print("Color called, RED!")
                state.get_top_card().color = Color.RED
                state.get_top_card().type = CardType.WILD
            if self.color == 3:
                print("Color called, YELLOW!")
                state.get_top_card().color = Color.YELLOW
                state.get_top_card().type = CardType.WILD

        #This code prevents choosing a number thats not an option
        self.user_choice = int(input('which card would you like to choose? '))
        while self.user_choice < 0 or  self.user_choice > len(self.hand) - 1:
            self.user_choice = int(input('Choose the number on the left of your card:'))
        self.card = self.hand[self.user_choice]

        #This code is logic for invalid cards
        if self.card == None:
            return None
        
        else:
            if self.card.color == state.get_top_card().color:
                return self.card
            elif self.card.color != state.get_top_card().color and self.card.type == state.get_top_card().type and self.card.number == state.get_top_card().number:
                return self.card
            elif self.card.type == CardType.WILD or self.card.type == CardType.WILD_DRAW_FOUR:
                return self.card
            while self.card.color != state.get_top_card().color or self.card.type != state.get_top_card().type:
                if self.card.color == state.get_top_card().color:
                    return self.card
                print(self.card.color)
                print(state.get_top_card().color)
                print("Illegal move!")
                print(f"Current top card: {state.get_top_card()}")
    # MISSIBG: print the card available to draw.
                self.user_choice = int(input('which card would you like to choose?'))
                self.card = self.hand[self.user_choice]
                if self.card == None:
                    return None

        self.card = self.hand[self.user_choice]
        return self.card
        

    def call_color(self,state):
        self.color = input('What color do you call?(yellow,blue,green,red):')
        self.color.lower()
        if self.color == 'yellow':
            self.color = Color.YELLOW
        if self.color == 'blue':
            self.color = Color.BLUE
        if self.color == 'red':
            self.color = Color.RED
        if self.color == 'green':
            self.color = Color.GREEN
        return self.color
  
