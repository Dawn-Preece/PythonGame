# Libraries ==================================================================
import time
import random
import colorama
colorama.init()

# Variables and Constants ====================================================
DELAY = 3

loc = 'start'
stage = 'house'
active = True
timer = -1

bedroom_key = False
gate_key = False
can_find_map = False

has_map = False

sticks = False
flint = False
steel = False

shed_lock_uses = 0
alt_stage = 0
maze_fails = 0

shed_code = [] # Random code
for _ in range (4):
    shed_code.append (str(random.randint(0, 9)))

forest_code = ''
for _ in range (5):
    forest_code += random.choice(['^', 'v', '<', '>'])

notes = ''

# Rooms and Subroutines ======================================================
def choice (prompt): # not broken
    global notes
    global stage
    global bedroom_key
    global gate_key

    b = True
    while b:
        string = input (colorama.Fore.YELLOW + prompt + colorama.Style.RESET_ALL).strip ().lower ()
        if string:
            if string[0] == '/':
                cmd = string.split(' ')

                if cmd[0] in ['/n', '/note', '/notes']:
                    if len (cmd) > 1:
                        notes += ' '.join(cmd[1:]) + '\n'
                        print ('Added a line to the notepad.')
                    else:
                        print ('You must specify text to write to the notepad.')
                elif cmd[0] in ['/r', '/read']:
                    if notes:
                        print (notes)
                    else:
                        print ("You haven't written any notes yet.\n")
                elif cmd[0] in ['/i', '/inv']:
                    match stage:
                        case 'house':
                            if bedroom_key and not gate_key:
                                print ('You have 1 key.')
                            elif bedroom_key and gate_key:
                                print ('You have 2 different keys.')
                            else:
                                print ('You have no items.')
                        case 'forest':
                            print ('This area has no items to collect.')
                        case 'cave':
                            print ('This area is unfinished, and does not yet have an inventory.')
            else:
                b = False
    return string

def s1_room_start ():
    print ('An empty entrance room. Doors lead forwards, left and right. Stairs lead up.')
    while True:
        c = choice ('up/left/right/forward: ')
        match c:
            case 'up':
                print ('You climb up the stairs.')
                return 'up_hall'
            case 'left':
                print ('You enter the room to the left.')
                return 'dining'
            case 'right':
                print ('You enter the room to the right.')
                return 'kitchen'
            case 'forward' | 'forwards':
                print ('You enter the door at the back.')
                return 'garden'
            case 'back' | 'backward' | 'backwards':
                print ('But there was not a door.')
def s1_room_garden ():
    global active
    global gate_key
    global shed_code
    global bedroom_key
    global shed_lock_uses
    global alt_stage

    print ('A single tree, small shed, and a gate. Which do you investigate?')
    while True:
        c = choice ('tree/shed/gate/back: ')
        match c:
            case 'back' | 'backward' | 'backwards':
                print ('You return to the entrance hall.')
                return 'start'
            case 'tree':
                if not bedroom_key:
                    print ('You investigate the tree.')
                    time.sleep (DELAY / 4)
                    print ('And find a key!')
                    bedroom_key = True
                else:
                    print ("You investigate the tree.")
                    time.sleep (DELAY / 4)
                    print ("There's nothing of use.")
            case 'gate':
                if not bedroom_key and not gate_key:
                    print ('The gate is locked.')
                elif gate_key:
                    s2_func_start ()
                    return 'forest'
                elif bedroom_key:
                    print ("Your key doesn't fit the lock.")
            case 'shed':
                if shed_lock_uses <= 2:
                    print ('It needs a 4-digit code.')
                    code = choice ('Enter the code, or "exit": ')
                    while (len(code) != 4 or not code.isdigit()) and not code == 'exit':
                        code = choice ('The code must be a 4-digit number or "exit": ')
                    if code == 'exit':
                        print ('You decide not to enter a code.')
                    elif code == ''.join(shed_code):
                        print ('The door unlocks!')
                        time.sleep (DELAY)
                        print ('You found a key inside!')
                        gate_key = True
                    else:
                        print ("But it wasn't the right code.")
                        shed_lock_uses += 1
                        match shed_lock_uses:
                            case 1:
                                print ('The lock is now slightly damaged.')
                            case 2:
                                print ('The lock is now very damaged.')
                                time.sleep (DELAY/2)
                                print ('After another attempt, it may be too broken to use!')
                            case 3:
                                print ('...')
                else:
                    if alt_stage == 0:
                        print ('The lock is too damaged.')
                        time.sleep (DELAY)
                        print ('You cannot input the code.')
                        time.sleep (DELAY)
                        print ('Start looking for another way.')
                        alt_stage = 1
                    else:
                        print ('The lock is too damaged.')
