#uno game

#create deck of cards
def buildDeck():
    deck = []
    colours = ["red", "green", "blue", "yellow"]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    actioncards = ["draw2", "reverse", "skip"]
    wildcards = ["wild", "drawfour"]
    for i in range(len(numbers)):
        for j in range(len(colours)):
            deck.append((colours[j], numbers[i]))
            if numbers[i] != 0:
                deck.append((colours[j], numbers[i]))

    for actioncard in actioncards:
        for _ in range(2):
            for j in range(len(colours)):
                deck.append((actioncards, 0))

    for wildcard in wildcards:
        for _ in range(4):
            deck.append((wildcard, 0))

    return deck

#special cards function
def specialcards(card, current_player, players, deck, discarded, direction):
    next_player = (current_player + direction) % len(players)

    if card[0] == "draw2":
        for _ in range(2):
            drawn_card = drawpile(deck, players, discarded, list(players.keys())[next_player])
            if drawn_card:
                players[list(players.keys())[next_player]].append(drawn_card)
        print(f"Player {list(players.keys())[next_player]} drew 2 cards")
        return (next_player + direction) % len(players)  # Skip the next player's turn

    elif card[0] == "reverse":
        direction = -direction
        print(f"Player {list(players.keys())[current_player]} reversed the direction")
        return current_player, direction

    elif card[0] == "skip":
        print(f"Player {list(players.keys())[next_player]} was skipped")
        return (next_player + direction) % len(players)  # Skip the next player

    elif card[0] == "wild":
        colors = ["red", "green", "blue", "yellow"]
        while True:
            new_color = input("Choose a color (red/green/blue/yellow): ").lower()
            if new_color in colors:
                break
            print("Invalid color. Please choose red, green, blue, or yellow.")
        print(f"Color changed to {new_color}")
        return current_player, new_color  # Return the new color

    elif card[0] == "drawfour":
        for _ in range(4):
            drawn_card = drawpile(deck, players, discarded, list(players.keys())[next_player])
            if drawn_card:
                players[list(players.keys())[next_player]].append(drawn_card)
        print(f"Player {list(players.keys())[next_player]} drew 4 cards")
        colors = ["red", "green", "blue", "yellow"]
        while True:
            new_color = input("Choose a color (red/green/blue/yellow): ").lower()
            if new_color in colors:
                break
            print("Invalid color. Please choose red, green, blue, or yellow.")
        print(f"Color changed to {new_color}")
        return (next_player + direction) % len(players), new_color  # Skip next player and return new color

    return current_player  # if it's not a special card, return the current player

#shuffle deck
def shuffleDeck(deck):
    import random
    random.shuffle(deck)
    return deck

#enter number of players
def enterPlayers():
    players = {}
    num_players = int(input("Enter number of players: "))

    if num_players < 2 or num_players > 7:
        print("Invalid number of players. Please enter a number between 2 and 7.")
        return enterPlayers()

    num_human_players = 0
    for i in range(num_players):
        while True:
            player_type = input(f"Is player {i+1} human or computer? (h/c): ").lower()

            if player_type == 'h':
                player_name = input(f"Enter Player {i+1} name: ")
                num_human_players += 1
                break

            elif player_type == 'c':
                player_name = f"Computer_{i+1}"
                break

            else:
                print("Invalid input. Defaulting to computer player.")
                player_name = f"Computer_{i+1}"

        players[player_name] = []

    return players

#deal a hand to players
def dealHands(deck, players):
    for _ in range(7):
        for player in players:
            if deck:  # to check if there are still cards in the deck
                players[player].append(deck.pop())
    return players

#drawpile is cards remaining after a hand is dealt
#draw a card from the drawpile
def drawpile(deck, players, discarded, player):
    if not deck:
        deck = refill_deck(discarded)

        if not deck:
            print("No more cards available.")
            return None
    drawn_card = deck.pop()
    print(f"Player {player} drew a card from the drawpile")
    return drawn_card

