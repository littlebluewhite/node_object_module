import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity")
args = parser.parse_args()
print(args)
print(args.__getattribute__("verbose"))