def s1_room_dining ():
    print ('A large room with a long table in the centre.')
    time.sleep (DELAY/2)
    print ('Investigate further?')
    while True:
        c = choice ('yes/no: ')
        match c:
            case 'y'|'yes':
                print ('Investigating further, you find a note on the table.')
                print ('__' + shed_code[2] + '_')
                print ("There's nothing else in the room.")
                return 'start'
            case 'n'|'no':
                print ('You leave the dining room.')
                return 'start'
def s1_room_hall ():
    global bedroom_key
    global shed_code
    global alt_stage

    print ('A long hall with 3 doors and stairs going back down.')
    while True:
        c = choice ('1/2/3/leave: ')
        match c:
            case 'leave':
                print ('You return down the stairs.')
                return 'start'
            case '3'|'three':
                if bedroom_key:
                    print ('You unlock the bedroom door.')
                    time.sleep (DELAY)
                    print ('There is a note on the bed.')
                    time.sleep (DELAY)
                    print (shed_code[0] + '__' + shed_code[3])
                else:
                    print ('The door is locked.')
            case '2'|'two':
                if alt_stage == 2:
                    print ('You enter the room.')
                    time.sleep (DELAY)
                    print ('The window is wide open.')
                    time.sleep (DELAY)
                    while True:
                        d = choice ('back/window: ')
                        match d:
                            case 'back'|'return'|'backward'|'backwards':
                                time.sleep (DELAY)
                                print ('The door is locked.')
                            case 'window':
                                time.sleep (DELAY)
                                print ('You leave through the window.')
                                s2_func_start ()
                                alt_stage = 3
                                return 'forest'

                else:
                    print ('The door is locked.')
            case '1'|'one':
                print ('The door is locked.')
def s1_room_kitchen ():
    global alt_stage

    print ('A small kitchen with cupboards hanging open.')
    time.sleep (DELAY/2)
    print ('Investigate further?')
    while True:
        c = choice ('yes/no: ')
        match c:
            case 'y'|'yes':
                print ('After looking through every cupboard, you find a note.')
                if alt_stage == 1:
                    time.sleep (DELAY)
                    print ('There should be something here. It has not been implemented yet.')
                    alt_stage = 2
                elif alt_stage == 0:
                    print ('_' + shed_code[1] + '__')
                else:
                    print ('You saw this already.')
                print ("There's nothing else in the room.")
                return 'start'
            case 'n'|'no':
                print ('You leave the kitchen.')
                return 'start'
def s1_func_start ():
    global timer

    difficulty = ''
    while difficulty not in ['easy', 'medium', 'hard']:
        difficulty = choice ('Select a difficulty (easy/medium/hard): ')
    match difficulty:
        case 'easy':
            print ('Easy difficulty selected.')
            timer = 420
        case 'medium':
            print ('Medium difficulty selected.')
            timer = 300
        case 'hard':
            print ('Hard difficulty selected. Good luck.')
            timer = 180
        case _:
            print ('Invalid difficulty. Defaulting to medium.')
            timer = 300
    
    print ("INFORMATION ==================")
    print (" - Your goal at each stage is provided.")
    print (" - If something tells you you're stuck, you're")
    print ("     probably not.")
    print (" - There might be secrets.")
    print (" - If the game isn't progressing, press enter.")
    print (" - No delays should be longer than a couple of seconds.")
    print (" - Closer inspections may be needed.")
    print ("COMMANDS =====================")
    print (" - Commands are available at every decision or input.")
    print (" - /n <text> (aliases /note, /notes) will add a line to the notepad.")
    print (" - /r (alias /read) will display the entire contents of the notepad.")
    print (" - /i (alias /inv) will display any items you have collected.")
    print ("==============================")
    print ()
    print ("You wake up in an unfamiliar house.")
    time.sleep (DELAY/2)
    print ("You're alone, for now.")
    time.sleep (DELAY/2)
    print ("Looking outside, you see the sun setting.")
    time.sleep (DELAY/2)
    print ("You should get out of here, before anyone comes back.")
    time.sleep (DELAY/2)
    print ()
    print ('GOAL - ESCAPE')
    input ()

