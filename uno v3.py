import random


def buildDeck():
    '''Builds a standard UNO deck with numbers, action cards, and wild cards.'''
    deck = []
    colours = ["red", "green", "blue", "yellow"]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    actioncards = ["draw2", "reverse", "skip"]
    wildcards = ["wild", "drawfour"]
    for i in range(len(numbers)):
        for j in range(len(colours)):
            deck.append(colours[j] + " " + str(numbers[i]))
            if numbers[i] != 0:
                deck.append(colours[j] + " " + str(numbers[i]))

#    for actioncard in actioncards:

    for _ in range(2):
        for i in range(len(actioncards)):
            for j in range(len(colours)):
                deck.append(colours[j] +" "+ actioncards[i] )

    for wildcard in wildcards:
        for _ in range(4):
            deck.append(wildcard,)
    
    return deck


def specialcards(card, current_player, players, deck, discarded, direction):
    next_player = (current_player + direction) % len(players)
    card_type = card.split()[1] if " " in card else card
    
    if card_type == "draw2":
        for _ in range(2):
            drawn_card = deck.pop()
            #drawn_card = drawpile(deck, players, discarded, list(players.keys())[next_player])
            if drawn_card:
                players[next_player].append(drawn_card)
        print(f"Player {next_player} drew 2 cards")
        return (next_player + direction) % len(players) , deck  # Skip the next player's turn

    elif card_type == "reverse":
        direction = -direction
        print(f"Player {list(players.keys())[current_player]} reversed the direction")
        return current_player, direction

    elif card_type == "skip":
        print(f"Player {list(players.keys())[next_player]} was skipped")
        return (next_player + direction) % len(players)  # Skip the next player

    elif card_type == "wild":
        colors = ["red", "green", "blue", "yellow"]
        while True:
            new_color = input("Choose a color (red/green/blue/yellow): ").lower()
            if new_color in colors:
                break
            print("Invalid color. Please choose red, green, blue, or yellow.")
        print(f"Color changed to {new_color}")
        return current_player, new_color  # Return the new color

    elif card_type == "drawfour":
        for _ in range(4):
            drawn_card = deck.pop()
            #drawn_card = drawpile(deck, players, discarded, list(players.keys())[next_player])
            if drawn_card:
                players[next_player].append(drawn_card)
        print(f"Player {next_player} drew 4 cards")
        colors = ["red", "green", "blue", "yellow"]
        while True:
            new_color = input("Choose a color (red/green/blue/yellow): ").lower()
            if new_color in colors:
                break
            print("Invalid color. Please choose red, green, blue, or yellow.")
        print(f"Color changed to {new_color}")
        return (next_player + direction) % len(players), new_color  # Skip next player and return new color

    return current_player  # if it's not a special card, return the current player


def shuffleDeck(deck):
    import random
    random.shuffle(deck)
    return deck


#enter number of players
def enterPlayers():
    players = {}
    print("#"*100)
    num_players = int(input("Enter number of players: "))

    if num_players < 2 or num_players > 7:
        print("Invalid number of players. Please enter a number between 2 and 7.")
        return enterPlayers()

    num_human_players = 0
    for i in range(num_players):
        while True:
            print("#"*100)
            player_type = input(f"Is player {i+1} human or computer? (h/c): ").lower()

            if player_type == 'h':
                print("#"*100)
                player_name = input(f"Enter Player {i+1} name: ")
                num_human_players += 1
                break

            elif player_type == 'c':
                print("#"*100)
                player_name = f"Computer_{i+1}"
                break

            else:
                print("Invalid input. Defaulting to computer player.")
                player_name = f"Computer_{i+1}"

        players[player_name] = []

    return players


def dealHands(deck, players):
    for player_name in players:
        for _ in range(7):
            players[player_name].append(deck.pop())
    return players, deck

def drawpile(deck, discarded):

    if not deck:
        deck = refill_deck(discarded)

        if not deck:
            print("No more cards available.")
            return None
    return deck.pop()


def discardpile(deck, discarded):
    return discarded, deck
#discarded = []
    

def refill_deck(discarded):
    if not discarded:
        return []
    print("No more cards in the drawpile")
    print("Taking cards from the discardpile.....")
    # keep the top card from the discard pile
    top_card = discarded.pop()
    # shuffle remaining cards
    deck = shuffleDeck(discarded)
    print("shuffling cards...")

    # add the top card from the drawpile to the new deck
    discarded.clear()
    discarded.append(top_card)
    return deck

