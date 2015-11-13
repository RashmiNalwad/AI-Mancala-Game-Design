import sys;
import copy;

posP = 0;
posC = 0;

class Mancal:
    PLAYER = 0
    CUT_OFF = 0
    DIMENSION = 3
    BOARD = None
    MANC = {}
    UTILITY_VALUE = []
    VALUE = -200000000
    CHILDREN = {}
    DEPTH = 0
    PLAYED = False
    SIB_UTIL = {}
    ALPHA = None
    BETA = None
    SELF_TURN = False

    def __init__(self):
        pass
    def assign_values(self,PLAYER,CUT_OFF,BOARD,MANC,DIMENSION,UTILITY_VALUE,VALUE,CHILDREN,DEPTH,PLAYED,SIB_UTIL,ALPHA,BETA,SELF_TURN):
        self.PLAYER = PLAYER
        self.CUT_OFF = CUT_OFF
        self.BOARD = BOARD
        self.MANC = MANC
        self.DIMENSION = DIMENSION
        self.UTILITY_VALUE = UTILITY_VALUE
        self.VALUE = VALUE
        self.CHILDREN = CHILDREN
        self.DEPTH = DEPTH
        self.PLAYED = PLAYED
        self.SIB_UTIL = SIB_UTIL
        self.ALPHA = ALPHA
        self.BETA = BETA
        self.SELF_TURN = SELF_TURN

def read_write_file(file_handler): #Reading Entire file
    algo_type = ""
    m = 0
    n = 0
    for each_line in file_handler:
        if "1" in each_line:
            write_handler_next = open('next_state.txt','w')
            algo_type = each_line
            root,dimension = read_data(file_handler,algo_type)
            first_player = choose_player(root,m,n)
            play_greedy_game(root,first_player,dimension,write_handler_next)
        elif "2" in each_line:
            write_handler_next = open('next_state.txt','w')
            write_handler_traverse = open('traverse_log.txt','w+')
            algo_type = each_line
            root,dimension = read_data(file_handler,algo_type)
            first_player = choose_player(root,m,n)
            play_game(root,first_player,dimension,write_handler_traverse,write_handler_next)
        elif "3" in each_line:
            write_handler_next = open('next_state.txt','w')
            write_handler_traverse = open('traverse_log.txt','w+')
            algo_type = each_line
            root,dimension = read_data(file_handler,algo_type)
            first_player = choose_player(root,m,n)
            play_alphaBeta_game(root,first_player,dimension,write_handler_traverse,write_handler_next)
        else:
            write_handler_next = open('next_state.txt','w')
            write_handler_traverse = open('traverse_log','w')
            algo_type = each_line

def read_data(file_handler,algo_type):
    player = 0
    cut_of_depth = 0
    mancala2 = -1
    mancala1 = -1
    dimension = 0
    board = []
    for each_line in file_handler:
        if player == 0:
            player = each_line.rstrip("\n")
        elif algo_type != 1 and cut_of_depth == 0:
            cut_of_depth = each_line.rstrip("\n")
        elif len(board) == 0 or len(board) == 1:
            values  = each_line.rstrip("\n").split(" ")
            board.append(values)
            dimension = len(values)
        elif mancala2 == -1:
            mancala2 = each_line.rstrip("\n")
        elif mancala1 == -1:
            mancala1 = each_line.rstrip("\n")
    root = make_node(player,cut_of_depth,board,mancala2,mancala1,dimension,[],-200000000,{},0,{},-100000000,100000000)
    return root,dimension

def make_node(Player,cut_off,board,mancala2,mancala1,dimension,utility_list,value,children,depth,sib_util,alpha,beta):
    """
     :type board: 2d list ( matrix)
    """
    node = Mancal()
    manc = {}
    manc.update({"1":mancala1})
    manc.update({"2":mancala2})
    brd = copy.deepcopy(board)
    node.assign_values(Player,cut_off,brd,manc,dimension,utility_list,value,children,depth,False,sib_util,alpha,beta,False)
    return node

def choose_player(root, m=0, n=0):
    first_player = {}
    if int(root.PLAYER) == 1:
        first_player.update({"m":1})
        first_player.update({"n":0})
    else:
        first_player.update({"m":0})
        first_player.update({"n":0})

    return first_player

def play_greedy_game(root,first_player,dimension,write_handler_next):
    n = first_player.get("n")
    m = first_player.get("m")
    for n in range(0,dimension):
        child, self_turn,end_game = play_greedy(root,root.BOARD,first_player,dimension,m,n,False)
        if child.PLAYED == True:
            if self_turn and end_game == False: #calling siblings
                for sib in range(0,dimension):
                    if (sib == n and child.BOARD[m][sib] == 0) or child.BOARD[m][sib] == 0:
                        continue
                    else:
                        call_greedy_siblings(child,dimension,m,sib,child.DEPTH,first_player)
                        if(child.DEPTH%2 == 0):
                            if len(child.SIB_UTIL) > 0:
                                child.VALUE = min(child.SIB_UTIL) # IF min node take max of sibling
                        else:
                            if len(child.SIB_UTIL) > 0:
                                child.VALUE = max(child.SIB_UTIL) #IF max node take min of sibling
                    
                    if root.CHILDREN.get(child.VALUE):
                        root.CHILDREN.get(child.VALUE).append(child)
                    else:
                        root.CHILDREN.update({child.VALUE:[child]})
                  
                root.UTILITY_VALUE.append(child.VALUE)
                root.VALUE = max(root.UTILITY_VALUE)
            else:  
                root.UTILITY_VALUE.append(child.VALUE)
                root.VALUE = max(root.UTILITY_VALUE)
            
                if root.CHILDREN.get(child.VALUE):
                    root.CHILDREN.get(child.VALUE).append(child)
                else:
                    root.CHILDREN.update({child.VALUE:[child]})
     
    compute_next_state(root,write_handler_next)

def play_greedy(root,board,first_player,dimension,m,n,isSibling):
    parent_board = root.BOARD
    board_pos = n+2
    mancala2 = root.MANC.get('2')
    mancala1 = root.MANC.get('1')
    end_game = False
    if (m == 1):
        player = "B" + str(board_pos)
    else:
        player = "A" + str(board_pos)
    
    child = make_node(player,root.CUT_OFF,parent_board,mancala2,mancala1,dimension,[],-200000000,{},root.DEPTH,{},-100000000,100000000)
    
    points = child.BOARD[m][n]     
    points = int(points)      
    child.BOARD[m][n] = 0
    
    ''' calling distribute points''' 
    
    if points == 0:
        child.PLAYED = False
    else:
        child.PLAYED = True    
        
    if points != 0:
        self_turn,brd,mancala1,mancala2,end_game = distribute_points(points,m,n,child.BOARD,dimension,mancala1,mancala2)
        child.BOARD = brd  
        
        if self_turn == True:
            child.SELF_TURN = True
        else:
            child.SELF_TURN = False               
        
        if isSibling:
            child.DEPTH = root.DEPTH
        else:    
            child.DEPTH = root.DEPTH + 1
            
        child.MANC.update({'1':mancala1})
        child.MANC.update({'2':mancala2})    
            
        if ( first_player.get('m') == 1):
            child.VALUE = mancala1 - mancala2
        else:
            child.VALUE = mancala2 - mancala1      
    else:
        manc1 = root.MANC.get('1')
        manc2 = root.MANC.get('2')
        
        manc1 = int(manc1)
        manc2 = int(manc2)
        if ( first_player.get('m') == 1):
            child.VALUE = manc1 - manc2
        else:
            child.VALUE = manc2 - manc1 
        self_turn = False
        end_game = False
        child.PLAYED = False
                
    return child,self_turn,end_game    

