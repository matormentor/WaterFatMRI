from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR
from plot_helper import line_plot_keys, get_fat_center_phantom
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

signal_name = "IM_0078"
folder = "D:\\MRIsignals\\08_04_2024_phantom\\forward\\shift_phase_by_mean\\"
dicom_path = folder + f"{signal_name}_PolyFit_no_weights.dcm"

dicom_path = r"D:\MRIsignals\23_05_2024_phantom\IM_0003_PolyFit_no_weights.dcm"
image = ImDataParamsBMRR(dicom_path, dicom_enhanced=True)

keys = ["UTEphase", "UTEphase_after_forward", "UTEphase_after_fit", "UTEphase_after_gn"]
keys = ["UTEphase", "phi", "UTEphase_after_fit", "UTEphase_after_gn"]

signals = [image.WFIparams["UTEphase_after_forward"]]

x, y = range(30, 270), range(60, 230)
X, Y = np.meshgrid(x, y)
fig, ax = plt.subplots(1, 1, subplot_kw={"projection": "3d"})
ax.plot_surface(X, Y, signals[0][161, 60:230, 30:270], rcount=250, ccount=250, vmin=-0.5, vmax=np.pi, cmap=cm.get_cmap("gray"), antialiased=True)
ax.set(xticklabels=[],
       yticklabels=[])
plt.show()
# line_plot_keys(image=image, keys=keys, title='lung')
# line_plot_keys(image=image, title='fat', center=get_fat_center_phantom())
