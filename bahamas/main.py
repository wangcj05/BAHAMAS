# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

"""
Created on October 14, 2024
@author: wangc
"""
import os
import sys
import logging
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bahamas.utils import SDLC_stages, UCA_types, read_toml
from bahamas.workflow import Workflow

from bahamas.validate import validate_toml
from bahamas.software_total_failure_probability_bbn import BBN
from bahamas.cccg import CCCG

logging.basicConfig(format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
# To enable the logging to both file and console, the logger for the main should be the root,
# otherwise, a function to add the file handler and stream handler need to be created and called by each module.
# logger = logging.getLogger(__name__)
logger = logging.getLogger('BAHAMAS')
# # create file handler which logs debug messages
fh = logging.FileHandler(filename='bahamas.log', mode='w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)-20s %(levelname)-8s %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

# file_dir =  os.path.dirname(__file__)
# config_default ={'params':{'seed':2, 'samples':10000},
#                 'files':{'defect':os.path.join(file_dir, '..', 'data/Defect_Data.xlsx')}
#               }

def main():
  logger.info('Welcome to use BAHAMAS!')
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('-i', '--input', type=str, default='../examples/bbn.toml', help='The path to the input file')
  parser.add_argument('-o', '--output', type=str, default='output.csv', help='The output file path to save the output to')
  # parse the arguments
  args = parser.parse_args()
  in_file = args.input
  out_file = args.output
  cwd = os.getcwd()
  config_file = os.path.join(cwd, in_file)
  config = read_toml(config_file)
  out_file =  os.path.join(cwd, out_file)

  module = Workflow(config)
  module.run()

  # logger.info('Outputs are saved to: %s', out_file)

  logger.info(' ... Complete!')

if __name__ == '__main__':
  sys.exit(main())


# TODO
# 3. Consistent sampling for correlated variables
# 4. Pip packaging
# 5. Benchmark
