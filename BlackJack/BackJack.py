from random import shuffle


def get_a_deck():
    """Gives us a deck of cards"""
    Deck = []
    for s in ["C", "D", "H", "S"]:
        for v in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            Deck.append("".join([v, s]))
    return Deck


class Deck:
    """Class that Holds Deck information"""

    def __init__(self,
                 deck_size: int = 1,
                 shuffle_n_before: int = -1,
                 auto_add: bool = True):
        """Creates a Deck that will shuffle and deal cards out

        Keyword Arguments:
            deck_size {int} -- How many draw_pile to included (default: {1})
            shuffle_n_before {int} -- How many cards to be left in the deck before 
                                      the draw_pile are shuffled. if -1, will not shuffle
                                      deck and will stop returning cards
                                      (default: {-1})
            auto_add {bool} -- Automatically add drawn cards to the discard pile. 
                               (default: {True})

        Details:
            if shuffle_n_before is greater than zero, it will maintain the order of the
            remaining n cards, shuffle all that have been used, then append the newly
            shuffled cards on the bottum of the draw_pile

            auto_add does something intresting. If True, as cards are drawn, will 
            automatically include them into the discard pile (keeping track of
            what is being drawn if shuffle is turned on). If False, one will have
            to explicitly add them to the discard pile via tthe Discard_Cards function
        """

        self.deck_size = deck_size
        self.shuffle_n_before = shuffle_n_before
        self.auto_add = auto_add

        self.index = 0
        self.draw_count = 0
        self.draw_pile = []
        self.discard_pile = []
        self.inplay_pile = []

        self.Get_draw_pile()
        self.Shuffle_Cards()

    def __next__(self):
        return(self.Draw_Cards())

    def __iter__(self):
        return(self)

    def __len__(self):
        return self.draw_count

    def __getitem__(self, Index: int = 0):
        if Index >= self.draw_count:
            return(None)
        else:
            return(self.draw_pile[Index])

    def __str__(self):
        STR = '\nNumber of draw_pile: {}' 
        STR = STR + '\nNumber of Cards Drawn: {}'  
        STR = STR + '\nNumber of Cards in play: {}' 
        STR = STR + '\nNumber of Remaining Cards: {}' 
        STR = STR.format(self.deck_size,
                         len(self.discard_pile),
                         len(self.inplay_pile),
                         self.draw_count)
        return(STR)

    def Draw_Cards(self,
                  n: int = 1):
        """Draws a card from the top of the deck"""
        drawn_cards = []
        for i in range(n):
            if self.shuffle_n_before < 0 and self.draw_count <= 0:
                break

            elif self.draw_count <= self.shuffle_n_before:
                print("shuffle shuffle shuffle")
                self.Get_draw_pile()
                self.Shuffle_Cards()
            self.draw_count -= 1

            drawn_cards.append(self.draw_pile.pop())
        if self.auto_add:
            self.Discard_Cards(drawn_cards)
        else:
            self.Play_Cards(drawn_cards)

        return(drawn_cards)

    def Peek(self, n: int = None):
        """Peek at the next n cards of the deck"""

        # using copy so that they can't F with the actual deck
        if n is None:
            n = self.draw_count
            
        if n > self.draw_count:
            return(self.draw_pile.copy())
        else:
            return(self.draw_pile[0:n].copy())

    def Get_draw_pile(self):
        """Generates the draw_pile for us to play with"""
        self.draw_pile = get_a_deck() * self.deck_size
        self.draw_count = len(self.draw_pile)
        self.discard_pile = []

    def Discard_Cards(self, cards: list = None):
        """returns cards from the fields into the discard pile
        
        Keyword Arguments:
            cards {list} -- list of cards to discard (default: {None})

        Details:
            if None, will check to see if any cards are in the field,
            and if so, will discard all cards in the field.
        """        
        if cards is None:
            if len(self.inplay_pile) > 0:
                for i in range(len(self.inplay_pile)):
                    self.discard_pile.append(self.inplay_pile.pop())
        else:
            if len(cards) > 0:
                for C in cards:
                    self.discard_pile.append(C)
    
    def Play_Cards(self, cards: list):
        """put cards into play"""
        for C in cards:
            self.inplay_pile.append(C)

    def Shuffle_Cards(self):
        """Shuffles the deck(s)"""
        shuffle(self.discard_pile)

        for C in self.discard_pile:
            self.draw_pile.append(C)
        self.draw_count = len(self.draw_pile)
        self.discard_pile = []
        