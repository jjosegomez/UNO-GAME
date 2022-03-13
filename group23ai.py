from uno import *

class Group23Ai(UnoPlayer,Deck,PublicGameState):
    def init(self,name):
        UnoPlayer.init(self,name)
        self.name = name


    def choose_card(self,state):
        state.get_top_card()

        if state.get_top_card().type == CardType.WILD or state.get_top_card().type == CardType.WILD_DRAW_FOUR:
            if self.card.color == 0:
                state.get_top_card().color = Color.BLUE
            if self.card.color == 1:
                state.get_top_card().color = Color.GREEN
            if self.card.color == 2:
                state.get_top_card().color = Color.RED
            if self.card.color == 3:
                state.get_top_card().color = color.YELLOW
        

        possible_cards = []
        for x in self.hand:
            if x.color == state.get_top_card().color:
                possible_cards.append(x)
##            if x.type == CardType.WILD or x.type == CardType.WILD_DRAW_FOUR:
##                 possible_cards.append(x)
            if x.type == state.get_top_card().type and x.number == state.get_top_card().number:
                possible_cards.append(x)

        print(self.hand)
        print(possible_cards)

        if len(possible_cards) == 0:
            return None
        else:
            return possible_cards[0]


        #To print list with id
        for x in self.hand:
            Index += 1
            print(self.hand)


        #PART  For implementing SKIP
        self.hand.append(None)
        print(str(id)+": Draw a card and skip your turn")




    def call_color(self,state):


        if self.color == 'yellow':
            self.color = Color.YELLOW
        if self.color == 'blue':
            self.color = Color.BLUE
        if self.color == 'red':
            self.color = Color.RED
        if self.color == 'green':
            self.color = Color.GREEN
        return self.color
