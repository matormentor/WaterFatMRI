from analysis.plot_helper import get_plt_entries

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from bmrr_wrapper.Visualization.CBviewer import cbviewer
from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR

matplotlib.use("TkAgg")
matplotlib.interactive(True)

signal_name = "IM_0078"

folder = "D:\\MRIsignals\\25_03_2024_phantom_set_fit_mask_b1_only_water\\forward\\"
path = folder + f"{signal_name}_PolyFit_no_weights.dcm"

# phantom_folder = "Z:\\Argudo\\2023_12_08\\Phantom\\DICOM\\"

image = ImDataParamsBMRR(path, dicom_enhanced=True)

image.WFIparams["UTEphase_after_forward"] += np.pi
image.WFIparams["water"] *= -1
image.WFIparams["fat"] *= -1
isForward = True
if isForward:
    pltEntry = get_plt_entries(image, {"ImDataParams": ["signal"],
                                       "WFIparams": ["forward_phase", "UTEphase_after_forward",  "phi",
                                                     "UTEphase_after_fit", "water", "fat"]})
else:
    pltEntry = get_plt_entries(image, {"ImDataParams": ["signal"],
                                       "WFIparams": ["phi", "water", "fat"]})

cbviewer(pltEntry)
plt.show(block=True)
