from analysis.plot_helper import get_plt_entries

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from bmrr_wrapper.Visualization.CBviewer import cbviewer
from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR

matplotlib.use("TkAgg")
matplotlib.interactive(True)

signal_name = "IM_0004"


folder = "D:\\MRIsignals\\08_04_2024_lung\\forward\\precise_susceptibility\\"
# path = r"D:\MRIsignals\23_05_2024_phantom\IM_0003_PolyFit_no_weights.dcm"
# path = r"D:\MRIsignals\25_03_2024_phantom_set_fit_mask_b1_only_water\forward\IM_0078_PolyFit_no_weights.dcm"
path = folder + f"{signal_name}_reg10_GN_w_init.dcm"

# phantom_folder = "Z:\\Argudo\\2023_12_08\\Phantom\\DICOM\\"

image = ImDataParamsBMRR(path, dicom_enhanced=True)

# image.WFIparams["UTEphase_after_forward"] += np.pi
# image.WFIparams["UTEphase_after_fit"] *= -1
# image.WFIparams["water"] *= -1
# image.WFIparams["fat"] *= -1
image.ImDataParams["signal"] = np.moveaxis(image.ImDataParams["signal"], [0, 1, 2], [2, 1, 0])
# image.WFIparams["forward_phase"] = np.moveaxis(image.WFIparams["forward_phase"], [0, 1, 2], [2, 1, 0])
isForward = True
phantom_forward = ["forward_phase", "UTEphase_after_forward", "phi", "UTEphase_after_fit", "water", "fat"]
phantom_no_forward = ["phi", "UTEphase_after_fit", "water", "fat"]
anatomy_forward = ["forward_phase", "UTEphase_after_forward", "fit_phase", "UTEphase_after_fit", "phi", "UTEphase_after_gn", "water", "fat"]
anatomy_no_forward = ["fit_phase", "UTEphase_after_fit", "phi", "UTEphase_after_gn", "water", "fat"]
if isForward:
    pltEntry = get_plt_entries(image, {"ImDataParams": ["signal"],
                                       "WFIparams": anatomy_forward})
else:
    pltEntry = get_plt_entries(image, {"ImDataParams": ["signal"],
                                       "WFIparams": anatomy_no_forward}, vmax=1)

cbviewer(pltEntry)
plt.show(block=True)