def s2_room_start ():
    print ('The house is behind you, a forest stretches out in front.')
    print ('The sound of rain on the trees is deafening.')
    while True:
        c = choice ('forward/search: ')
        match c:
            case 'forward'|'forwards':
                print ('You run deeper into the forest.')
                return 'centre'
            case 'backward'|'backwards'|'back':
                print ('There is no reason to go back.')
            case 'search':
                s2_func_search()
def s2_room_centre ():
    global maze_fails
    global can_find_map
    global has_map

    print ('You enter a small clearing.')
    while True:
        c = choice ('back/forward/search: ')
        match c:
            case 'forward'|'forwards':
                if maze_fails <= 2 or has_map:
                    print ('You run even deeper into the forest.')
                    return 'maze'
                elif not can_find_map:
                    print ("You clearly don't have the map for this yet.")
                    can_find_map = True
                else:
                    print ("You should search for a map first.")
            case 'backward'|'backwards'|'back':
                return 'start'
            case 'search':
                if can_find_map:
                    print ("There's a note on the ground.")
                    time.sleep (DELAY/1.5)
                    print ('It shows a drawing of the clearing, with an arrow pointing forward.')
                    time.sleep (DELAY/3)
                    print ("After that arrow, there's a list of other directions.")
                    time.sleep (DELAY/3)
                    print (forest_code)
                    can_find_map = False
                    has_map = True
                else:
                    s2_func_search()
def s2_room_maze ():
    global alt_stage
    global maze_fails

    correct = 0
    while True:
        next_dir = forest_code[correct]
        c = choice ('forward/backward/left/right: ')
        match c:
            case 'forward'|'forwards':
                if next_dir == '^':
                    correct += 1
                else:
                    print ('You find yourself back at the clearing.')
                    maze_fails += 1
                    return 'centre'
            case 'backward'|'backwards'|'back':
                if next_dir == 'v':
                    correct += 1
                else:
                    print ('You find yourself back at the clearing.')
                    maze_fails += 1
                    return 'centre'
            case 'left':
                if next_dir == '<':
                    correct += 1
                else:
                    print ('You find yourself back at the clearing.')
                    maze_fails += 1
                    return 'centre'
            case 'right':
                if next_dir == '>':
                    correct += 1
                else:
                    print ('You find yourself back at the clearing.')
                    maze_fails += 1
                    return 'centre'
        if correct == 10:
            alt_stage = 4
            print ('...')
            time.sleep (DELAY)
            return 'solved'
def s2_room_aftermaze ():
    s3_func_start ()
    return 'cave'
def s2_func_start ():
    print('You escaped the house!')
    time.sleep(DELAY / 2)
    print("It's raining heavily.")
    time.sleep(DELAY / 2)
    print('You can hear thunder in the distance.')
    time.sleep(DELAY / 2)
    print("You should find shelter.")
    time.sleep(DELAY / 2)
    print("You run into the forest, hoping the leaves provide some cover.")
    time.sleep(DELAY / 2)
    print("It's not perfect. You should keep searching.")
    print()
    print('GOAL - SEARCH')
def s2_func_search ():
    r = random.randint(1, 3)
    match r:
        case 1:
            print("There's a berry bush here.")
            time.sleep(DELAY / 3)
            print("You probably shouldn't eat them.")
        case 2:
            print("There are trees around you.")
            time.sleep(DELAY / 3)
            print("Unsurprising, given that you are in a forest.")
        case 3:
            print("You notice a squirrel on one of the trees.")
            time.sleep(DELAY / 3)
            print("It runs away after noticing you.")