def call_greedy_siblings(parent,dimension,m,n,depth,first_player):
    pred,self_turn,end_game = play_greedy(parent,parent.BOARD,first_player,dimension,m,n,True)
    if pred.PLAYED == True:
        if self_turn and end_game == False: #testing
            for sib in range(0,dimension):
                if (sib == n and pred.BOARD[m][sib] == 0) or pred.BOARD[m][sib] == 0:
                    continue
                else:
                    sibling = call_greedy_siblings(pred,dimension,m,sib,pred.DEPTH,first_player)
                    
                    if(pred.DEPTH%2 == 0):
                        if len(pred.SIB_UTIL) > 0:
                            pred.VALUE = min(pred.SIB_UTIL.keys()) # IF min node take max of sibling
                    else:
                        if len(pred.SIB_UTIL) > 0:
                            pred.VALUE = max(pred.SIB_UTIL.keys()) #IF max node take min of sibling
                    
                    if parent.SIB_UTIL.get(pred.VALUE):
                        if sibling.VALUE == pred.VALUE:
                            parent.SIB_UTIL.get(pred.VALUE).append(pred)
                    else:
                        parent.SIB_UTIL.update({pred.VALUE:[pred]})  
        else:
            if parent.SIB_UTIL.get(pred.VALUE):
                parent.SIB_UTIL.get(pred.VALUE).append(pred)
            else:
                parent.SIB_UTIL.update({pred.VALUE:[pred]})  
        
    return pred

def play_game(root,first_player,dimension,write_handler_traverse,write_handler_next):
    n = first_player.get("n")
    m = first_player.get("m")
    write_line_to_file(write_handler_traverse, "Node" + "," + "Depth" +"," + "Value" + "\n",True)
    write_line_to_file(write_handler_traverse, "root" + "," + str(0) + "," + "-Infinity" + "\n",True)
    for n in range(0,dimension):
        child,self_turn,value,end_game = play(root,root.BOARD,first_player,dimension,m,n,False,write_handler_traverse,False)
        if child.PLAYED == True:
            if end_game == True:
                print(" ")
            if self_turn and end_game == False: #calling siblings
                for sib in range(0,dimension):
                    if (sib == n and child.BOARD[m][sib] == 0) or child.BOARD[m][sib] == 0:
                        continue
                    else:
                        sibling = call_siblings(child,dimension,m,sib,child.DEPTH,write_handler_traverse,first_player,True)
                        if child.PLAYED == True:
                            if(child.DEPTH%2 == 0):
                                if len(child.SIB_UTIL) > 0:
                                    child.VALUE = min(child.SIB_UTIL) # IF min node take max of sibling
                            else:
                                if len(child.SIB_UTIL) > 0:
                                    child.VALUE = max(child.SIB_UTIL) #IF max node take min of sibling
                            
                            if child.VALUE == 200000000:
                                value = "Infinity"
                            elif child.VALUE == -200000000:
                                value = "-Infinity"    
                            else:
                                value = child.VALUE         
                            
                            write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) +  "\n",False)
                            
                            if child.CHILDREN.get(sibling.VALUE):
                                child.CHILDREN.get(sibling.VALUE).append(sibling.VALUE)
                            else:
                                child.CHILDREN.update({sibling.VALUE:[sibling]})
                                
                
                root.UTILITY_VALUE.append(child.VALUE)
                root.VALUE = max(root.UTILITY_VALUE)
                
                if root.VALUE == -200000000:
                    value = "-Infinity"
                elif root.VALUE == 200000000:
                    value = "Infinity"
                else:
                    value = root.VALUE   
                     
                write_line_to_file(write_handler_traverse, "root" + "," + str(0) + "," + str(value) + "\n",True)
            else:  
                root.UTILITY_VALUE.append(child.VALUE)
                root.VALUE = max(root.UTILITY_VALUE)
                
                if root.VALUE == -200000000:
                    value = "-Infinity"
                elif root.VALUE == 200000000:
                    value = "Infinity"
                else:
                    value = root.VALUE        
                write_line_to_file(write_handler_traverse, "root" + "," + str(0) + "," + str(value) + "\n",True)
            
            if root.CHILDREN.get(child.VALUE):
                root.CHILDREN.get(child.VALUE).append(child)
            else:
                root.CHILDREN.update({child.VALUE:[child]})
         
    compute_next_state(root,write_handler_next) 
    
def write_line_to_file(fileHandle, outString, deletePrevious):
    global posP, posC
    outString = outString.strip()+ "\n"
     
    deletePrevious = False
    if fileHandle.tell() == 0:
        fileHandle.write(outString)
        posC = fileHandle.tell()
        posP = 0
    else: 
        fileHandle.seek(posP)
        lastLine = fileHandle.read()
        if deletePrevious == True:
            if not lastLine == outString:
                fileHandle.write(outString)
                posP = posC
                posC = fileHandle.tell()
        else:
            fileHandle.write(outString)
            posP = posC
            posC = fileHandle.tell()       
    
def compute_next_state(root,write_handler_next):
    child = root.CHILDREN.get(root.VALUE)
    if len(child) > 0:
        best_child = child[0]
        if best_child.SELF_TURN == True:
            if root.VALUE in best_child.SIB_UTIL.keys():
                best_child = best_state(best_child,root.VALUE)   
            else:
                best_child = best_child
        else:
            best_child = child[0]

    dim  = len(best_child.BOARD[0])
    for ele in range(0,dim):
        write_handler_next.write(str(best_child.BOARD[0][ele]) + " ")
        
    write_handler_next.write("\n")
    for ele in range(0,dim):
        write_handler_next.write(str(best_child.BOARD[1][ele]) + " ")     
            
    write_handler_next.write("\n")
    write_handler_next.write(str(best_child.MANC.get('2')) + "\n")
    write_handler_next.write(str(best_child.MANC.get('1')) + "\n") 

def best_state(best_child,value):
    if best_child.SELF_TURN == True:
        if value in best_child.SIB_UTIL.keys():
            best_chi = best_child.SIB_UTIL[value]
            
            if len(best_chi[0].SIB_UTIL) == 0:
                best_val = best_chi[0]
                return best_val
            else:
                best_val = best_state(best_chi[0],value)
                return best_val
    return best_child        
                   
    
    
