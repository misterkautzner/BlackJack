__author__ = 'John'

import random

# A "deck" with shorthand for each card in a real deck.
fulldeck = ['2C', '2D', '2H', '2S', '3C', '3D', '3H', '3S', '4C', '4D', '4H', '4S', '5C', '5D', '5H', '5S', '6C', '6D',
        '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S', '9C', '9D', '9H', '9S', '10C', '10D', '10H',
        '10S', 'JC', 'JD', 'JH', 'JS', 'QC', 'QD', 'QH', 'QS', 'KC', 'KD', 'KH', 'KS', 'AC', 'AD', 'AH', 'AS']


class Card:  # Gives a shorthand card from fulldeck its attributes.
    def __init__(self, valSuit):  # valSuit is the shorthand for a card, value followed by suit.
        if len(valSuit) == 2:
            if valSuit[0].isdigit():
                self.value = int(valSuit[0])
                self.face = valSuit[0]
            else:
                if valSuit[0] == 'A':
                    self.value = 11    # value is the numeric value of the card, used to calculate hand value
                    self.face = "Ace"  # face is what the card is called so the player knows what's in his hand
                else:
                    self.value = 10
                    if valSuit[0] == 'J':
                        self.face = 'Jack'
                    elif valSuit[0] == 'Q':
                        self.face = "Queen"
                    else:
                        self.face = "King"

        else:
            self.value = int(valSuit[0:2])
            self.face = str(self.value)
        suits = {'C':"Clubs", 'D':"Diamonds", 'H':"Hearts", 'S':"Spades"}  # Suit tells the player the suit of the card
        self.suit = suits[valSuit[-1]]
    def __str__(self):
        return self.face + " of " + str(self.suit)
    def getValue(self):
        return self.value
    def getSuit(self):
        return self.suit

def show(list):  # Shows the player's or dealer's current hand
    if len(list) == 1:
        return list[0]
    elif len(list) == 2:
        return str(list[0]) + " and " + str(list[1])
    else:
        string = ''
        for x in list:
            if x != list[-1]:
                string += str(x) + ",  "
            else:
                string += "and  " + str(x)
        return string

def betCred(credit): # Asks the player how much they'd like to bet, and returns bet.  Doesn't accept invalid bets.
    bet = None
    while type(bet) != int:
        print "You have a total credit of ", credit
        bet = raw_input("How much would you like to bet? (Enter a positive Integer): ")
        print
        try:
            bet = int(bet)
        except:
            print "You did not enter an INTEGER.  Please try again."
            print

        if type(bet) == int:
            if bet > credit:
                print "You cannot bet more than you have.  Please try again."
                print
                bet = None
            elif bet <= 0:
                print "Your bet must be positive.  Please try again."
                print
                bet = None
            else:
                print "You bet ", bet
                print
    return bet

class Player():  # Keeps track of a player's or dealer's hand
    def __init__(self, name):
        self.name = name.capitalize()
        self.hand = []
    def showHand(self):
        return show(self.hand)
    def getScore(self):     # Calculates the player or dealer's score
        self.score = 0
        aces = 0
        for card in self.hand:      # Determines number of aces in hand.
            self.score += card.getValue()
            if card.getValue() == 11:
                aces += 1
            while self.score > 21 and aces > 0:  # Value of ace(s) changed to 1 if 11 would bust.
                self.score -= 10
                aces -= 1
        return self.score
    def addCard(self, card):
        self.hand += card
        print self.name + "'s Hand:  ", self.showHand()
        print self.name + "'s Score: ", self.getScore()
        print


def playHand(credit):  # Goes through the steps of playing a hand of blackjack.

    deck = list(fulldeck)

    def draw(number = 1):  # Draws cards from the deck for the player or dealer.
        cards = []
        for x in range(number):
            drawCard = random.choice(deck)
            deck.remove(drawCard)
            cards.append(Card(drawCard))
        return cards

    player = Player('player')  # Initializes player and dealer
    dealer = Player('dealer')

    bet = betCred(credit)

    player.addCard(draw(2))
    dealer.addCard(draw())

    decision = None
    while (decision != ('s' or 'S')) and (player.getScore() < 21):  # Player decides to hit or stay.
        decision = raw_input("Type 'h' to hit or 's' to stay: " )
        print
        print
        if decision == ('h' or 'H'):
            player.addCard(draw())
        else:
            print "Stay"
            print


    if player.getScore() > 21:
        print "Bust!"
        print
        print "You Lose."
        win = 0

    else:  # If player doesn't bust, dealer draws cards until his score is greater than 16.
        print "Dealer shows other card."
        print
        dealer.addCard(draw())
        print
        while dealer.getScore() < 17:
            raw_input("Dealer must hit.  Press 'Enter' when ready.")
            print
            print
            dealer.addCard(draw())

        if dealer.getScore() > 21:
            print "Dealer Busts!  You Win!"
            win = 1

        else:  # If no one busts, scores are compared here.
            print "You got ", player.getScore(), " and the dealer got ", dealer.getScore(), "."
            if player.getScore() > dealer.getScore():
                print "You Win!"
                win = 1

            else:
                print "You Lose."
                win = 0

    print
    if win == 1:  # The winner is announced and the bet is added/subtracted.
        credit += bet
        print bet, " added to your credit!"

    else:
        credit -= bet
        print bet, " subtracted from your credit"

    print
    print "Credit: ", credit
    print

    return credit


def play():  # The main function.  Credit initialized.  player asked if they want to keep playing after each hand.

    print "Welcome to BlackJack.  We'll lend you 100 credits to get started."
    raw_input("Press 'Enter' to begin.  Good luck!")
    print

    credit = 100
    keepPlaying = ''

    while keepPlaying != 'n':
        credit = playHand(credit)

        if credit <= 0:
            print "You are out of credit.  Would you like to start over?"
            credit = 100
        else:
            print "Would you like to keep playing?"
        keepPlaying = None
        keepPlaying = raw_input("Enter 'n' to quit.  Just hit 'Enter' to keep playing. ")
        print
        print

    print "Thanks for playing!  See you next time."

play()
