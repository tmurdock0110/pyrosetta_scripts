#day 1 bootcamp app
import sys
import argparse
from pyrosetta import *

init(extra_options="-ignore_unrecognized_res")

parser = argparse.ArgumentParser()
#add line here to add an argument
#args file upload to rosetta
parser.add_argument("-f", "--pdb_file", help="name of the pdb file to process")
parser.add_argument("-o", "--output_file", help="name of the output file")
args = parser.parse_args()

#load the pdb file
pose = pose_from_pdb(args.pdb_file)
print(f"Loaded pose with {pose.total_residue()} residues from: {args.pdb_file}")

sfxn = get_fa_scorefxn()
score = sfxn(pose)
print(f"Score: {score}")