def play(root,board,first_player,dimension,m,n,isSibling,write_handler_traverse,comingFromSiblingsFunc):
    parent_board = root.BOARD
    board_pos = n+2
    mancala2 = root.MANC.get('2')
    mancala1 = root.MANC.get('1')
    minValue = "Infinity"
    maxValue = "-Infinity"
    value = None
    end_game = False
    if (m == 1):
        player = "B" + str(board_pos)
    else:
        player = "A" + str(board_pos)
    
    child = make_node(player,root.CUT_OFF,parent_board,mancala2,mancala1,dimension,[],-200000000,{},root.DEPTH,{},-100000000,100000000)
    
    points = child.BOARD[m][n]  
    points = int(points)         
    child.BOARD[m][n] = 0
            
    ''' calling distribute points''' 
    
    if points == 0:
        child.PLAYED = False
    else:
        child.PLAYED = True    
    
    if points != 0:
        self_turn,brd,mancala1,mancala2,end_game = distribute_points(points,m,n,child.BOARD,dimension,mancala1,mancala2)
        child.BOARD = brd 
        
        if self_turn == True:
            child.SELF_TURN = True
        else:
            child.SELF_TURN = False                   
            
        if isSibling:
            child.DEPTH = root.DEPTH
        else:    
            child.DEPTH = root.DEPTH + 1
            
        if child.DEPTH%2 == 0:
            child.VALUE = 200000000
        else:
            child.VALUE = -200000000            
            
        if m == 1:
            row = 0
        else:
            row = 1   
            
        child.MANC.update({'1':mancala1})
        child.MANC.update({'2':mancala2})    
            
        if int(child.DEPTH) < int(child.CUT_OFF) and end_game == False:
            
            ''' This piece of code is to set values while traversing down '''
            if child.DEPTH%2 == 0: #Updating Value                       
                if self_turn == True and end_game == False:
                    value = minValue
                elif self_turn == False and end_game == False:
                    value = maxValue   
                elif self_turn == False and end_game == True:
                    if ( first_player.get('m') == 1):
                        child.VALUE = mancala1 - mancala2
                    else:
                        child.VALUE = mancala2 - mancala1  
                else:
                    if ( first_player.get('m') == 1):
                        child.VALUE = mancala1 - mancala2
                    else:
                        child.VALUE = mancala2 - mancala1  
                                
                
            else: #Updating Value
                if self_turn == True and end_game == False:
                    value = maxValue
                elif self_turn == False and end_game == False:
                    value = minValue
                elif self_turn == False and end_game == True:
                    if ( first_player.get('m') == 1):
                        child.VALUE = mancala1 - mancala2
                    else:
                        child.VALUE = mancala2 - mancala1  
                else:
                    if ( first_player.get('m') == 1):
                        child.VALUE = mancala1 - mancala2
                    else:
                        child.VALUE = mancala2 - mancala1     
                                
            if root.PLAYER == child.PLAYER:
                write_line_to_file(write_handler_traverse, player + "," + str(child.DEPTH) + "," + str(value) +  "\n",False)
            else:
                write_line_to_file(write_handler_traverse, player + "," + str(child.DEPTH) + "," + str(value) +  "\n",True)    

            if self_turn:
                print(" ")
            else:
                for col in range(0,dimension):
                    chil = call_opponent(child,row,col,dimension,False,write_handler_traverse,first_player)
                    
                    ''' This is to update node after opponents have played'''
                    
                    if child.PLAYED == True:
                        if child.DEPTH%2 == 0:
                            if len(child.UTILITY_VALUE) > 0:
                                child.VALUE = max(child.UTILITY_VALUE) #Max Nodes choose max of children
                                value = child.VALUE
                                if child.VALUE == 200000000:
                                    value = "Infinity"
                                elif child.VALUE == -200000000:
                                    value = "-Infinity"    
                                else:
                                    value = child.VALUE    
                                          
                        else:
                            if len(child.UTILITY_VALUE) > 0:
                                child.VALUE =  min(child.UTILITY_VALUE) #min Nodes choose min of children
                                value = child.VALUE
                                if child.VALUE == 200000000:
                                    value = "Infinity"
                                elif child.VALUE == -200000000:
                                    value = "-Infinity"    
                                else:
                                    value = child.VALUE       
                                        
                            if child.VALUE == 200000000:
                                value = "Infinity"
                            elif child.VALUE == -200000000:
                                value = "-Infinity"    
                            else:
                                value = str(child.VALUE)
                        
                        if comingFromSiblingsFunc == True:
                            write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) +"\n",True)
                        else:
                            if (col != dimension-1 or child.DEPTH == 1) and chil.PLAYED == True:
                                write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "\n",True)
                                
        else:
            if ( first_player.get('m') == 1):
                child.VALUE = mancala1 - mancala2
            else:
                child.VALUE = mancala2 - mancala1
                                    
            if child.DEPTH%2 == 0:               
                if self_turn:
                    if child.VALUE == -200000000:
                        value = minValue
                    else:
                        value = child.VALUE    
                else:
                    if child.VALUE == -200000000:
                        value = maxValue
                    else:
                        value = child.VALUE        
            else:
                if self_turn:
                    if child.VALUE == 200000000:
                        value = minValue
                    else:
                        value = child.VALUE    
                else:
                    if child.VALUE == -200000000:
                        value = maxValue
                    else:
                        value = child.VALUE            
                        
            if end_game == True:            
                write_line_to_file(write_handler_traverse, player + "," + str(child.DEPTH) + "," + str(value) + "\n",True )
                         
    else:
        manc1 = root.MANC.get('1')
        manc2 = root.MANC.get('2')
    
        manc1 = int(manc1)
        manc2 = int(manc2)
        if ( first_player.get('m') == 1):
            child.VALUE = manc1 - manc2
        else:
            child.VALUE = manc2 - manc1 
        self_turn = False
        end_game = False
        child.PLAYED = False
        value = str(child.VALUE)
            
    return child,self_turn,value,end_game   

def distribute_points(points,m,n,board,dimension,mancala1,mancala2):
    points = int(points)
    mancala1 = int(mancala1)
    mancala2 = int(mancala2)
    self_turn = False
    end_game = False
    if m == 1: #player 1s coin distribution
        col_start = n + 1
        if n == dimension-1 and points != 0:  #Adding points to player 2 mancala
            points = points - 1
            mancala1 = mancala1 + 1
            
            if points == 0:
                self_turn = True
            
            if points != 0: #Updating Opponents Point
                row = 0    
                for col in range(dimension-1,-1,-1): # to be verified if value is decreasing
                    if ( points != 0):
                        points = points - 1      
                        board[row][col] = int(board[row][col]) + 1
            
            if points != 0:
                self_turn,board,mancala1,mancala2,end_game = distribute_points(points,m,-1,board,dimension,mancala1,mancala2)            
            
            if points == 0:
                end_game = check_end_game(board,True,True) 
                
            if end_game:
                for col in range(0,dimension): 
                    mancala2 = mancala2 + int(board[0][col])
                    mancala1 = mancala1 + int(board[1][col])
                    board[0][col] = 0      
                    board[1][col] = 0
        else:
            for col in range(col_start,dimension):
                if ( points != 0): #not tested
                    next_points = board[m][col] #check if its col or col+1
                    
                    if int(next_points) == 0 and points == 1: # Checking Empty Pit condition
                        if m == 1:
                            row = 0 #opponent row
                            bonus = int(board[row][col]) #opponent's pit
                            board[row][col] = 0
                            mancala1 = mancala1 + bonus
                            mancala1 = mancala1 + 1 #Because even the moved point should be added to bucket 
                    else:
                        board[m][col] = int(board[m][col]) + 1                 
                    points = points - 1
            
            if points != 0: #Adding points to player 1 mancala
                points = points - 1
                mancala1 = mancala1 + 1 
                if points == 0:
                    self_turn = True         
            
            if points != 0: #Updating Opponents Point
                row = 0   
                for n in range(dimension-1,-1,-1): # to be verified if value is decreasing
                    if ( points != 0):
                        points = points - 1
                        board[row][n] = int(board[row][n]) + 1  
                    
            if points != 0:
                self_turn,board,mancala1,mancala2,end_game = distribute_points(points,m,-1,board,dimension,mancala1,mancala2) 
                
            if points == 0:
                end_game = check_end_game(board,True,True) 
                    
            if end_game:
                for n in range(0,dimension): 
                    mancala2 = mancala2 + int(board[0][n])
                    mancala1 = mancala1 + int(board[1][n])
                    board[0][n] = 0      
                    board[1][n] = 0                                                      
    else: #Player 2 coins distribution
        col_start = n - 1
        if n == 0 and points != 0:  #Adding points to player 2 mancala
            points = points - 1
            mancala2 = mancala2 + 1
            
            if points == 0:
                self_turn = True
            
            if points != 0: #Updating Opponents Point
                row = 1    
                for col in range(0,dimension): # to be verified if value is decreasing
                    if ( points != 0):
                        points = points - 1      
                        board[row][col] = int(board[row][col]) + 1
            
            if points != 0:
                self_turn,board,mancala1,mancala2,end_game = distribute_points(points,m,dimension,board,dimension,mancala1,mancala2)            
            
            if points == 0:
                end_game = check_end_game(board,True,True) 
                
            if end_game:
                for col in range(0,dimension): 
                    mancala2 = mancala2 + int(board[0][col])
                    mancala1 = mancala1 + int(board[1][col])
                    board[0][col] = 0      
                    board[1][col] = 0   
        else:
            for col in range(col_start,-1,-1):
                next_points = board[m][col]    
                if ( points != 0):          
                    if int(next_points) == 0 and points == 1: # Checking Empty Pit condition
                        row = 1
                        bonus = int(board[row][col])
                        board[row][col] = 0
                        mancala2 = mancala2 + bonus
                        mancala2 = mancala2 + 1 #Even the moved point should be added to bucket 
                    else:
                        board[m][col] = int(board[m][col]) + 1        
                    points = points - 1                           
                    
            
            if points != 0: #Adding points to player 1 mancala
                points = points - 1
                mancala2 = mancala2 + 1 
                if points == 0:
                    self_turn = True                                    
                 
            if points != 0: #Updating Opponents Point
                row = 1    
                for col in range(0,dimension): # to be verified if value is decreasing
                    if ( points != 0):
                        points = points - 1
                        board[row][col] = int(board[row][col]) + 1                      
                    
            if points != 0:
                self_turn,board,mancala1,mancala2,end_game = distribute_points(points,m,dimension,board,dimension,mancala1,mancala2)            
            
            if points == 0:
                end_game = check_end_game(board,True,True) 
                
            if end_game:
                for col in range(0,dimension): 
                    mancala2 = mancala2 + int(board[0][col])
                    mancala1 = mancala1 + int(board[1][col])
                    board[0][col] = 0      
                    board[1][col] = 0   
    return self_turn,board,mancala1,mancala2,end_game

