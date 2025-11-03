#day 1 bootcamp app
import sys
import argparse
from pyrosetta import *

init(extra_options="-ignore_unrecognized_res")

parser = argparse.ArgumentParser()
#add line here to add an argument
parser.add_argument("filename", help="the name of the file to process")
args = parser.parse_args()

#Test it by printing out the filename that was passed in.
print(args.filename)
