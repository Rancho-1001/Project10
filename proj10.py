###########################################################

#  Computer Project #10
#
#
#
#  Algorithm
#           This program imports the cards file which contains the card and deck classes  
#           The program uses 9 functions and 1 main function. 
#           The docstrings for the various functions have been included in the functions.
#           The Functions:
#                         1. init_game()
#                         2. deal_to_tableau()
#                         3. validate_move_to_foundation()
#                         4. move_to_foundation()
#                         5. validate_move_within_tableau()
#                         6. move_within_tableau()
#                         7. check_for_win()
#                         8. display()
#                         9. get_option()
#
#           The main function:
#                1. initializes the game by calling the init_game function
#                2. displays the rules of the game and gets an option from the user
#                3. it then loops till the user quits by inputing ("Q" or "q")
#                4. The program keeps showing the current state of the game and prompts the user 
#                    to enter a command until the user wins the game or enters ("Q" or "q"), which ever comes first   
#                5. The program detects, reports, and recovers from invalid commands from the user.      
#                6. None of the data structures for stock, tableau, or foundation is altered by an invalid command.     
#                                      
#                                   
###########################################################

import cards  # required !!!

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
     of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''


def init_game():
    """
    Initializes the Aces Up game by creating a shuffled deck, dealing four cards from the deck into a four-column tableau,
    creating an empty foundation pile, and returning all three as variables.

    Returns:
    - deck: a shuffled deck of 52 cards
    - tableau: a list of four lists, each containing one card dealt from the deck
    - foundation: an empty list representing the foundation pile
    """
    deck = cards.Deck()
    deck.shuffle()

    tableau = [[] for _ in range(4)]         #initialize four empty tableau
    for i in range(4):
        tableau[i].append(deck.deal())       #deal a card to each tableau 
    
    #initalize empty foundation
    foundation = []

    return deck, tableau, foundation


def deal_to_tableau(tableau, stock):
    """
    This function is used to deal cards to the tableau. It deals a card from 
    the stock to each column of the tableau, unless the stock has fewer than 4 cards
    in which case it deals a card to consecutive columns until the stock is empty.

    Parameters: 
            tableau ----> (list of lists)
            stock ----> (type Class Deck)
    Returns:
            Nothing 
    """
    # Deal cards to each column of the tableau
    for i in range(4):
        # If the stock is not empty, deal a card to the column
        if not stock.is_empty():
            tableau[i].append(stock.deal())
        # Otherwise, break out of the loop
        else:
            break
        

def validate_move_to_foundation(tableau, from_col):
    """
    This function is used to check whether a move to the foundation is valid based on 
    the rules of the game. It returns true if valid and false if not valid and prints 
    an error message.

    Parameter:
            tableau ----> (list of lists)
            from_col ----> (int) range(0-3)
        
    Returns: 
            Bool  
    """

    #If the list is empty return false 
    if len(tableau[from_col]) == 0:
        print("\nError, empty column:" + str(from_col))
        return False

    #set a variable for the card to move and find its suit and rank 
    card_to_move = tableau[from_col][-1]
    suit = card_to_move.suit()
    rank = card_to_move.rank()

    for i in tableau:
        if len(i) > 0:
            #treat aces as high 
            rank = 14 if rank == 1 else rank
            
            #find the rank of the bottom card and set and treat aces as high
            card_rank = i[-1].rank()
            card_rank = 14 if card_rank == 1 else card_rank

            #compare if the have the same suit, if so, compare the rank 
            if i[-1].suit() == suit:
                if card_rank > rank:
                    return True
        else:
            continue

    #if anything else, print error message and return False         
    print("\nError, cannot move {}.".format(card_to_move))
    return False


def move_to_foundation(tableau, foundation, from_col):
    """
    This function calls the validate move to foundation to check if valid or not
    if move is valid the function updates the tableau and foundation; otherwise,
    it does nothing

    Parameter:
            tableau ----> (list of lists)
            foundation ----> (list) 
            from_col ----> (int) range(0-3)
        
    Returns: 
            Nothing

    """

    #check for validity and update the tableau and foundation 
    if validate_move_to_foundation(tableau, from_col):
        card_to_move = tableau[from_col].pop()
        foundation.append(card_to_move)


def validate_move_within_tableau(tableau, from_col, to_col):
    """
    The function checks if a move within a tableau is valid. 
    It returns True, if the move is valid and False otherwise, and 
    also prints error messages. 
    Parameter:
            tableau ----> (list of lists)
            from_col ----> (int) range(0-3)
            to_col ----> (int) range(0-3)
        
    Returns: 
            Bool 
    """
    
    #checks if column is empty 
    if len(tableau[from_col]) == 0 and len(tableau[to_col]) == 0: 
        print("\nError, no card in column:",str(from_col+1))
        return False

    #checks if column moving from is not empty and column sending to is empty
    if len(tableau[from_col]) > 0 and len(tableau[to_col]) == 0:
        return True 

    #checks if column moving from is empty and column sending is not empty
    if len(tableau[from_col]) == 0 and len(tableau[to_col]) > 0:     
        print("\nError, target column is not empty:",str(to_col+1))
        return False
    
    #checks if both columns are not empty 
    if len(tableau[from_col]) > 0 and len(tableau[to_col]) > 0:
        print("\nError, target column is not empty:",str(to_col+1))
        return False