def check_end_game(board,end_game_1,end_game_2):
    for i in board[0]:
        if int(i) != 0:
            end_game_1 = False 
                
    for i in board[1]:
        if int(i) != 0:
            end_game_2 = False
                   
    return end_game_1 or end_game_2

def call_siblings(parent,dimension,m,n,depth,write_handler_traverse,first_player,fromPlayGame):
    oppo_played = False
    parentUpdated = False
    pred,self_turn,value,end_game = play(parent,parent.BOARD,first_player,dimension,m,n,True,write_handler_traverse,True)
    if pred.PLAYED == True:
            
        if pred.VALUE == 200000000:
            value = "Infinity"
        elif pred.VALUE == -200000000:
            value = "-Infinity"    
        else:
            value = pred.VALUE                            
            
        if self_turn and end_game == False: 
            for sib in range(0,dimension):
                if sib == 0:
                    if pred.DEPTH%2 == 0:
                        value = "Infinity"
                    else:
                        value = "-Infinity" 
                else:
                    for i in range(0,sib):
                        if pred.BOARD[m][i] != 0:
                            parentUpdated = True #Previous Siblings are having 0 points so parent value should be Inf or -Inf 
                    if parentUpdated == False:
                        if pred.DEPTH%2 == 0:
                            value = "Infinity"
                        else:
                            value = "-Infinity" 
                    else:                    
                        value = pred.VALUE 
                    
                if (sib == n and pred.BOARD[m][sib] == 0) or pred.BOARD[m][sib] == 0:
                    continue
                else:
                    if sib == n or int(pred.DEPTH) == int(pred.CUT_OFF):
                        write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) + "\n", False)
                    else:
                        write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) + "\n", True)
                                
                    
                    sibling = call_siblings(pred,dimension,m,sib,pred.DEPTH,write_handler_traverse,first_player,False)
                    
                    if(pred.DEPTH%2 == 0):
                        if len(pred.SIB_UTIL) > 0:
                            pred.VALUE = min(pred.SIB_UTIL.keys()) # IF max node take min of sibling
                            parent.UTILITY_VALUE.append(pred.VALUE)
                            parent.SIB_UTIL.update({pred.VALUE:[pred]})
                                
                            if pred.VALUE == 200000000:
                                value = "Infinity"
                            elif pred.VALUE == -200000000:
                                value = "-Infinity"    
                            else:
                                value = pred.VALUE 
                            
                    else:
                        if len(pred.SIB_UTIL) > 0 :
                            pred.VALUE = max(pred.SIB_UTIL.keys()) #IF max node take min of sibling
                            parent.UTILITY_VALUE.append(pred.VALUE)
                            parent.SIB_UTIL.update({pred.VALUE:[pred]})
                                
                            if pred.VALUE == 200000000:
                                value = "Infinity"
                            elif pred.VALUE == -200000000:
                                value = "-Infinity"    
                            else:
                                value = pred.VALUE    
                        
                    if parent.SIB_UTIL.get(pred.VALUE):
                        if sibling.VALUE == pred.VALUE:
                            parent.SIB_UTIL.get(pred.VALUE).append(pred)
                    else:
                        parent.SIB_UTIL.update({pred.VALUE:[pred]})  
                        
        else: 
            if parent.SIB_UTIL.get(pred.VALUE):
                parent.SIB_UTIL.get(pred.VALUE).append(pred)
            else:
                parent.SIB_UTIL.update({pred.VALUE:[pred]})
        
        
        write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) +"\n",True)        
        
        oppo_played = True
        
        if m == 1:
            row = 0
        else:
            row = 1   
        
        if int(pred.DEPTH) < int(pred.CUT_OFF) and oppo_played == False:
            oppo_played = True
            for col in range(0,dimension):
                chil = call_opponent(pred,row,col,dimension,False,write_handler_traverse,first_player)
                ''' This is to update node after opponents have played'''
                if pred.PLAYED == True:
                    if pred.DEPTH%2 == 0:
                        if len(pred.UTILITY_VALUE) > 0:
                            pred.VALUE = max(pred.UTILITY_VALUE) #Max Nodes choose max of children
                            
                            if pred.VALUE == 200000000:
                                value = "Infinity"
                            elif pred.VALUE == -200000000:
                                value = "-Infinity"    
                            else:
                                value = pred.VALUE        
                    else:
                        if len(pred.UTILITY_VALUE) > 0:
                            pred.VALUE =  min(pred.UTILITY_VALUE) #min Nodes choose min of predren
                                
                            if pred.VALUE == 200000000:
                                value = "Infinity"
                            elif pred.VALUE == -200000000:
                                value = "-Infinity"    
                            else:
                                value = pred.VALUE    
                        
                    if pred.VALUE == 200000000:
                        value = "Infinity"
                    elif pred.VALUE == -200000000:
                        value = "-Infinity"    
                    else:
                        value = pred.VALUE      
                    
                    write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) + "\n",True)
                       
    return pred   

