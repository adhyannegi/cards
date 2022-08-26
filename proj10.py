##########################################################################
#    Computer Project #10
#    Algorithm
#        >10 functions defined.        
#        >Main function starts by printing welcome message and initializing the
#         board. It then displays the board and prints the menu and asks the 
#         user for an option and checks the validity of the option. It then 
#         either moves a card from one place to another, undoes the last move,
#         restarts the game, or quits the game based on user input.
##########################################################################

#DO NOT DELETE THESE LINES
import cards, random
random.seed(100) #random number generator will always generate 
                 #the same 'random' number (needed to replicate tests)

MENU = '''     
Input options:
    MTT s d: Move card from Tableau pile s to Tableau pile d.
    MTF s d: Move card from Tableau pile s to Foundation d.
    MFT s d: Move card from Foundation s to Tableau pile d.
    U: Undo the last valid move.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game       
'''
                
def initialize():
    '''
    Creates and initializes the tableau and foundation and returns them 
    as a tuple.
    Param: None
    Returns: Tuple
    '''
    #creating empty foundation list of lists
    foundation = [[], [], [], []]
    #creating sub-lists for tableau
    l0 = []
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []
    l6 = []
    l7 = []
    
    #creating class object and shuffling the deck
    deck = cards.Deck()
    deck.shuffle()
    
    #dealing cards to sub-lists based on length of list
    for i in range(7):
        l0.append(deck.deal())
    for i in range(6):
        l1.append(deck.deal())
    for i in range(7):
        l2.append(deck.deal())
    for i in range(6):
        l3.append(deck.deal())
    for i in range(7):
        l4.append(deck.deal())
    for i in range(6):
        l5.append(deck.deal())
    for i in range(7):
        l6.append(deck.deal())
    for i in range(6):
        l7.append(deck.deal())
    
    #creating tableau list
    tableau = [l0, l1, l2, l3, l4, l5, l6, l7]
    
    return (tableau, foundation)

def display(tableau, foundation):
    '''Each row of the display will have
       tableau - foundation - tableau
       Initially, even indexed tableaus have 7 cards; odds 6.
       The challenge is the get the left vertical bars
       to line up no matter the lengths of the even indexed piles.'''
    
    # To get the left bars to line up we need to
    # find the length of the longest even-indexed tableau list,
    #     i.e. those in the first, leftmost column
    # The "4*" accounts for a card plus 1 space having a width of 4
    max_tab = 4*max([len(lst) for i,lst in enumerate(tableau) if i%2==0])
    # display header
    print("{1:>{0}s} | {2} | {3}".format(max_tab+2,"Tableau","Foundation", \
                                         "Tableau"))
    # display tableau | foundation | tableau
    for i in range(4):
        left_lst = tableau[2*i] # even index
        right_lst = tableau[2*i + 1] # odd index
        # first build a string so we can format the even-index pile
        s = ''
        s += "{}: ".format(2*i)  # index
        for c in left_lst:  # cards in even-indexed pile
            s += "{} ".format(c)
        # display the even-indexed cards; the "+3" is for the index, colon and 
        # space the "{1:<{0}s}" format allows us to incorporate the max_tab as 
        # the width so the first vertical-bar lines up
        print("{1:<{0}s}".format(max_tab+3,s),end='')
        # next print the foundation
        # get foundation value or space if empty
        found = str(foundation[i][-1]) if foundation[i] else ' '
        print("|{:^12s}|".format(found),end="")
        # print the odd-indexed pile
        print("{:d}: ".format(2*i+1),end="") 
        for c in right_lst:
            print("{} ".format(c),end="") 
        print()  # end of line
    print()
    print("-"*80)
          
def valid_tableau_to_tableau(tableau,s,d):
    '''
    Determines if move is valid from one tableau to another.
    Param: List of lists, list, list
    Returns: Boolean 
    '''
    #cannot move card from empty list
    if tableau[s] == []:
        return False
    
    #can move card to empty list
    if tableau[d] == []:
        return True
    
    #creating source and destination cards
    src = tableau[s][-1]
    destination = tableau[d][-1]
    
    #checking if move is valid or not
    if int(destination.rank() - src.rank()) == 1:
        return True
    
    return False

    
