import argparse
action_map = {'0':'W','1':'E','2':'N','3':'S'}
def decode(grid,policy_vector,value_vector):
    state_counter = 0
    endstate = []
    startstate = 0
    state_position_mapping = {} # position to state
    position_state_mapping = {} # state to position
    for idr,row in enumerate(grid):
        for idx,x in enumerate(row):
            if x == '0':
                if idr in state_position_mapping:
                    state_position_mapping[idr][idx] = state_counter
                else:
                    state_position_mapping[idr] = {}
                    state_position_mapping[idr][idx] = state_counter
                position_state_mapping[state_counter] = tuple((idr,idx))
                state_counter += 1
                continue
            if x == '2':
                if idr in state_position_mapping:
                    state_position_mapping[idr][idx] = state_counter
                else:
                    state_position_mapping[idr] = {}
                    state_position_mapping[idr][idx] = state_counter
                startstate = state_counter
                position_state_mapping[state_counter] = tuple((idr,idx))
                state_counter += 1
                continue
            if x == '3':
                if idr in state_position_mapping:
                    state_position_mapping[idr][idx] = state_counter
                else:
                    state_position_mapping[idr] = {}
                    state_position_mapping[idr][idx] = state_counter
                endstate.append(state_counter)
                position_state_mapping[state_counter] = tuple((idr,idx))
                state_counter += 1
                continue
    policy_direction = []
    for idx,action in enumerate(policy_vector):
        if value_vector[idx]!=0.0:
            policy_direction.append(action_map[action])
        else:
            policy_direction.append('stop')

    current_state = startstate
    # print(position_state_mapping)
    # print("\n\n")
    # print(state_position_mapping)
    while current_state not in endstate:
        print(policy_direction[current_state],end = ' ')
        current_position = position_state_mapping[current_state]
        next_position = current_position
        if policy_direction[current_state] == 'W':
            next_position = tuple((current_position[0],current_position[1]-1))
        elif policy_direction[current_state] == 'E':
            next_position = tuple((current_position[0],current_position[1]+1))
        elif policy_direction[current_state] == 'N':
            next_position = tuple((current_position[0]-1,current_position[1]))
        elif policy_direction[current_state] == 'S':
            next_position = tuple((current_position[0]+1,current_position[1]))
        else:
            break;
        current_state = state_position_mapping[next_position[0]][next_position[1]]
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--grid',type=str,default='')
    parser.add_argument('--value_policy',type=str,default='')
    args = parser.parse_args()
    grid_file = args.grid
    value_policy_file = args.value_policy
    grid = [line.split() for line in open(grid_file,'r').readlines()]
    vector = [(line.split()[0],line.split()[1]) for line in open(value_policy_file,'r').readlines()]
    policy_vector = [x[1] for x in vector]
    value_vector = [x[0] for x in vector]
    decode(grid,policy_vector,value_vector)