def move_within_tableau(tableau, from_col, to_col):
    """
    Move a card within the tableau from the bottom of one column to the bottom of another.
    If the move is not valid, do nothing.
    Parameter:
            tableau ----> (list of lists)
            from_col ----> (int) range(0-3)
            to_col ----> (int) range(0-3)
        
    Returns: 
            Nothing 
    """
    if validate_move_within_tableau(tableau, from_col, to_col):
        card_to_tableau = tableau[from_col].pop()
        tableau[to_col].append(card_to_tableau) 
        

def check_for_win(tableau, stock):
    """
    This function checks if the game has been won;returns True if the stock is empty
    and the tableau contains only the four aces, and False, otherwise.

    Parameters: 
            tableau ----> (list of lists)
            stock ----> (type Class Deck)
    Returns:
            Bool  
    """
            
    # Check if stock is empty
    if len(stock) > 0:
        return False

    # Check if tableau contains only aces
    for column in tableau:
        for card in column:
            if card.rank() != 1:
                return False
    return True


def display( stock, tableau, foundation ):
    '''Provided: Display the stock, tableau, and foundation.'''

    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    maxm = 0
    for col in tableau:
        if len(col) > maxm:
            maxm = len(col)
    
    assert maxm > 0   # maxm == 0 should not happen in this game?
        
    for i in range(maxm):
        if i == 0:
            if stock.is_empty():
                print("{:<8s}".format(""),end='')
            else:
                print("{:<8s}".format(" XX"),end='')
        else:
            print("{:<8s}".format(""),end='')        
        
        #prior_ten = False  # indicate if prior card was a ten
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print( "{:4s}".format( str(col[i]) ), end='' )

        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')
                
        print()


def get_option():
    """
    This function prompts the user to enter an option and it returns a designed representation
    of the option for subsequent processing. 

    Parameter:
            Nothing
    
    Returns:
            A list 

    """ 
    while True:
        choice = input("\nInput an option (DFTRHQ): ")
        tokens = choice.split()
        if len(tokens) == 1 and tokens[0].upper() in ['D', 'R', 'H', 'Q']:
            return [tokens[0].upper()]
        elif len(tokens) == 2 and tokens[0].upper() == 'F' and tokens[1].isdigit() and 1 <= int(tokens[1]) <= 4:
            return [tokens[0].upper(), int(tokens[1])-1]
        elif len(tokens) == 3 and tokens[0].upper() == 'T' and tokens[1].isdigit() and tokens[2].isdigit() \
                and 1 <= int(tokens[1]) <= 4 and 1 <= int(tokens[2]) <= 4 and tokens[1] != tokens[2]:
            return [tokens[0].upper(), int(tokens[1])-1, int(tokens[2])-1]
        else:
            print("\nError in option:",choice)
            return []


def main():
    # Initialize game
    stock, tableau, foundation = init_game()
    print(RULES)
    print(MENU)

    # Loop until game over or quitting
    while True:
        # Display current state of game
        display(stock, tableau, foundation)
        
        # Get user command
        option = get_option()
        
        
        # Handle user command
        while not option:
            option = get_option() 

        if option[0] == "Q":
            # Quit the game
            print("\nYou have chosen to quit.")
            break

        elif option[0] == "H":
            print(MENU)
            
        elif option[0] == "R":
            # Restart the game
            print("\n=========== Restarting: new game ============")
            stock, tableau, foundation = init_game()
            print(RULES)
            print(MENU)
            
        elif option[0] == "D":
            deal_to_tableau(tableau, stock) 

        elif option[0] == "F":
            # Deal card to tableau 
            from_col = option[1]
            if validate_move_to_foundation(tableau, from_col):
                move_to_foundation(tableau, foundation, from_col)
                if check_for_win(tableau, stock):
                    # Player has won the game
                    print("\nYou won!") 
                    break 
           
        elif option[0] == "T":
            from_col, to_col = option[1], option[2]
            if validate_move_within_tableau(tableau, from_col, to_col):
                move_within_tableau(tableau, from_col, to_col)

         
if __name__ == '__main__':
    main()


"\nInput an option (DFTRHQ): "
"\nError, empty column:"
"\nError, cannot move {}."
"\nError, no card in column:"
"\nError, target column is not empty:"
"\nError in option:"
"=========== Restarting: new game ============"
"\nYou have chosen to quit."
"\nYou won!" 