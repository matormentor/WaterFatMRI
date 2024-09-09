import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from bmrr_wrapper.Visualization.CBviewer import cbviewer
from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR

matplotlib.use("TkAgg")
matplotlib.interactive(True)

signal_name = "IM_0086"
# signal_name_2 = "IM_0078"

phantom_folder = "Z:\\Argudo\\2023_12_08\\Phantom\\DICOM\\"
phantom_path = phantom_folder + f"{signal_name}"
# phantom_2_path = phantom_folder + f"{signal_name_2}"

image = ImDataParamsBMRR(phantom_path, dicom_enhanced=True)
# image_2 = ImDataParamsBMRR(phantom_2_path, dicom_enhanced=True)
# image_2.Masks['tissueMask'] = image_2.get_tissueMaskFilled(10)
# image_2.set_UTEphase()
# pltEntry = [[image_2.WFIparams["UTEphase"], {'window': [-0.5, np.pi], 'title': 'UTE phase', 'cmap': 'gray'}]]
# pltEntry = [[2*np.pi*image.WFIparams["fieldmap_Hz"]*image_2.ImDataParams["TE_s"], {'window': [-0.5, 0.5], 'title': 'B0 phase', 'cmap': 'gray'}]]
pltEntry =[[np.abs(image.ImDataParams["signal"]), {'cmap': 'gray'}]]
cbviewer(pltEntry)


plt.show(block=True)
