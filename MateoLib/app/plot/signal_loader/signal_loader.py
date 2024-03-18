import os
import torch
import pickle
import numpy as np


def load_fat_water(path: str, signal_name: str, method: str, theta_value: str, reg=None):
    if reg:
        logic_fat = (lambda x: ((".pickle" in x) and ("fat" in x) and (signal_name in x) and (method in x) and
                                (theta_value in x) and (f"reg{reg}_" in x)))
        logic_water = (lambda x: ((".pickle" in x) and ("water" in x) and (signal_name in x) and (method in x) and
                                  (theta_value in x) and (f"reg{reg}_" in x)))

    else:
        logic_fat = (lambda x: ((".pickle" in x) and ("fat" in x) and (signal_name in x) and (method in x) and
                                (theta_value in x)))
        logic_water = (lambda x: ((".pickle" in x) and ("water" in x) and (signal_name in x) and (method in x) and
                                  (theta_value in x)))
    list_fat = sorted(list(filter(logic_fat, os.listdir(path))))
    list_water = sorted(list(filter(logic_water, os.listdir(path))))
    print(f"list_water: {list_water}")
    print(f"list_fat: {list_fat}")
    assert len(list_fat) == 1, 'fat more than one element'
    assert len(list_water) == 1, 'water more than one element'
    with open(os.path.join(os.getcwd(), path, list_water[0]), 'rb') as water_file:
        water = pickle.load(water_file)
    with open(os.path.join(os.getcwd(), path, list_fat[0]), 'rb') as fat_file:
        fat = pickle.load(fat_file)

    return fat, water


def get_list_phis_directories(path: str, signal_name: str, reg: float):
    logic_phi = (lambda x: ("phi" in x) and (signal_name in x) and (f"reg{reg}.pickle" in x))
    logic_phi_fit = (lambda x: (".pickle" in x) and ("phi" in x) and (signal_name in x) and ('Fit' in x)
                     and not ('GN' in x))
    list_phi1 = sorted(list(filter(logic_phi, os.listdir(path))))
    list_fit = sorted(list(filter(logic_phi_fit, os.listdir(path))))
    list_phis = sorted(list_fit + list_phi1)
    print(f"list_phi: {list_phis}")
    return list_phis


def load_phis(path: str, list_phis: list):
    phi_list = []
    for phi_path in list_phis:
        with open(os.path.join(os.getcwd(), path, phi_path), 'rb') as phi_file:
            phi = pickle.load(phi_file)
        if isinstance(phi, torch.Tensor):
            phi_list.append(phi.numpy())
            continue
        phi_list.append(phi)
    return np.array(phi_list)