#player actions
def playeractions(players, discarded, drawpile, player_hand, player_name):
    #if player_name.startswith("Computer_"):
    #    return computer_action(players, discarded, drawpile, player_hand, player_name)

    while True:
        print(f"Player {player_name}, your hand is: {player_hand}")
        action = input("Enter 'draw', 'play', or 'pass': ")

        if action == "draw":

           #drawn_card = drawpile(deck, players, discarded)
            drawn_card = deck.pop()
            if drawn_card:
                player_hand.append(drawn_card)
                print(f"Player {player_name} drew {drawn_card} from the drawpile")
            return player_hand, discarded


        elif action == "play":
            card_to_play = input("Enter the card you want to play: ")

            if can_play_card(player_hand, discarded):
                player_hand.remove(card_to_play)
                discarded.append(card_to_play)
                print(f"{player_name} played {card_to_play}")

                #if card_to_play.split()[0] in ["draw2", "reverse", "skip", "wild", "drawfour"]:
                #    specialcards(card_to_play, players, deck, discarded, direction)
                #    return "special cards"
                return players, player_hand, discarded      
            else:
                print("Invalid card. Please choose a valid card to play.")

        elif action == "pass":
        #    return (next_player) % len(players)

            break
        else:
            print("Invalid action. Please enter 'draw', 'play', or 'pass'.")



def computer_action(players, player_hand, discarded, deck, player_name):
 
    while True:
        playable_cards = [card for card in player_hand if can_play_card([card], discarded)]
        if playable_cards:
            card_to_play = random.choice(playable_cards)
            player_hand.remove(card_to_play)
            discarded.append(card_to_play)
            print(f"{player_name} played {card_to_play}")

            if card_to_play.split()[0] in ["draw2", "reverse", "skip", "wild", "drawfour"]:
                return "special cards"
            return player_hand, discarded
        else:
            #drawn_card = drawpile(deck, discarded)
            drawn_card = deck.pop()
            if drawn_card:
                player_hand.append(drawn_card)
                print(f"{player_name} drew a card")
            return player_hand, discarded

def can_play_card(player_hand, discarded):
    if not discarded:
        return False

    top_card = discarded[-1]
    top_card_split = top_card.split(" ")
    top_card_colour = top_card_split[0]
    top_card_value = top_card_split[1] if len(top_card_split) > 1 else None

    for card in player_hand:
        card_split = card.split(" ")
        card_colour = card_split[0]
        card_value = card_split[1] if len(card_split) > 1 else None

        # Wild cards can always be played
        if card_colour in ["wild", "drawfour"]:
            return True

        # If top card is wild/drawfour, only color match or another wild/drawfour is valid
        if top_card_colour in ["wild", "drawfour"]:
            continue  # Only wilds can be played on wilds

        # Color or value match
        if card_colour == top_card_colour or (card_value and card_value == top_card_value):
            return True

    return False


    #initializing

deck = buildDeck()
shuffleDeck(deck)
print(''' _    _  ____  __    ___  _____  __  __  ____    ____  _____    __  __  _  _  _____ 
( \/\/ )( ___)(  )  / __)(  _  )(  \/  )( ___)  (_  _)(  _  )  (  )(  )( \( )(  _  )
 )    (  )__)  )(__( (__  )(_)(  )    (  )__)     )(   )(_)(    )(__)(  )  (  )(_)( 
(__/\__)(____)(____)\___)(_____)(_/\/\_)(____)   (__) (_____)  (______)(_)\_)(_____)

''')
players = enterPlayers()
dealHands(deck, players)
discardpile = []
discarded = list()
drawpile = []
direction = 1
#    player_hand = players[player_name]

#start game with first card
first_card = deck.pop()
while first_card[0] in ["wild", "drawfour"]:
    deck.append(first_card)
    shuffleDeck(deck)
    first_card = deck.pop()
discarded.append(first_card)
top_card = first_card
print(f"The First card played: {first_card}")

#main game loop
current_player = 0
gameplaying = True
while gameplaying:

    player_names = list(players.keys())
    player_name = player_names[current_player]
    player_hand = players[player_name]
    print("#"*100)
    print(f"\nIt's {player_name}'s turn.")
    print("="*100)
    print(f"Top Card: {discarded[-1]}")
    print("="*100)

    if player_name.startswith("Computer_"):
        action = computer_action(players, discarded, drawpile, player_hand, player_name)
    else:
        action = playeractions(players, discarded, drawpile, player_hand, player_name)
        
    if len(player_hand) == 0:
        print(f"{player_name} WINS!!!")

        gameplaying = False

    #handle special cards
    if action == "special cards":
        result = specialcards(discarded[-1], current_player, players, deck, discarded, direction)
        if isinstance(result, tuple):
            current_player, direction = result
        else:
            current_player = result
    else:
        #move to next player
        current_player = (current_player + direction) % len(players)

    if len(deck) == 0:
        deck = refill_deck(discarded)
    top_card = discarded[-1]
    print("#"*100)  
print('''.------..------..------.
|U.--. ||N.--. ||O.--. |
| (\/) || :(): || :/\: |
| :\/: || ()() || :\/: |
| '--'U|| '--'N|| '--'O|
`------'`------'`------''')