def call_opponent(parent,m,n,dimension,isSibling,write_handler_traverse,first_player):
    parentUpdated = False
    child,self_turn,value,end_game = play(parent,parent.BOARD,first_player,dimension,m,n,isSibling,write_handler_traverse,False)
    if child.PLAYED == True:            
        if child.VALUE == 200000000:
            value = "Infinity"
        elif child.VALUE == -200000000:
            value = "-Infinity"    
        else:
            value = child.VALUE    
                     
        if self_turn and end_game == False:
            for sib in range(0,dimension):
                if sib == 0:
                    if child.DEPTH%2 == 0:
                        value = "Infinity"
                    else:
                        value = "-Infinity" 
                else:
                    for i in range(0,sib):
                        if child.BOARD[m][i] != 0:
                            parentUpdated = True #Previous Siblings are having 0 points so parent value should be Inf or -Inf 
                    if parentUpdated == False:
                        if child.DEPTH%2 == 0:
                            value = "Infinity"
                        else:
                            value = "-Infinity" 
                    else:                    
                        value = child.VALUE
                                                 
                if (sib == n and child.BOARD[m][sib] == 0) or child.BOARD[m][sib] == 0:
                    continue
                else:
                    if sib == n or int(child.DEPTH) == int(child.CUT_OFF):
                        write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "\n", False)
                    else:
                        write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "\n", True)
                    
                    sibl = call_siblings(child,dimension,m,sib,child.DEPTH,write_handler_traverse,first_player,False)
                    
                    if child.PLAYED == True:            
                        if(child.DEPTH%2 == 0):
                            if len(child.SIB_UTIL) > 0:
                                child.VALUE = min(child.SIB_UTIL.keys()) # IF max node take min of sibling
                                parent.UTILITY_VALUE.append(child.VALUE)
                                parent.SIB_UTIL.update({child.VALUE:[child]})
                                
                                if child.VALUE == 200000000:
                                    value = "Infinity"
                                elif child.VALUE == -200000000:
                                    value = "-Infinity"
                                else:
                                    value = child.VALUE            
                            
                        else:
                            if len(child.SIB_UTIL) > 0 :
                                child.VALUE = max(child.SIB_UTIL.keys()) #IF max node take min of sibling
                                parent.UTILITY_VALUE.append(child.VALUE)
                                parent.SIB_UTIL.update({child.VALUE:[child]})                                
                                
                                if child.VALUE == 200000000:
                                    value = "Infinity"
                                elif child.VALUE == -200000000:
                                    value = "-Infinity"    
                                else:
                                    value = child.VALUE
                            
                        write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "\n",False)   
        else:
            parent.UTILITY_VALUE.append(child.VALUE)
            parent.CHILDREN.update({child.VALUE:[child]})
            write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "\n",True)
                    
    return child

def play_alphaBeta_game(root,first_player,dimension,write_handler_traverse,write_handler_next):
    n = first_player.get("n")
    m = first_player.get("m")
    alpha = None
    beta = None
    write_line_to_file(write_handler_traverse, "Node" + "," + "Depth" +"," + "Value" + "," +"Alpha" + "," + "Beta" + "\n",True)
    write_line_to_file(write_handler_traverse, "root" + "," + str(0) + "," + "-Infinity" + "," + "-Infinity" + "," + "Infinity" + "\n",True)
    for n in range(0,dimension):
        print(" ")
        child,self_turn,value,end_game = play_alphaBeta(root,root.BOARD,first_player,dimension,m,n,False,write_handler_traverse,False)
        if child.PLAYED == True:
            if end_game == True:
                if child.BETA == 100000000:
                    beta = "Infinity"
                else:
                    beta = child.BETA    
                if child.ALPHA == -100000000:
                    alpha = "-Infinity"
                else:
                    alpha = child.ALPHA        
                
            if self_turn and end_game == False: #calling siblings
                for sib in range(0,dimension):
                    if (sib == n and child.BOARD[m][sib] == 0) or child.BOARD[m][sib] == 0:
                        continue
                    else:
                        sibling = call_alphaBeta_siblings(child,dimension,m,sib,child.DEPTH,write_handler_traverse,first_player,True)
                        if child.PLAYED == True:
                            if(child.DEPTH%2 == 0):
                                if len(child.SIB_UTIL) > 0:
                                    child.VALUE = min(child.SIB_UTIL) # IF min node take max of sibling
                                    if child.BETA > child.VALUE:
                                        child.BETA = child.VALUE
                                    root.ALPHA = -100000000
                            else:
                                if len(child.SIB_UTIL) > 0:
                                    child.VALUE = max(child.SIB_UTIL) #IF max node take min of sibling
                                    if child.ALPHA < child.VALUE:
                                        child.ALPHA = child.VALUE
                                    root.BETA = 100000000
                            
                            if child.BETA == 100000000:
                                beta = "Infinity" 
                            else:
                                beta = child.BETA     
                            
                            if child.ALPHA == -100000000:
                                alpha = "-Infinity"
                            else:
                                alpha = child.ALPHA  
                            
                            if child.VALUE == 200000000:
                                value = "Infinity"
                            elif child.VALUE == -200000000:
                                value = "-Infinity"    
                            else:
                                value = child.VALUE         
                            
                            write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha) + "," + str(beta)+ "\n",False)
                            
                            if child.CHILDREN.get(sibling.VALUE):
                                child.CHILDREN.get(sibling.VALUE).append(sibling.VALUE)
                            else:
                                child.CHILDREN.update({sibling.VALUE:[sibling]})
                                
                
                root.UTILITY_VALUE.append(child.VALUE)
                root.VALUE = max(root.UTILITY_VALUE)
                
                if root.VALUE == -200000000:
                    value = "-Infinity"
                elif root.VALUE == 200000000:
                    value = "Infinity"
                else:
                    value = root.VALUE   
                
                root.BETA = 100000000
                if root.BETA == 100000000:
                    beta = "Infinity"
                else:
                    beta = root.BETA      
                
                if root.ALPHA < root.VALUE:
                    root.ALPHA = root.VALUE
                if root.ALPHA == -100000000:
                    alpha = "-Infinity" 
                else:
                    alpha = root.ALPHA   
                     
                write_line_to_file(write_handler_traverse, "root" + "," + str(0) + "," + str(value) + "," + str(alpha) + "," + str(beta) + "\n",True)
            else:  
                root.UTILITY_VALUE.append(child.VALUE)
                root.VALUE = max(root.UTILITY_VALUE)
                
                if root.VALUE == -200000000:
                    value = "-Infinity"
                elif root.VALUE == 200000000:
                    value = "Infinity"
                else:
                    value = root.VALUE        
                
                root.BETA = 100000000
                
                if root.BETA == 100000000:
                    beta = "Infinity"
                else:
                    beta = root.BETA         
                
                if root.ALPHA < root.VALUE:
                    root.ALPHA = root.VALUE
                
                if root.ALPHA == -100000000:
                    alpha = "-Infinity" 
                else:
                    alpha = root.ALPHA     
                write_line_to_file(write_handler_traverse, "root" + "," + str(0) + "," + str(value) + "," + str(alpha) + "," + str(beta) + "\n",True)
            
            if root.CHILDREN.get(child.VALUE):
                root.CHILDREN.get(child.VALUE).append(child)
            else:
                root.CHILDREN.update({child.VALUE:[child]})
         
    compute_next_state(root,write_handler_next) 

