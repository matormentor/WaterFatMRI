# %%
import copy

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy.ndimage import binary_erosion, binary_dilation

from MateoLib.app.plot.plot_3d import plot3d
from bmrr_wrapper.Interfaces.ImDataParams.ImDataParamsBMRR import ImDataParamsBMRR
matplotlib.use("TkAgg")

path = "Z:\\Argudo\\2023_12_08\\Phantom\\DICOM\\IM_0078"

if ".mat" in path:
    image = ImDataParamsBMRR(path)
else:
    image = ImDataParamsBMRR(path, dicom_enhanced=True)

TE_s = image.ImDataParams['TE_s'].astype(float)

# if isinstance(image.ImDataParams['TE_s'], np.ndarray):
#     image.ImDataParams['TE_s'] = image.ImDataParams['TE_s'].tolist()
try:
    image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s'][0]]  # set_theta does not work for more than 1 TEs
except TypeError as e:
    image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s']]
    print(e)

# Initialize mask, unwrap phase and fat model with theta
filled_mask = image.get_tissueMaskFilled(10)
fit_mask = filled_mask
image.Masks['tissueMask'] = filled_mask
image.BFRparams['BFRmask'] = image.Masks['tissueMask']

image.set_UTEphase()
print(image.WFIparams['UTEphase'].shape)
plt.hist(image.WFIparams['UTEphase'][fit_mask].flatten(), 100)
plt.show()
# %%

fat_mask = np.zeros_like(filled_mask)
fat_mask[(2.1 < image.WFIparams["UTEphase"]) & (image.WFIparams["UTEphase"] < 3)] = 1
fat_mask = binary_erosion(fat_mask, np.ones((5, 5, 5)), iterations=2)
fat_mask = binary_erosion(fat_mask, np.ones((3, 3, 3)), iterations=3)
fat_mask = binary_dilation(fat_mask, np.ones((5, 5, 5)), iterations=3)

img_sub = copy.deepcopy(image.WFIparams["UTEphase"])
img_sub[fat_mask] = -5
plot3d(img_sub)
# plt.title("Fat Mask")
# plt.show()
# %%
water_mask = fit_mask != fat_mask
water_mask = binary_erosion(water_mask, np.ones((6, 6, 6)), iterations=3)
water_mask = binary_dilation(water_mask, np.ones((5, 5, 5)), iterations=2)

img_sub2 = copy.deepcopy(image.WFIparams["UTEphase"])
img_sub2[water_mask] = -5
plot3d(img_sub2)
# plt.title("Water Mask")
# plt.show()