#discardpile is cards played and keeps the top card in play
def discardpile(deck, players):
    discarded = []
    for player in players:
        print(f"Player {player}, your hand is: {players[player]}")
        discard = input("Enter the card you want to play: ")
        if discard in players[player]:
            players[player].remove(discard)
            discarded.append(discard)
            print(f"Player {player} played {discard}")
            break
        else:
            print("!!!Invalid card!!!")
    return discarded

def refill_deck(discarded):
    if not discarded:
        return []
    print("No more cards in the drawpile")
    print("Taking cards from the discardpile.....")
    # keep the top card from the discard pile
    top_card = discarded.pop()
    # shuffle remaining cards
    new_deck = shuffleDeck(discarded)
    print("shuffling cards...")

    # add the top card from the drawpile to the new deck
    discarded.clear()
    discarded.append(top_card)
    return new_deck

#player actions
def playeractions(players, discardpile, drawpile, player, discarded):
    if player.startswith("Computer_"):
        return computer_action(players, discardpile, drawpile, player)

    while True:
        print(f"Player {player}, your hand is: {players[player]}")
        action = input("Enter 'draw', 'play', or 'pass': ")
        if action == "draw":
            drawn_card = drawpile(drawpile, players, discarded, player)  # Pass the correct arguments to drawpile
            if drawn_card:
                players[player].append(drawn_card)
            else:
                print("No cards left to draw!")

        elif action == "play":
            card_to_play = input("Enter the card you want to play: ")

            if can_play_card(card_to_play, discardpile[-1]):
                players[player].remove(card_to_play)
                discardpile.append(card_to_play)
                print(f"{player} played {card_to_play}")
                if card_to_play[0] in ["draw2", "reverse", "skip", "wild", "drawfour"]:
                    return "special cards"
                break
            else:
                print("Invalid card. Please choose a valid card to play.")

        elif action == "pass":
            break
        else:
            print("Invalid action. Please enter 'draw', 'play', or 'pass'.")

def computer_action(players, discardpile, drawpile, player):
    import random
    playable_cards = [card for card in players[player] if can_play_card(card, discardpile[-1])]
    if playable_cards:
        card_to_play = random.choice(playable_cards)
        players[player].remove(card_to_play)
        discardpile.append(card_to_play)
        print(f"{player} played {card_to_play}")
        if card_to_play[0] in ["draw2", "reverse", "skip", "wild", "drawfour"]:
            return "special cards"
    else:
        drawn_card = drawpile(drawpile, players, discardpile, player)
        if drawn_card:
            players[player].append(drawn_card)
            print(f"{player} drew a card")
        else:
            print(f"{player} passed")

def can_play_card(card, top_card):
    if not top_card:
        return False
    color_match = top_card[0] == card[0]
    number_match = top_card[1] == card[1]
    wild_match = card[0] in ["wild", "drawfour"]
    return color_match or number_match or wild_match

def game_play():
    #initializing

    deck = buildDeck()
    shuffleDeck(deck)
    players = enterPlayers()
    dealHands(deck, players)
    discarded = []
    direction = 1

    #start game with first card
    first_card = deck.pop()
    while first_card[0] in ["wild", "drawfour"]:
        deck.append(first_card)
        shuffleDeck(deck)
        first_card = deck.pop()
    discarded.append(first_card)
    print(f"The First card played: {first_card}")

    #main game loop
    current_player = 0
    while True:
        player_name = list(players.keys())[current_player]
        print(f"\nIt's {player_name}'s turn.")
        print(f"Top Card: {discarded[-1]}")

        if player_name.startswith("Computer_"):
            action = computer_action(players, discarded, deck, player_name)
        else:
            action = playeractions(players, discarded, deck, player_name, discarded)

        #check for win
        if len(players[player_name]) == 0:
            print(f"{player_name} WINS!!!")
            break

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

    print("!!!UNO!!!")

game_play()