def play_alphaBeta(root,board,first_player,dimension,m,n,isSibling,write_handler_traverse,comingFromSiblingsFunc):
    parent_board = root.BOARD
    board_pos = n+2
    mancala2 = root.MANC.get('2')
    mancala1 = root.MANC.get('1')
    minValue = "Infinity"
    maxValue = "-Infinity"
    beta = None
    alpha = None
    value = None
    end_game = False
    if (m == 1):
        player = "B" + str(board_pos)
    else:
        player = "A" + str(board_pos)
    
    child = make_node(player,root.CUT_OFF,parent_board,mancala2,mancala1,dimension,[],-200000000,{},root.DEPTH,{},-100000000,100000000)
    
    points = child.BOARD[m][n]  
    points = int(points)         
    child.BOARD[m][n] = 0
            
    ''' calling distribute points''' 
    
    if points == 0:
        child.PLAYED = False
    else:
        child.PLAYED = True    
    
    if points != 0:
        self_turn,brd,mancala1,mancala2,end_game = distribute_points(points,m,n,child.BOARD,dimension,mancala1,mancala2)
        child.BOARD = brd 
        
        if self_turn == True:
            child.SELF_TURN = True
        else:
            child.SELF_TURN = False                  
            
        if isSibling:
            child.DEPTH = root.DEPTH
        else:    
            child.DEPTH = root.DEPTH + 1
            
        if child.DEPTH%2 == 0:
            child.VALUE = 200000000
        else:
            child.VALUE = -200000000            
            
        if m == 1:
            row = 0
        else:
            row = 1   
            
        child.MANC.update({'1':mancala1})
        child.MANC.update({'2':mancala2})    
            
        if int(child.DEPTH) < int(child.CUT_OFF) and end_game == False:
            
            ''' This piece of code is to set values while traversing down '''
            if child.DEPTH%2 == 0: #Updating Beta at max Nodes                       
                if root.BETA == 100000000 and root.ALPHA == -100000000:
                    alpha = maxValue
                    beta = minValue
                    if self_turn:
                        value = minValue
                    else:
                        value = maxValue    
                else:
                    child.ALPHA = root.ALPHA     
                    if child.ALPHA == -100000000:
                        alpha = maxValue
                    else:
                        alpha = child.ALPHA      
    
                    child.BETA = root.BETA
                    
                    if child.BETA == 100000000:
                        beta = minValue
                    else:
                        beta = child.BETA
                    
                    
                    if self_turn:
                        value = minValue
                    else:
                        value = maxValue        
                
            else: #Updating Alpha value at min nodes
                if root.ALPHA == -100000000 and root.BETA == 100000000: # 1st level leftmost node
                    alpha = maxValue
                    beta = minValue 
                    if self_turn:
                        value = maxValue #Behave like max node
                    else:
                        value = minValue
                else:
                    child.ALPHA = root.ALPHA 
                    if child.ALPHA == -100000000:
                        alpha = maxValue
                    else:
                        alpha = child.ALPHA
                    child.BETA = root.BETA
                    if child.BETA == 100000000:
                        beta = minValue
                    else:    
                        beta = child.BETA  
                    if self_turn:
                        value = maxValue
                    else:
                        value = minValue            
            
            if root.PLAYER == child.PLAYER:
                write_line_to_file(write_handler_traverse, player + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha) + "," + str(beta) + "\n",False)
            else:
                write_line_to_file(write_handler_traverse, player + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha) + "," + str(beta) + "\n",True)


            if self_turn:
                print(" ")
            else:
                for col in range(0,dimension):
                    chil = call_alphaBeta_opponent(child,row,col,dimension,False,write_handler_traverse,first_player)
                    
                    ''' This is to update node after opponents have played'''
                    
                    if child.PLAYED == True:
                        if child.DEPTH%2 == 0:
                            if len(child.UTILITY_VALUE) > 0:
                                child.VALUE = max(child.UTILITY_VALUE) #Max Nodes choose max of children
                                value = child.VALUE
                                if child.VALUE >= child.BETA: #Pruning
                                    if len(child.UTILITY_VALUE) > 0:
                                        child.UTILITY_VALUE.remove(chil.VALUE)
                                        if len(child.UTILITY_VALUE) == 0:
                                            child.ALPHA = child.ALPHA
                                    else:
                                        child.ALPHA = child.ALPHA
                                    
                                    if child.ALPHA == -100000000:
                                        alpha = "-Infinity"
                                    else:
                                        alpha = child.ALPHA
                                        
                                    if child.BETA == 100000000:
                                        beta = "Infinity"
                                    else:
                                        beta = child.BETA    
            
                                    if child.VALUE == 200000000:
                                        value = "Infinity"
                                    elif child.VALUE == -200000000:
                                        value = "-Infinity"    
                                    else:
                                        value = child.VALUE    
                                          
                                    if child.DEPTH == 1: #TO be tested. Assumption only nodes at level 1 needs to be printed here      
                                        write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) +"\n",True)
                                    return child,self_turn,value,end_game    
                                else:
                                    if child.ALPHA < child.VALUE:
                                        if len(child.UTILITY_VALUE) > 0:
                                            child.ALPHA = max(child.UTILITY_VALUE) #Update Alpha
                                    if child.ALPHA == -100000000:
                                        alpha = "-Infinity"
                                    else:
                                        alpha = child.ALPHA          
                        else:
                            if len(child.UTILITY_VALUE) > 0:
                                child.VALUE =  min(child.UTILITY_VALUE) #min Nodes choose min of children
                                value = child.VALUE
                                if child.VALUE <= child.ALPHA: #Pruning
                                    if len(child.UTILITY_VALUE) > 0: # 1 because left most child's value is reqd for computing beta
                                        child.UTILITY_VALUE.remove(chil.VALUE)
                                        if len(child.UTILITY_VALUE) == 0:
                                            child.BETA = child.BETA
                                    else:
                                        child.BETA = child.BETA
                                        
                                    if child.BETA == 100000000:
                                        beta = "Infinity"
                                    else:
                                        beta = child.BETA  
                                    
                                    if child.ALPHA == -100000000:
                                        alpha = "-Infinity"
                                    else:
                                        alpha = child.ALPHA      
                                        
                                    if child.VALUE == 200000000:
                                        value = "Infinity"
                                    elif child.VALUE == -200000000:
                                        value = "-Infinity"    
                                    else:
                                        value = child.VALUE       
                                    
                                    if child.DEPTH == 1: #TO be tested. Assumption only nodes at level 1 needs to be printed here                                     
                                        write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha) + "," + str(beta) +"\n",True)
                                    return child,self_turn,value,end_game
                                else:
                                    if child.BETA > child.VALUE:
                                        if len(child.UTILITY_VALUE) > 0:
                                            child.BETA = min(child.UTILITY_VALUE) #Update Beta, check with mancala
                                    if child.BETA == 100000000:
                                        beta = "Infinity"
                                    else:
                                        beta = child.BETA
                            
                            if child.BETA == 100000000:
                                beta = "Infinity"
                            else:
                                beta = child.BETA  
                                    
                            if child.ALPHA == -100000000:
                                alpha = "-Infinity"
                            else:
                                alpha = child.ALPHA      
                                        
                            if child.VALUE == 200000000:
                                value = "Infinity"
                            elif child.VALUE == -200000000:
                                value = "-Infinity"    
                            else:
                                value = str(child.VALUE)
                        
                        if comingFromSiblingsFunc == True:
                            write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) +"\n",True)
                        else:
                            if (col != dimension-1 or child.DEPTH == 1) and chil.PLAYED == True:
                                write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) +"\n",True)
                                
        else:
            if ( first_player.get('m') == 1):
                child.VALUE = mancala1 - mancala2
            else:
                child.VALUE = mancala2 - mancala1
                                    
            if child.DEPTH%2 == 0:         #At max nodes updating Beta value from parent               
                if root.BETA == 100000000 and root.ALPHA == -100000000:
                    alpha = maxValue
                    beta = minValue
                    if self_turn:
                        if child.VALUE == -200000000:
                            value = minValue
                        else:
                            value = child.VALUE    
                    else:
                        if child.VALUE == -200000000:
                            value = maxValue
                        else:
                            value = child.VALUE        
                else:
                    child.ALPHA = root.ALPHA
                    
                    if child.ALPHA == -100000000:
                        alpha = "-Infinity"
                    else:
                        alpha = child.ALPHA
                          
                    child.BETA = root.BETA
                    
                    if child.BETA == 100000000:
                        beta = "Infinity"
                    else:    
                        beta = child.BETA 
                   
                    if self_turn:
                        if child.VALUE == -200000000:
                            value = minValue
                        else:
                            value = child.VALUE    
                    else:
                        if child.VALUE == -200000000:
                            value = maxValue
                        else:
                            value = child.VALUE            
                
            else: #At min node updating Alpha value from parent.
                if root.ALPHA == -100000000 and root.BETA == 100000000: # 1st level leftmost node
                    alpha = maxValue
                    beta = minValue 
                    if self_turn:
                        if child.VALUE == 200000000:
                            value = maxValue #Behave like max node
                        else:
                            value = child.VALUE    
                    else:
                        if child.VALUE == 200000000:
                            value = minValue
                        else:
                            value = child.VALUE    
                else:
                    child.ALPHA = root.ALPHA
                    if child.ALPHA == -100000000:
                        alpha = "-Infinity"
                    else:
                        alpha = child.ALPHA
                     
                     
                    child.BETA = root.BETA
                    
                    if child.BETA == 100000000:
                        beta = "Infinity"
                    else:    
                        beta = child.BETA 
                   
                    if self_turn:
                        if child.VALUE == -200000000:
                            value = minValue
                        else:
                            value = child.VALUE    
                    else:
                        if child.VALUE == -200000000:
                            value = maxValue
                        else:
                            value = child.VALUE   
                        
            if end_game == True:            
                write_line_to_file(write_handler_traverse, player + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha) + "," + str(beta) + "\n",True )
                         
    else:
        manc1 = root.MANC.get('1')
        manc2 = root.MANC.get('2')
    
        manc1 = int(manc1)
        manc2 = int(manc2)
        if ( first_player.get('m') == 1):
            child.VALUE = manc1 - manc2
        else:
            child.VALUE = manc2 - manc1 
        self_turn = False
        end_game = False
        child.PLAYED = False
        value = str(child.VALUE)
            
    return child,self_turn,value,end_game

