from planning_algorithms import *
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mdp',type=str,default='')
    parser.add_argument('--algorithm',type=str,default='')
    args = parser.parse_args()

    filepath = args.mdp
    algorithm = args.algorithm

    mdp_solver = MDP()
    mdp_solver.solve_mdp(filepath,algorithm)