# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import logging
import pathlib
import toml
import os

logger = logging.getLogger()

# software development lifecycle stages
SDLC_stages = ['Concept', 'Requirement', 'Design', 'Implementation', 'Testing', 'Install and Maintenance']

# Define action type names
human_error_modes = ['D1', 'D2', 'C', 'OC', 'D1C', 'D1OC', 'D2C', 'D2OC', 'O', 'D1O', 'D2O']

# ODC types
ODC_types = ['Algorithm', 'Assignment', 'Checking', 'Documentation', 'Function', 'Interface', 'Relationship', 'Timing']

UCA_types = ['UCA-A', 'UCA-B', 'UCA-C', 'UCA-D']

UCA_mean = ['UCA-A Mean',	'UCA-B Mean',	'UCA-C Mean',	'UCA-D Mean']

UCA_sigma = ['UCA-A Sigma',	'UCA-B Sigma','UCA-C Sigma','UCA-D Sigma']


def read_toml(file_path):
  """Read TOML-formatted file

  Args:
      file_path (str): Path to the file

  Returns:
      dict: Dictionary of file content
  """
  with open(file_path, 'r') as file:
    path = pathlib.Path(file_path).parent
    data = toml.load(file)
    if 'BBN' in data:
      for f in data['BBN']['files']:
        data['BBN']['files'][f] = os.path.join(path, data['BBN']['files'][f])
    if 'CCF' in data:
      for f in data['CCF']['files']:
        data['CCF']['files'][f] = os.path.join(path, data['CCF']['files'][f])
  return data
