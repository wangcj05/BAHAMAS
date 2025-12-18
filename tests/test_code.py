# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import os
import numpy as np

from bahamas.sdlc_stage_hep_calculation import sdlc_stage_hep_calculation
from bahamas.human_error_mode_distribution import get_hemd_from_spreadsheet
from bahamas.stage_odc_distribution import get_stage_odc_dist
from bahamas.defect_conditional_probability import stage_dcp_calculation
from bahamas.uca_defect_correlation import get_uca_defect_correlation_dist
from bahamas.software_total_failure_probability_bbn import BBN
from bahamas.utils import SDLC_stages, ODC_types, UCA_types


workdir = os.path.dirname(__file__)
defect_data = os.path.join(workdir, '..', 'data', 'Defect_Data.xlsx')
task_data = os.path.join(workdir, '..', 'data', 'Task_List.xlsx')

def test_HEP_EMD():
    _,d = get_hemd_from_spreadsheet(defect_data)
    assert d['D2C'].pdf(0.6) == 2.0301163385771801e-07

def test_stage_odc_dist():
    d = get_stage_odc_dist(defect_data)
    assert d['Concept']['Documentation'].cdf(0.99) == 7.327789556831712e-06
    assert d['Requirement']['Algorithm'].cdf(0.1) == 0.0012975084733137195
    assert d['Concept']['Documentation'].mean() == (1000+0.5)/(1.+1000)
    assert d['Requirement']['Assignment'].mean() == (26+0.5)/(1.0+375)
    assert d['Design']['Checking'].mean() == (26+0.5)/(1.0+375)
    assert d['Implementation']['Function'].mean() == (372+0.5)/(1.+2292)
    assert d['Testing']['Interface'].mean() == (361+0.5)/(1.0+2464)
    assert d['Install and Maintenance']['Relationship'].mean() == (91+0.5)/(1.+2464)
    assert d['Design']['Timing'].mean() == (13+0.5)/(1.+375)

def test_dcp():
    dcp_gold = [3.497242685425109e-05, 0.0002529112181892472, 3.9544415406499936e-05, 5.478224783437511e-05, 3.7439121863896394e-05, 5.478224783437511e-05]
    for i, stage in enumerate(SDLC_stages):
        dcp = stage_dcp_calculation(task_data, stage)
        assert dcp == dcp_gold[i]

def test_uca_defect_correlation():
    ## Data for norm distribution
    # data = np.array([
    # [0.217, 0.0255, 0.525, 0.034, 0.124, 0.022, 0.134, 0.0095],
    # [0.288, 0.076, 0.667, 0.065, 0.045, 0.036, 0, 0],
    # [0.219, 0.037, 0.539, 0.0575, 0.102, 0.036, 0.141, 0.0645],
    # [0.25, 0.125, 0.25, 0.125, 0.25, 0.125, 0.25, 0.125],
    # [0.25, 0.077, 0.518, 0.032, 0.157, 0.046, 0.074, 0.108],
    # [0.262, 0.0325, 0.579, 0.043, 0.093, 0.0475, 0.065, 0.0195],
    # [0.25, 0.125, 0.25, 0.125, 0.25, 0.125, 0.25, 0.125],
    # [0.095, 0.167, 0.19, 0.1445, 0.524, 0.2115, 0.19, 0.1445]
    # ])

    ## Data for truncated norm distribution
    data = np.array([2.17000000e-01, 2.55000000e-02, 2.88023094e-01, 7.59562269e-02,
        2.19000000e-01, 3.69999989e-02, 2.56905982e-01, 1.17689469e-01,
        2.50157985e-01, 7.67429390e-02, 2.62000000e-01, 3.25000000e-02,
        2.56905982e-01, 1.17689469e-01, 1.74228858e-01, 1.18680274e-01,
        5.25000000e-01, 3.40000000e-02, 6.66999948e-01, 6.49998672e-02,
        5.38999999e-01, 5.74999999e-02, 2.56905982e-01, 1.17689469e-01,
        5.18000000e-01, 3.20000000e-02, 5.79000000e-01, 4.30000000e-02,
        2.56905982e-01, 1.17689469e-01, 2.16813548e-01, 1.22746487e-01,
        1.24000001e-01, 2.19999969e-02, 5.23521165e-02, 3.01844519e-02,
        1.02260018e-01, 3.56287876e-02, 2.56905982e-01, 1.17689469e-01,
        1.57054236e-01, 4.59073196e-02, 9.58592444e-02, 4.45215116e-02,
        2.56905982e-01, 1.17689469e-01, 5.21162941e-01, 1.98439447e-01,
        1.34000000e-01, 9.50000000e-03, 5.00000000e-15, 2.88675135e-15,
        1.43393694e-01, 6.17819499e-02, 2.56905982e-01, 1.17689469e-01,
        1.19224107e-01, 7.91971989e-02, 6.50300873e-02, 1.94497665e-02,
        2.56905982e-01, 1.17689469e-01, 2.16813548e-01, 1.22746487e-01])

    dist_dict = get_uca_defect_correlation_dist(defect_data)
    for i, uca in enumerate(UCA_types):
        for j, odc in enumerate(ODC_types):
            print(dist_dict[uca][odc].mean(), dist_dict[uca][odc].std())
            assert abs(dist_dict[uca][odc].mean() - data[i*len(ODC_types)*2+j*2]) < 1.E-8
            assert abs(dist_dict[uca][odc].std() - data[i*len(ODC_types)*2+j*2+1]) < 1.E-8

def test_BNN():
    uca_mean = [7.115368513716712e-06, 1.3418930928567966e-05, 4.909072581183153e-06, 4.329229240648344e-06]
    uca_sigma = [3.874164789989045e-06, 7.084402413124453e-06, 2.9678690820199835e-06, 2.387632635327028e-06]
    software_BBN = BBN(defect_data, task_data, num_samples=1000)
    software_BBN.calculate()
    total_failure_mean, total_failure_sigma, _ = software_BBN.get_total_failure_probability()
    assert total_failure_mean == 2.9772601264116172e-05
    assert total_failure_sigma == 1.572734313136203e-05
    for i, uca in enumerate(UCA_types):
        mean, sigma, _ = software_BBN.get_uca(uca)
        assert mean == uca_mean[i]
        assert sigma == uca_sigma[i]
