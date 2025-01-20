import geatpy as ea
import sys
import os
import argparse
from public import glo
import numpy as np
from Mopso import Mopso
from public import P_objective
import debugpy



# Constants
NUM_ELE = glo.NUM_ELE

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run stimulation optimization.")
    parser.add_argument('--type', '-t', default="ti", help='Stimulation method')
    parser.add_argument('--position', '-p', default='hippo', help='Target location')
    parser.add_argument('--head', '-m', default='ernie', help='Head model name')
    parser.add_argument('--gen', '-g', default=0, type=int, help='Max epochs')
    args = parser.parse_args()

    # Add derived arguments
    args.name = f"{args.type}_{args.position}_{args.head}"
    return args

def set_global_variables(args):
    """Set global variables based on arguments."""
    glo.head_model = args.head
    glo.type = args.type

    # Set position coordinates
    position_map = {
        'hippo': [-31, -20, -14],
        'pallidum': [-17, 3, -1],
        'thalamus': [10, -19, 6],
        'sensory': [41, -36, 66],
        'dorsal': [25, 42, 37],
        'v1': [10, -92, 2],
        'dlpfc': [-39, 34, 37],
        'motor': [47, -13, 52],
    }

    glo.position = np.array(position_map.get(args.position, args.position))

def create_problem(args):
    """Create the appropriate problem based on the type."""
    if args.type == 'ti':
        from ti_problem import MyProblem
        return MyProblem()
    elif args.type in {'mti', 'tdcs'}:
        from tdcs_problem import MyProblem
        return MyProblem()
    else:
        raise ValueError(f"Unsupported stimulation type: {args.type}")

def run_algorithm(problem, gen):
    """Run the evolutionary algorithm."""
    algorithm = ea.soea_SEGA_templet(
        problem,
        ea.Population(Encoding='RI', NIND=30),
        MAXGEN=gen,
        logTras=1,
        maxTrappedCount=10
    )
    algorithm.mutOper.F = 0.5
    algorithm.recOper.XOVR = 0.2

    return ea.optimize(
        algorithm,
        verbose=True,
        drawing=10,
        outputMsg=False,
        drawLog=False,
        saveFlag=False
    )

def run_mopso(args, prior_solution):
    """Run the MOPSO algorithm."""
    particals, cycle_, mesh_div, thresh = 100, 100, 10, 100
    Problem, M = "TES", 2

    print("Initializing MOPSO...")
    _, Boundary, _ = P_objective.P_objective("init", Problem, M, particals)
    max_, min_ = Boundary

    mopso_ = Mopso(particals, max_, min_, thresh, mesh_div)
    pareto_in, pareto_fitness = mopso_.done(cycle_)

    # Save results
    path_fitness = f"./output/pareto_fitness_{args.name}.txt"
    path_in = f"./output/pareto_in_{args.name}.txt"

    if args.type == 'ti':
        with open(path_in, 'w+') as fp:
            for solution in pareto_in:
                result = ' '.join([
                    str(int(round(solution[2] * (NUM_ELE-1)))),  # Element calculation
                    str(2 * solution[0]),
                    str(int(round(solution[3] * (NUM_ELE-1)))),
                    str(-2 * solution[0]),
                    str(int(round(solution[4] * (NUM_ELE-1)))),
                    str(2 * solution[1]),
                    str(int(round(solution[5] * (NUM_ELE-1)))),
                    str(-2 * solution[1])
                ])
                fp.write(result + "\n")
    else:
        np.savetxt(path_in, pareto_in)

    np.savetxt(path_fitness, pareto_fitness)
    print(f"Pareto positions saved to: {path_in}")
    print(f"Pareto values saved to: {path_fitness}")

def main():
    
    debugpy.listen(("localhost", 5678))  # Specify the debugging port
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()
    
    """Main function to run the optimization process."""
    args = parse_arguments()
    set_global_variables(args)

    print("Creating problem...")
    problem = create_problem(args)
    gen = args.gen if args.gen != 0 else 50

    print("Running algorithm...")
    res = run_algorithm(problem, gen)
    print(res)

    glo.prior = np.array(res['Vars'][0])

    print("Running MOPSO...")
    run_mopso(args, glo.prior)
    print("Process completed.")

if __name__ == "__main__":
    main()
