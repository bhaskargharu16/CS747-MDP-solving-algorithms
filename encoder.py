import argparse
def generate_mdpfile(grid):
    state_counter = 0
    endstate = []
    startstate = 0
    state_position_mapping = {} #position to state
    for idr,row in enumerate(grid):
        for idx,x in enumerate(row):
            if x == '0':
                if idr in state_position_mapping:
                    state_position_mapping[idr][idx] = state_counter
                else:
                    state_position_mapping[idr] = {}
                    state_position_mapping[idr][idx] = state_counter
                state_counter += 1
                continue
            if x == '2':
                if idr in state_position_mapping:
                    state_position_mapping[idr][idx] = state_counter
                else:
                    state_position_mapping[idr] = {}
                    state_position_mapping[idr][idx] = state_counter
                startstate = state_counter
                state_counter += 1
                continue
            if x == '3':
                if idr in state_position_mapping:
                    state_position_mapping[idr][idx] = state_counter
                else:
                    state_position_mapping[idr] = {}
                    state_position_mapping[idr][idx] = state_counter
                endstate.append(state_counter)
                state_counter += 1
                continue
    print("numStates", state_counter)
    print("numActions 4")
    print("start",startstate)
    print("end",end=' ')
    for x in endstate:
        print(x,end=' ')
    print()

    for idr,row in enumerate(grid[1:-1],1):
        for idx,x in enumerate(row[1:-1],1):
            if x == '0' or x == '2':
                if grid[idr][idx-1] == '0' or grid[idr][idx-1] == '2' or grid[idr][idx-1] == '3':#left is 0 or left is 2 or 3
                    print("transitions",state_position_mapping[idr][idx],0,state_position_mapping[idr][idx-1],-1,1)
                if grid[idr][idx-1] == '1':#left is 1
                    print("transitions",state_position_mapping[idr][idx],0,state_position_mapping[idr][idx],-1,1)
                if grid[idr][idx+1] == '0' or grid[idr][idx+1] == '2' or grid[idr][idx+1] == '3':#right is 0 or right is 2 or 3
                    print("transitions",state_position_mapping[idr][idx],1,state_position_mapping[idr][idx+1],-1,1)
                if grid[idr][idx+1] == '1':
                    print("transitions",state_position_mapping[idr][idx],1,state_position_mapping[idr][idx],-1,1)
                if grid[idr-1][idx] == '0' or grid[idr-1][idx] == '2' or grid[idr-1][idx] == '3':#up is 0 or up is 2 or 3
                    print("transitions",state_position_mapping[idr][idx],2,state_position_mapping[idr-1][idx],-1,1)
                if grid[idr-1][idx] == '1':
                    print("transitions",state_position_mapping[idr][idx],2,state_position_mapping[idr][idx],-1,1)
                if grid[idr+1][idx] == '0' or grid[idr+1][idx] == '2' or grid[idr+1][idx] == '3':#down is 0 or down is 2 or 3
                    print("transitions",state_position_mapping[idr][idx],3,state_position_mapping[idr+1][idx],-1,1)
                if grid[idr+1][idx] == '1':
                    print("transitions",state_position_mapping[idr][idx],3,state_position_mapping[idr][idx],-1,1)
    print("mdptype episodic")
    print("discount 1")
            



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--grid',type=str,default='')
    args = parser.parse_args()
    grid_file = open(args.grid,'r')
    grid = [line.split() for line in grid_file.readlines()]
    generate_mdpfile(grid)

