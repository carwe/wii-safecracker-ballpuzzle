from collections import deque
from ansimarkup  import ansiprint


#            0         1         2
#            0123456789012345678901234      ->  y
raw_map = [ "______X_____X________X___", #0
            "___XX_____X______________", #1
            "__________________X______", #2
            "________________X_____X__", #3
            "__~__________XX_~__X_____", #4
            "____X____________________", #5
            "_______________X___X___X_", #6
            "______X______X_____X_____", #7
            "__X_________X____________", #8
            "______~__X____X__X______X", #9
            "______________X_____XX___", #10
            "X____________X___________", #11
            "___X_____X_______________", #12
            "_____X_____________~_X___", #13
            "__X_____________X____XX__", #14
            "_________________________", #15
            "_______________X_________", #16  |
            "____X_________X__________", #17  V
            "____________X___X________", #18
            "_______________________X_"] #19  x



def map_import( raw_map ):
    result_map = []
    for i,line in enumerate( raw_map ):
        temp_line  = []
        for j,field in enumerate( line ):
            temp_line.append( {'type':field, 'visited':False, 'start':False} )
        result_map.append( temp_line )
    return result_map


def map_print( game_map ):
    for line in game_map:
        for field in line:
            message = ""
            if field['start'] == True:
                message += "<i>"

            if   field['visited']==False:
                message += "<lw,r>"+field['type']+"</lw,r>"

            elif field['visited']==True and field['type']=='_':
                message += "<lw,g>"+field['type']+"</lw,g>"

            elif field['visited']==True and field['type']=='~':
                message += "<k,ly>"+field['type']+"</k,ly>"

            elif field['visited']==True and field['type']=='X':
                message += "<lr,lw>"+field['type']+"</lr,lw>"

            if field['start'] == True:
                message += "</i>"
            ansiprint( message, end="" )
        print("")
    print("")
    return


def map_count_hits( game_map ):
    count = 0
    for line in game_map:
        for field in line:
            if field['visited']== True and field['type']=='~':
                count = count + 1
    return count


def task_list():
    global todo
    for task in todo:
        print(task_print(task))
    return


def task_print( task ):
    return str(task['x']) + " " + str(task['y']) + " " + task['direction']


def task_add (x,y,direction):
    global todo,done
    task = {'x':x, 'y':y, 'direction':direction}
    if todo.count( task )>0 or done.count( task )>0: # duplicate rejected
        return
    todo.append( task )
    return


def task_exec( task ):
    global game_map, done
    done.append( task )
    x,y,direction = task['x'],task['y'],task['direction']
    game_map[x][y]['visited']=True
    if game_map[x][y]['type']=='X':
#        print("reached BLOCKED " + task_print( task ) )
        return
#    if game_map[x][y]['type']=='~':
#        global todo,done
#        todo,done=[],[]
#        return

    if   direction == 'n': ####################################################
        new_x,new_y = x,y
        while True:
            if new_x==0:
                return
            if game_map[new_x-1][new_y]['type']=='~':
                game_map[new_x-1][new_y]['visited']=True
                print( 'reached TARGET @{},{} from {},{}'.format(new_x-1,new_y,x,y) )
            if game_map[new_x-1][new_y]['type']=='X':
                task_add(new_x,new_y,'s')
                task_add(new_x,new_y,'e')
                task_add(new_x,new_y,'w')
                return
            new_x -= 1

    elif direction == 's': ####################################################
        new_x,new_y = x,y
        while True:
            if new_x==len(game_map)-1:
                return
            if game_map[new_x+1][new_y]['type']=='~':
                game_map[new_x+1][new_y]['visited']=True
                print( 'reached TARGET @{},{} from {},{}'.format(new_x+1,new_y,x,y) )
            if game_map[new_x+1][new_y]['type']=='X':
                task_add(new_x,new_y,'n')
                task_add(new_x,new_y,'e')
                task_add(new_x,new_y,'w')
                return
            new_x += 1

    elif direction == 'e': ####################################################
        new_x,new_y = x,y
        while True:
            if new_y==len(game_map[0])-1:
                return
            if game_map[new_x][new_y+1]['type']=='~':
                game_map[new_x][new_y+1]['visited']=True
                print( 'reached TARGET @{},{} from {},{}'.format(new_x,new_y+1,x,y) )
            if game_map[new_x][new_y+1]['type']=='X':
                task_add(new_x,new_y,'n')
                task_add(new_x,new_y,'s')
                task_add(new_x,new_y,'w')
                return
            new_y += 1

    elif direction == 'w': ####################################################
        new_x,new_y = x,y
        while True:
            if new_y==0:
                return
            if game_map[new_x][new_y-1]['type']=='~':
                game_map[new_x][new_y-1]['visited']=True
                print( 'reached TARGET @{},{} from {},{}'.format(new_x,new_y-1,x,y) )
            if game_map[new_x][new_y-1]['type']=='X':
                task_add(new_x,new_y,'n')
                task_add(new_x,new_y,'s')
                task_add(new_x,new_y,'e')
                return
            new_y -= 1

    else: ####################################################
        raise Exception("task contains unknown direction " + direction)
    return


def task_next():
    global todo
    task = todo.popleft()
    task_exec( task )
    return


def task_init(x,y):
    task_add( x, y, 'n' )
    task_add( x, y, 's' )
    task_add( x, y, 'e' )
    task_add( x, y, 'w' )
    return


def init( start_coords ):
    x,y = start_coords['x'], start_coords['y']
    global todo,done,game_map,raw_map
    todo = deque([])
    done = deque([])
    game_map = map_import( raw_map )
    game_map[x][y]['start'] = True
    task_init( x,y )
    return


def run():
    global todo, game_map
#    i,j=0,0
    while len(todo) > 0:
        task_next()
#        i=i+1
#        if i>0:
#            i=0
#            map_print( game_map )
#    map_print( game_map )
#    print( map_count_hits( game_map ) )
    return


start_coords={'x':5,'y':6}
init( start_coords )
run()
map_print( game_map )

#for x in range(0,20):
#    for y in range(0,25):
#        start_coords={'x':x,'y':y}
#        init( start_coords )
#        run()
#        if map_count_hits( game_map ) == 3:
#            print( start_coords, map_count_hits( game_map ) )
#            map_print( game_map )
