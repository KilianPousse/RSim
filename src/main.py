import argparse
from simulation import RSim



# Create a parser
parser = argparse.ArgumentParser(description="RSim is a program developed by K.Pousse which allows you to launch a simulation with entities in a fixed world.")

# Positional argument for 'new' or 'load'
parser.add_argument('action', choices=['new', 'load'], help="Load mode: 'new' --> new save, 'load' --> load an existing save")

# Option to enable verbose mode
parser.add_argument('-v', '--verbose', action='store_true', help='Enable VERBOSE mode')

# Option for the save number
parser.add_argument('-s', '--save', type=int, help='Save number that the program will use', default=0)

# Option for the map size, which expects two values (width, height)
parser.add_argument('--size', type=int, nargs=2, metavar=('width', 'height'), help="Simulator Map Size (width height)", default=(200, 150))

# Option for the number of entities at the start of the simulation
parser.add_argument('--nEntities', type=int, help='Number of entities at the start of the simulation', default=10)

# Option for the number of foods at the start of the simulation
parser.add_argument('--nFoods', type=int, help='Number of foods at the start of the simulation', default=10)

# Parse the arguments
args = parser.parse_args()

# Validate the values for entities and food
if args.nEntities < 0:
    print("Error: nEntities must be a non-negative integer.")
    exit(1)

if args.nFoods < 0:
    print("Error: nFoods must be a non-negative integer.")
    exit(1)

# Initialize the simulation with the arguments
verbose = args.verbose
RSim.init(args.save, tuple(args.size))

# Logic for generating or loading
if args.action == 'new':
    RSim.generate(args.nEntities, args.nFoods)
    if args.verbose:
        print(f"New simulation created with {args.nEntities} entities and {args.nFoods} food items.")

elif args.action == 'load':
    RSim.save.load()
    if args.verbose:
        print(f"Loaded simulation from save number {args.save}.")

# Start the simulation
RSim.run()

if args.verbose:
    print("Simulation is now running.")
