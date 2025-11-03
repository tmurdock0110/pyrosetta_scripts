#day 1 bootcamp app
import sys
import argparse
from pyrosetta import *
from pyrosetta.rosetta.numeric.random import *

init(extra_options="-ignore_unrecognized_res")

parser = argparse.ArgumentParser()
#add line here to add an argument
#args file upload to rosetta
parser.add_argument("-f", "--pdb_file", help="name of the pdb file to process")
parser.add_argument("-o", "--output_directory", help="name of the output directory")
parser.add_argument("-n", "--n_iterations", type=int, help="number of iterations to run")
args = parser.parse_args()

#load the pdb file
pose = pose_from_pdb(args.pdb_file)
sfxn = get_fa_scorefxn()
kT = 1.0
mc = MonteCarlo(pose,sfxn,kT)

print(f"Loaded pose with {pose.total_residue()} residues from: {args.pdb_file}")
mypose = pose
total_residue = pose.total_residue() + 1

# Packing
tf = pyrosetta.rosetta.core.pack.task.TaskFactory()
score = sfxn(mypose)
print(f"Score: {score}")

# Set up MoveMap for backbone and sidechain movement
movemap = pyrosetta.rosetta.core.kinematics.MoveMap()
movemap.set_bb(True)
movemap.set_chi(True)
# Minimizer setup
min_opts = pyrosetta.rosetta.core.optimization.MinimizerOptions("lbfgs_armijo_atol", 0.01, True)
minimizer = pyrosetta.rosetta.core.optimization.AtomTreeMinimizer()




#Create Monte Carlo Protocol loop to Optimize Pose n times
for i in range(args.n_iterations):
    #choose a random residue and move it by a random amount
    #use PyRosetta's numeric.random module to generate a value between negative infinity and positive infinity drawn from a standard normal.
    phi_pert = pyrosetta.rosetta.numeric.random.gaussian()
    psi_pert = pyrosetta.rosetta.numeric.random.gaussian()

    print(f"Phi perturbation: {phi_pert}")
    print(f"Psi perturbation: {psi_pert}")

    #using the “uniform” function from PyRosetta numeric.random you can turn a random number 
    # uniformly distributed in the range [0..1) to an integer between 1 and N (the number of residues in your Pose) 
    # by random_number * N + 1.
    randres = pyrosetta.rosetta.numeric.random.uniform()
    randres = int(randres * total_residue)
    print(f"Random residue: {randres}")

    orig_phi = mypose.phi(randres)
    orig_psi = mypose.psi(randres)
    mypose.set_phi(randres, orig_phi + phi_pert)
    mypose.set_psi(randres, orig_psi + psi_pert)

    # Packing
    score = sfxn(mypose)
    print(f"Score: {score}")
    print("Packing...")
    task = tf.create_task_and_apply_taskoperations(mypose)
    task.restrict_to_repacking()
    pyrosetta.rosetta.core.pack.pack_rotamers(mypose, sfxn, task)
    print("Packed")
    minimizer.run(mypose, movemap, sfxn, min_opts)
    print("Minimized")
    score = sfxn(mypose)
    mc.boltzmann(score, mypose)
    print(f"Score: {score}")

pose = mc.lowest_score_pose()
pose.dump_pdb("best_pose.pdb")
print(f"Saved pose to: best_pose.pdb")