def s3_room_start ():
    global sticks

    print ('The entrance of the cave.')
    if not sticks:
        print ('There are some dry sticks on the ground.')
        print ('Collect the sticks or go deeper?')
        while True:
            c = choice ('collect/deeper: ')
            match c:
                case 'collect':
                    print ('You collected all of the sticks.')
                    sticks = True
                    break
                case 'deeper':
                    print ('You go deeper into the cave.')
                    return 'second_room'
    print ('Go deeper?')
    while True:
        c = choice ('yes/no: ')
        match c:
            case 'y'|'yes':
                return 'second_room'
            case 'n'|'no':
                print ('But there was nothing else to do.')
                time.sleep (DELAY/3)
                print ('Go deeper?')
def s3_room_secondchamber ():
    global flint

    print ('The cave widens out into a largs chamber.')
    time.sleep (DELAY/3)
    print ("It's very dark. You cannot see clearly.")
    time.sleep (DELAY/3)
    print ('Search the chamber or head back.')
    while True:
        c = choice ('search/back/forward: ')
        match c:
            case 'back'|'backward'|'backwards':
                print ('You return to the light of the cave entrance.')
                return 'start'
            case 'forward'|'forwards':
                print ("It's too dark.")
                time.sleep (DELAY/3)
                print ("You need a light source first.")
            case 'search':
                if not flint:
                    print ('Looking around the room, you find some sharp stones.')
                    time.sleep (DELAY/4)
                    print ('Looks like flint.')
                    time.sleep (DELAY/4)
                    print ('Take one?')
                    c2 = choice ('yes/no: ')
                    if c2 in ['y', 'yes']:
                        print ('You pick up a shard of flint.')
                        flint = True
                    else:
                        print ('You choose not to pick up the flint.')
                else:
                    print ("Looking around, you don't see anything useful.")
                    time.sleep (DELAY/4)
                    print ("There's flint, but you already took some.")
def s3_func_start ():
    print ('You find a cave.')
    time.sleep (DELAY/2)
    print ('You should be safe from the storm here.')
    time.sleep (DELAY/2)
    print ("It's very cold. Find a way to warm up.")
    print ()
    print ('GOAL - START A FIRE')
# ============================================================================

s1_func_start ()
s1_time_start = time.perf_counter()
while active:
    match stage:
        case 'house':
            match loc:
                case 'start':
                    loc = s1_room_start ()
                case 'garden':
                    loc = s1_room_garden ()
                case 'up_hall':
                    loc = s1_room_hall ()
                case 'dining':
                    loc = s1_room_dining ()
                case 'kitchen':
                    loc = s1_room_kitchen ()
                case 'forest':
                    stage = 'forest'
                    loc = 'start'
                case _:
                    raise NotImplementedError ('This should be impossible.')
            if time.perf_counter() - s1_time_start >= timer:
                match loc:
                    case 'garden':
                        print ('You see people arriving.')
                        time.sleep (DELAY/2)
                        print ('They see you, and look furious.')
                        time.sleep (DELAY/2)
                    case 'start':
                        print ('You see the back door opening.')
                        time.sleep (DELAY/2)
                        print ('People come in, and see you.')
                        time.sleep (DELAY/2)
                    case _:
                        print ('You here people entering.')
                        time.sleep (DELAY/2)
                        print ("You can't leave without them noticing.")
                        time.sleep (DELAY/2)
                print ('YOU LOST THE GAME!')
                active = False
        case 'forest':
            match loc:
                case 'start':
                    loc = s2_room_start ()
                case 'centre':
                    loc = s2_room_centre ()
                case 'maze':
                    loc = s2_room_maze ()
                case 'solved':
                    loc = s2_room_aftermaze ()
                case 'cave':
                    loc = 'start'
                    stage = 'cave'
                case _:
                    raise NotImplementedError ('This should be impossible.')
        case 'cave':
            raise NotImplementedError ("\nThis area is currently under development.\nCongratulations on finishing the first 2 stages.")
            match loc:
                case 'start':
                    loc = s3_room_start ()
                case 'second_room':
                    loc = s3_room_secondchamber ()
                case _:
                    raise NotImplementedError ('This should be impossible.')
    print ()
