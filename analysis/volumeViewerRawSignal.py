import matplotlib
import matplotlib.pyplot as plt

from bmrr_wrapper.Visualization.CBviewer import cbviewer
from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR

matplotlib.use("TkAgg")
matplotlib.interactive(True)

signal_name = "IM_0048"

phantom_folder = "Z:\\Argudo\\2023_12_08\\Phantom\\DICOM\\"
phantom_path = phantom_folder + f"{signal_name}"

image = ImDataParamsBMRR(phantom_path, dicom_enhanced=True)
pltEntry = [[abs(image.ImDataParams["signal"]), {'window': [0, 100], 'title': 'B1_percentage', 'cmap': 'gray'}]]
cbviewer(pltEntry)
plt.show(block=True)
