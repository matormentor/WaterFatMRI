from analysis.plot_helper import get_plt_entries

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from bmrr_wrapper.Visualization.CBviewer import cbviewer
from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR

matplotlib.use("TkAgg")
matplotlib.interactive(True)

signal_name = "IM_0078"

folder = "C:\\Users\\USUARIO\\Desktop\\Thesis\\MRIThesis\\signals\\14_03_2024_2nd_polyfit_phantom\\salt\\forward\\"
path = folder + f"{signal_name}_PolyFit_no_weights"

phantom_folder = "Z:\\Argudo\\2023_12_08\\Phantom\\DICOM\\"

image = ImDataParamsBMRR(path, dicom_enhanced=True)

image.WFIparams["UTEphase_after_forward"] += np.pi
isForward = True
if isForward:
    pltEntry = get_plt_entries(image, {"ImDataParams": ["signal"],
                                       "WFIparams": ["forward_phase", "UTEphase_after_forward",  "phi",
                                                     "UTEphase_after_fit"]})  # , "water", "fat"]})
else:
    pltEntry = get_plt_entries(image, {"ImDataParams": ["signal"],
                                       "WFIparams": ["phi", "water", "fat"]})

cbviewer(pltEntry)
plt.show(block=True)