def move_tableau_to_tableau(tableau,s,d):
    '''Moves card from tableau to tableau if move is valid.
    Param: List of lists, list, list
    Returns: Boolean
    '''
    if valid_tableau_to_tableau(tableau, s, d):
        #removes element from source and puts it in destination
        val = tableau[s].pop()
        tableau[d].append(val)
        return True
    
    return False

def valid_foundation_to_tableau(tableau,foundation,s,d):
    '''
    Determines if move is valid from foundation to tableau.
    Param: List of lists, list of lists, list, list
    Returns: Boolean 
    '''
    #can move card to empty list
    if tableau[d] == []:
        return True
    
    #cannot move card from empty list
    if foundation[s] == []:
        return False
    
    #creating source and destination cards
    src = foundation[s][-1]
    destination = tableau[d][-1]
    
    #checking if move is valid or not
    if int(destination.rank() - src.rank()) == 1:
        return True
    
    return False

def move_foundation_to_tableau(tableau,foundation,s,d):
    '''Moves card from foundation to tableau if move is valid.
    Param: List of lists, list of lists, list, list
    Returns: Boolean
    '''
    if valid_foundation_to_tableau(tableau, foundation, s, d):
        #removes element from source and puts it in destination
        val = foundation[s].pop()
        tableau[d].append(val)
        return True
    
    return False

def valid_tableau_to_foundation(tableau,foundation,s,d):
    '''
    Determines if move is valid from tableau to foundation.
    Param: List of lists, list of lists, list, list
    Returns: Boolean 
    '''
    #move only allowed if card is Ace
    if foundation[d] == []:
        if tableau[s][-1].rank() == 1:
            return True
        return False
        
    #cannot move card from empty list
    if tableau[s] == []:
        return False
    
    #creating source and destination cards
    src = tableau[s][-1]
    destination = foundation[d][-1]
    
    #checking if move is valid or not
    if src.suit() == destination.suit():
        if int(src.rank() - destination.rank()) == 1:
            return True
        
    return False
    
def move_tableau_to_foundation(tableau, foundation, s,d):
    '''Moves card from tableau to foundation if move is valid.
    Param: List of lists, list, list
    Returns: Boolean
    '''
    if valid_tableau_to_foundation(tableau, foundation, s, d):
        #removes element from source and puts it in destination
        val = tableau[s].pop()
        foundation[d].append(val)
        return True
    
    return False

def check_for_win(foundation):
    '''Checks if foundation list is full or not.
    Param: List of lists
    Returns: Boolean
    '''
    #checks if there are 52 cards in the foundation list
    return (len(foundation[0]) + len(foundation[1]) + len(foundation[2]) \
        + len(foundation[3])) == 52

def get_option():
    '''Prompts user for input and checks if it is valid or not.
    Param: None
    Returns: None/List based on user input
    Displays: Error messages
    '''
    option = input("\nInput an option (MTT,MTF,MFT,U,R,H,Q): " )
    option = option.lower()
    if option[0] not in "murhq":
        #invalid input
        print("Error in option:", option)
        return None
    
    #creating a list
    list1 = option.split()
    
    #checking if input is valid or not
    if (list1[0] == "mtt"):
        list1 = [list1[0], int(list1[1]), int(list1[2])]
        if (list1[1] in range(8)) and (list1[2] in range(8)):
            return list1
        elif (list1[1] not in range(8)) and (list1[2] in range(8)):
            print("Error in Source.")
            return None
        elif (list1[1] in range(8)) and (list1[2] not in range(8)):
            print("Error in Destination")
            return None
        
    elif (list1[0] == "mtf"):
        list1 = [list1[0], int(list1[1]), int(list1[2])]
        if (list1[1] in range(8)) and (list1[2] in range(4)):
            return list1
        elif (list1[1] not in range(8)) and (list1[2] in range(4)):
            print("Error in Source.")
            return None
        elif (list1[1] in range(8)) and (list1[2] not in range(4)):
            print("Error in Destination")
            return None    
    
    elif (list1[0] == "mft"):
        list1 = [list1[0], int(list1[1]), int(list1[2])]
        if (list1[1] in range(4)) and (list1[2] in range(4)):
            return list1
        elif (list1[1] not in range(4)) and (list1[2] in range(4)):
            print("Error in Source.")
            return None
        elif (list1[1] in range(4)) and (list1[2] not in range(4)):
            print("Error in Destination")
            return None    
    
    elif list1[0] == "u":
        return list1
    
    elif list1[0] == "r":
        return list1
    
    elif list1[0] == "h":
        return list1
    
    elif list1[0] == "q":
        return list1

