# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

"""
Created on September 8, 2025
@author: wangc
"""
import os
from pathlib import Path
import logging
import pandas as pd
import copy

from .utils import SDLC_stages, UCA_types
from .validate import validate_toml
from .software_total_failure_probability_bbn import BBN
from .cccg import CCCG

logger = logging.getLogger('BAHAMAS.Workflow')

file_dir =  os.path.dirname(__file__)
bbn_config_default = {'params':{'seed':2, 'samples':10000},
                'files':{'defect':os.path.join(file_dir, '..', 'data/Defect_Data.xlsx'),
                        'task':None,
                        'approx':None},
                'analysis':{'type':'precise'}
              }

ccf_config_default = {'files':{'structure':None},
                      'generate':{'output_file_base':'cccg',
                                  'output_type':'csv',
                                  'final':True,
                                  'single':False,
                                  'double':False,
                                  'triple':False,
                                  'function_all':False,
                                  'input_all':False,
                                  'design_all':False}
              }

class Workflow:
  """Workflow manager for BAHAMAS calculation
  """

  def __init__(self, config):
    logger.info('Initialization')
    self._config = config
    self._bbn_config = None
    self._ccf_config = None
    # validate input
    self._validate(config)
    if 'BBN' in config:
      self._bbn_config = self.update_config(config['BBN'], name="BBN")
      self.initialize_bbn()
    elif 'CCF' in config:
      self._ccf_config = self.update_config(config['CCF'], name="CCF")
      self.initialize_ccf()

  def update_config(self, config, name):
    """update default config with user provided data

    Args:
        config (dict): User-provided config file
        name (str): Name for the config file (i.e., BBN or CCF)

    Raises:
        IOError: If name is valid, raise the error

    Returns:
        dict: updated config file
    """
    if name == "BBN":
      default = copy.deepcopy(bbn_config_default)
    elif name == "CCF":
      default = copy.deepcopy(ccf_config_default)
    else:
      raise IOError(f'Unrecognized config file name: {name}')
    for key, value in config.items():
      default[key].update(value)
    return default


  def initialize_bbn(self):
    """Initialize BBN calculation
    """
    self._num_samples = self._bbn_config['params']['samples']
    self._seed = self._bbn_config['params']['seed']
    self._defect_data = self._bbn_config['files']['defect']
    self._task_data = self._bbn_config['files']['task']
    self._analysis_type = self._bbn_config['analysis']['type']
    self._approx_file = self._bbn_config['files']['approx']

  def initialize_ccf(self):
    """Initialize CCF calculation
    """
    self._sys_diagram = self._ccf_config['files']['structure']

  def run_bbn(self):
    """Run BBN Calculation

    Raises:
        IOError: Error out if invalid input for analysis type is provided
    """
    if self._analysis_type == 'precise':
      software_BBN = BBN(self._defect_data, self._task_data, self._num_samples, approx=False, seed=self._seed)
    elif self._analysis_type == 'approx':
      software_BBN = BBN(self._defect_data, self._approx_file, self._num_samples, approx=True, seed=self._seed)
    else:
      raise IOError('Invalid input')
    software_BBN.calculate()
    software_BBN.plot(save=False)

    total_failure_mean, total_failure_sigma, _ = software_BBN.get_total_failure_probability()
    logger.info('Software total failure: %s with std %s', total_failure_mean, total_failure_sigma)

    for uca in UCA_types:
      mean, sigma, _ = software_BBN.get_uca(uca)
      logger.info('UCA type: %s, Mean: %s, STD: %s', uca, mean, sigma)

  def run_ccf(self):
    """Run CCF calculation
    """
    cccg_obj = CCCG(file=self._sys_diagram)
    cccg_obj.generate(config=self._ccf_config['generate'])

  def run(self):
    """Execute the workflow
    """
    if self._bbn_config is not None:
      logger.info('Start BBN Calculation ...')
      self.run_bbn()
      logger.info('End BBN Calculation')
    if self._ccf_config is not None:
      logger.info('Start CCCGs generation')
      self.run_ccf()
      logger.info('End CCCGs generation')


  def write(self, data, fname, style='csv'):
    """Dump data

    Args:
        data (pandas.DataFrame): Output data to dump
        fname (str): File name for saving the data
        style (str, optional): Type of file (defaults to "csv")
    """
    if isinstance(data, pd.DataFrame):
      data.to_csv(fname, index=False)
    else:
      pass

  def visualize(self):
    pass

  def reset(self):
    pass


  def _validate(self, config):
    """Validate input file using JSON schema

    Args:
        config (dict): Dictionary for input

    Raises:
        IOError: Error out if  invalid
    """
    # validate
    validate = validate_toml(config)
    if not validate:
      logger.error("TOML input file is invalid.")
      raise IOError("TOML input file is invalid.")
