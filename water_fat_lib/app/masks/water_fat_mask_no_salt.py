# %%
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import binary_erosion
from water_fat_lib.app.data_loader.data_io import load_data

path = "/home/marrieta/Thesis/data/ArgudoNAS/2023_12_08/Phantom/DICOM/IM_0003"

image = load_data(image_path=path, return_echo_time=False)

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
fat_mask = np.ones_like(filled_mask)
fat_mask[image.WFIparams["UTEphase"] > -3] = 0
plt.imshow(fat_mask[:, :, 161])
plt.show()
# %%
water_mask = fit_mask != fat_mask
plt.imshow(water_mask[:, :, 161])
plt.show()
# %%
# Taking a matrix of size 3 as the kernel
kernel = np.ones((3, 3, 3), np.uint8)
water_erosion = binary_erosion(water_mask, kernel, iterations=1)
fat_erosion = binary_erosion(fat_mask, kernel, iterations=1)

plt.imshow(water_erosion[:, :, 161])
plt.show()
plt.imshow(fat_erosion[:, :, 161])
plt.show()