def main():  
    print("\nWelcome to Streets and Alleys Solitaire.\n")
    tableau, foundation = initialize()
    display(tableau, foundation)
    moves = []
    print(MENU)
    option = get_option()
    
    #keeps askig for option until valid input is provided
    while option is None:
        option = get_option()
        
    while option != None:
        
        #checks if move is valid and if user has won the game
        if option[0] == "mtt":
            s = option[1]
            d = option[2]
            if move_tableau_to_tableau(tableau, s, d):
                moves.append(option)
                if check_for_win(foundation):
                    print("You won!\n")
                    display(tableau, foundation)
                    print("\n- - - - New Game. - - - -\n")
                    tableau, foundation = initialize()
                    display(tableau, foundation)
                    print(MENU)
                
                else:
                    display(tableau, foundation)
                                    
            else:
                print("Error in move: {} , {} , {}".format(option[0].upper(),\
                                                    option[1], option[2]))
                      
        elif option[0] == "mtf":
            s = option[1]
            d = option[2]
            if move_tableau_to_foundation(tableau, foundation, s, d):
                moves.append(option)
                if check_for_win(foundation):
                    print("You won!\n")
                    display(tableau, foundation)
                    print("\n- - - - New Game. - - - -\n")
                    tableau, foundation = initialize()
                    display(tableau, foundation)
                    print(MENU)
                
                else:
                    display(tableau, foundation)
                                    
            else:
                print("Error in move: {} , {} , {}".format(option[0].upper(),\
                                                        option[1], option[2]))   
        
        elif option[0] == "mft":
            s = option[1]
            d = option[2]
            if move_foundation_to_tableau(tableau, foundation, s, d):
                moves.append(option)
                if check_for_win(foundation):
                    print("You won!\n")
                    display(tableau, foundation)
                    print("\n- - - - New Game. - - - -\n")
                    tableau, foundation = initialize()
                    display(tableau, foundation)
                    print(MENU)
                
                else:
                    display(tableau, foundation)
                                    
            else:
                print("Error in move: {} , {} , {}".format(option[0].upper(),\
                                                        option[1], option[2]))  
                
        elif option == ["U"] or option == ["u"]:
            if moves == []:
                print("No moves to undo.")                            
            
            else:
                #undo te moves basd on movement of last element
                print("Undo: {} {} {}".format(moves[-1][0].upper(), \
                                              moves[-1][1], moves[-1][2]))
                if moves[-1][0][1].upper() == "T" and \
                    moves[-1][0][2].upper() == "T":
                    val = tableau[moves[-1][2]].pop()
                    tableau[moves[-1][1]].append(val)
                    moves.pop()            
                    
                elif moves[-1][0][1].upper() == "F" and \
                    moves[-1][0][2].upper() == "T":
                    val = tableau[moves[-1][2]].pop()
                    foundation[moves[-1][1]].append(val)
                    moves.pop()
                    
                elif moves[-1][0][1].upper() == "T" and \
                    moves[-1][0][2].upper() == "F":
                    val = foundation[moves[-1][2]].pop()
                    tableau[moves[-1][1]].append(val)       
                    moves.pop()
                    
                display(tableau, foundation)

        elif option == ["Q"] or option == ["q"]:
            #quits the program
            print("Thank you for playing.")
            break
        
        #continues to ask for input
        option = get_option()
        while option is None:
            option = get_option()
                                                                                        
if __name__ == '__main__':
     main()