def call_alphaBeta_siblings(parent,dimension,m,n,depth,write_handler_traverse,first_player,fromPlayGame):
    oppo_played = False
    parentUpdated = False
    pred,self_turn,value,end_game = play_alphaBeta(parent,parent.BOARD,first_player,dimension,m,n,True,write_handler_traverse,True)
    if pred.PLAYED == True:
        if pred.ALPHA == -100000000:
            alpha = "-Infinity"
        else:
            pred.ALPHA = pred.ALPHA
            
        if pred.BETA == 100000000:
            beta = "Infinity"
        else:
            pred.BETA = pred.BETA
                
        if pred.ALPHA == -100000000:
            alpha = "-Infinity"
        else:
            alpha = pred.ALPHA
            
        if pred.BETA == 100000000:
            beta = "Infinity"
        else:
            beta = pred.BETA    
            
        if pred.VALUE == 200000000:
            value = "Infinity"
        elif pred.VALUE == -200000000:
            value = "-Infinity"    
        else:
            value = pred.VALUE                            
            
        if self_turn and end_game == False: 
            for sib in range(0,dimension):
                if sib == 0:
                    if pred.DEPTH%2 == 0:
                        value = "Infinity"
                    else:
                        value = "-Infinity" 
                else:
                    for i in range(0,sib):
                        if pred.BOARD[m][i] != 0:
                            parentUpdated = True #Previous Siblings are having 0 points so parent value should be Inf or -Inf 
                    if parentUpdated == False:
                        if pred.DEPTH%2 == 0:
                            value = "Infinity"
                        else:
                            value = "-Infinity" 
                    else:                    
                        value = pred.VALUE 
                    
                if (sib == n and pred.BOARD[m][sib] == 0) or pred.BOARD[m][sib] == 0:
                    continue
                else:
                    if sib == n or int(pred.DEPTH) == int(pred.CUT_OFF):
                        write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) +"\n",False)
                    else:
                        write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) +"\n",True)
                    
                    sibling = call_alphaBeta_siblings(pred,dimension,m,sib,pred.DEPTH,write_handler_traverse,first_player,False)
                    
                    if(pred.DEPTH%2 == 0):
                            if len(pred.SIB_UTIL) > 0:
                                pred.VALUE = min(pred.SIB_UTIL.keys()) # IF max node take min of sibling
                                parent.UTILITY_VALUE.append(pred.VALUE)
                                parent.SIB_UTIL.update({pred.VALUE:[pred]})
                                
                                if pred.ALPHA == -100000000:
                                    alpha = "-Infinity"
                                else:
                                    alpha = pred.ALPHA
                                 
                                if pred.BETA == 100000000:
                                    beta = "Infinity"
                                else:
                                    beta = pred.BETA
                                
                                if pred.VALUE == 200000000:
                                    value = "Infinity"
                                elif pred.VALUE == -200000000:
                                    value = "-Infinity"    
                                else:
                                    value = pred.VALUE 
                                
                                if pred.VALUE <= pred.ALPHA: #In sibling method conditon of pruning reverses
                                    write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) + "," + str(alpha) + "," + str(beta) + "\n",True)   
                                    return pred
                                else:    
                                    if pred.BETA > pred.VALUE:
                                        pred.BETA = pred.VALUE
                                    if pred.BETA == 100000000:
                                        beta = "Infinity"
                                    else:
                                        beta = pred.BETA
                            
                    else:
                        if len(pred.SIB_UTIL) > 0 :
                            pred.VALUE = max(pred.SIB_UTIL.keys()) #IF max node take min of sibling
                            parent.UTILITY_VALUE.append(pred.VALUE)
                            parent.SIB_UTIL.update({pred.VALUE:[pred]})
                            
                            if pred.ALPHA == -100000000:
                                alpha = "-Infinity"
                            else:
                                alpha = pred.ALPHA
                             
                            if pred.BETA == 100000000:
                                beta = "Infinity"
                            else:
                                beta = pred.BETA
                                
                            if pred.VALUE == 200000000:
                                value = "Infinity"
                            elif pred.VALUE == -200000000:
                                value = "-Infinity"    
                            else:
                                value = pred.VALUE    
                            
                            if pred.VALUE >= pred.BETA: #In sibling method conditon of pruning reverses
                                write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) + "," + str(alpha) + "," + str(beta) + "\n",True)   
                                return pred
                            else:    
                                if pred.ALPHA < pred.VALUE:
                                    pred.ALPHA = pred.VALUE
                                if pred.ALPHA == -100000000:
                                    alpha = "-Infinity"
                                else:
                                    alpha = pred.ALPHA
                        
                    if parent.SIB_UTIL.get(pred.VALUE):
                        if sibling.VALUE == pred.VALUE:
                            parent.SIB_UTIL.get(pred.VALUE).append(pred)
                    else:
                        parent.SIB_UTIL.update({pred.VALUE:[pred]})  
                        
        else: 
            if parent.SIB_UTIL.get(pred.VALUE):
                parent.SIB_UTIL.get(pred.VALUE).append(pred)
            else:
                parent.SIB_UTIL.update({pred.VALUE:[pred]})
        
        
        write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) +"\n",True)        
        
        oppo_played = True
        
        if m == 1:
            row = 0
        else:
            row = 1   
        
        if int(pred.DEPTH) < int(pred.CUT_OFF) and oppo_played == False:
            oppo_played = True
            for col in range(0,dimension):
                chil = call_alphaBeta_opponent(pred,row,col,dimension,False,write_handler_traverse,first_player)
                ''' This is to update node after opponents have played'''
                if pred.PLAYED == True:
                    if pred.DEPTH%2 == 0:
                        if len(pred.UTILITY_VALUE) > 0:
                            pred.VALUE = max(pred.UTILITY_VALUE) #Max Nodes choose max of children
                            if pred.ALPHA == -100000000 or pred.ALPHA < pred.VALUE:
                                pred.ALPHA = pred.VALUE #Update Alpha
                            
                            if pred.ALPHA == -100000000:
                                alpha = "-Infinity"
                            else:
                                alpha = pred.ALPHA
                                 
                            if pred.BETA == 100000000:
                                beta = "Infinity"
                            else:
                                beta = pred.BETA
                            
                            if pred.VALUE == 200000000:
                                value = "Infinity"
                            elif pred.VALUE == -200000000:
                                value = "-Infinity"    
                            else:
                                value = pred.VALUE        
                                       
                            if pred.VALUE >= pred.BETA: #Pruning
                                write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) +"\n",True)
                                return pred
                    else:
                        if len(pred.UTILITY_VALUE) > 0:
                            pred.VALUE =  min(pred.UTILITY_VALUE) #min Nodes choose min of predren
                            if pred.BETA == 100000000 or pred.BETA > pred.VALUE:
                                pred.BETA = pred.VALUE #Update Beta, check with mancala
                            else:
                                print(" ")  
                                
                            if pred.ALPHA == -100000000:
                                alpha = "-Infinity"
                            else:
                                alpha = pred.ALPHA
                                 
                            if pred.BETA == 100000000:
                                beta = "Infinity"
                            else:
                                beta = pred.BETA
                                
                            if pred.VALUE == 200000000:
                                value = "Infinity"
                            elif pred.VALUE == -200000000:
                                value = "-Infinity"    
                            else:
                                value = pred.VALUE    
                                      
                            if pred.VALUE <= pred.ALPHA: #Pruning
                                write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) +"\n",True)
                                return pred
                            
                    if pred.ALPHA == -100000000:
                        alpha = "-Infinity"
                    else:
                        alpha = pred.ALPHA
                                 
                    if pred.BETA == 100000000:
                        beta = "Infinity"
                    else:
                        beta = pred.BETA  
                        
                    if pred.VALUE == 200000000:
                        value = "Infinity"
                    elif pred.VALUE == -200000000:
                        value = "-Infinity"    
                    else:
                        value = pred.VALUE      
                    
                    write_line_to_file(write_handler_traverse, pred.PLAYER + "," + str(pred.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) +"\n",True)
                       
    return pred   

def call_alphaBeta_opponent(parent,m,n,dimension,isSibling,write_handler_traverse,first_player):
    alpha = None
    beta = None 
    parentUpdated = False
    child,self_turn,value,end_game = play_alphaBeta(parent,parent.BOARD,first_player,dimension,m,n,isSibling,write_handler_traverse,False)
    if child.PLAYED == True:
        if child.ALPHA == -100000000:
            alpha = "-Infinity"
        else:
            alpha = child.ALPHA
            
        if child.BETA == 100000000:
            beta = "Infinity"
        else:
            beta = child.BETA    
            
        if child.VALUE == 200000000:
            value = "Infinity"
        elif child.VALUE == -200000000:
            value = "-Infinity"    
        else:
            value = child.VALUE    
                     
        if self_turn and end_game == False:
            for sib in range(0,dimension):
                if sib == 0:
                    if child.DEPTH%2 == 0:
                        value = "Infinity"
                    else:
                        value = "-Infinity" 
                else:
                    for i in range(0,sib):
                        if child.BOARD[m][i] != 0:
                            parentUpdated = True #Previous Siblings are having 0 points so parent value should be Inf or -Inf 
                    if parentUpdated == False:
                        if child.DEPTH%2 == 0:
                            value = "Infinity"
                        else:
                            value = "-Infinity" 
                    else:                    
                        value = child.VALUE
                
                if beta != str(child.BETA): #Dirty Fix
                    beta = str(child.BETA)
                
                if child.ALPHA == -100000000:
                    alpha = "-Infinity"
                else:
                    alpha = child.ALPHA
                    
                if child.BETA == 100000000:
                    beta = "Infinity"
                else:
                    beta = child.BETA    
                                 
                if (sib == n and child.BOARD[m][sib] == 0) or child.BOARD[m][sib] == 0:
                    continue
                else:
                    if sib == n or int(child.DEPTH) == int(child.CUT_OFF):
                        write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) +"\n",False)
                    else:
                        write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) +"\n",True)
                    sibl = call_alphaBeta_siblings(child,dimension,m,sib,child.DEPTH,write_handler_traverse,first_player,False)
                    
                    if child.PLAYED == True:            
                        if(child.DEPTH%2 == 0):
                            if len(child.SIB_UTIL) > 0:
                                child.VALUE = min(child.SIB_UTIL.keys()) # IF max node take min of sibling
                                parent.UTILITY_VALUE.append(child.VALUE)
                                parent.SIB_UTIL.update({child.VALUE:[child]})
                                
                                if child.ALPHA == -100000000:
                                    alpha = "-Infinity"
                                else:
                                    alpha = child.ALPHA
                                 
                                if child.BETA == 100000000:
                                    beta = "Infinity"
                                else:
                                    beta = child.BETA
                                    
                                if child.VALUE == 200000000:
                                    value = "Infinity"
                                elif child.VALUE == -200000000:
                                    value = "-Infinity"
                                else:
                                    value = child.VALUE            
                                
                                if child.VALUE <= child.ALPHA: #In sibling method conditon of pruning reverses
                                    write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha) + "," + str(beta) + "\n",True)   
                                    return child
                                else:    
                                    if child.BETA > child.VALUE:
                                        child.BETA = child.VALUE   
                                    if child.BETA == 100000000:
                                        beta = "Infinity"
                                    else:
                                        beta = child.BETA
                            
                        else:
                            if len(child.SIB_UTIL) > 0 :
                                child.VALUE = max(child.SIB_UTIL.keys()) #IF max node take min of sibling
                                parent.UTILITY_VALUE.append(child.VALUE)
                                parent.SIB_UTIL.update({child.VALUE:[child]})
                                
                                if child.ALPHA == -100000000:
                                    alpha = "-Infinity"
                                else:
                                    alpha = child.ALPHA
                                 
                                if child.BETA == 100000000:
                                    beta = "Infinity"
                                else:
                                    beta = child.BETA
                                
                                if child.VALUE == 200000000:
                                    value = "Infinity"
                                elif child.VALUE == -200000000:
                                    value = "-Infinity"    
                                else:
                                    value = child.VALUE
                            
                                if child.VALUE >= child.BETA: #In sibling method conditon of pruning reverses
                                    write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha) + "," + str(beta) + "\n",True)   
                                    return child
                                else:    
                                    if child.ALPHA < child.VALUE:
                                        child.ALPHA = child.VALUE
                                    if child.ALPHA == -100000000:
                                        alpha = "-Infinity"
                                    else:
                                        alpha = child.ALPHA
                            
            write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) + "\n",False)   
        else:
            parent.UTILITY_VALUE.append(child.VALUE)
            parent.CHILDREN.update({child.VALUE:[child]})
            write_line_to_file(write_handler_traverse, child.PLAYER + "," + str(child.DEPTH) + "," + str(value) + "," + str(alpha)+ "," + str(beta) + "\n",True)
                    
    return child
    
file_handler = open("input.txt")
read_write_file(file_handler)
file_handler.close()