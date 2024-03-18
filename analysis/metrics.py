from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR

import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import binary_erosion, binary_dilation
import scipy.ndimage as nd

signal_name = "IM_0003"
folder = ("C:\\Users\\USUARIO\\Desktop\\Thesis\\MRIThesis\\signals\\"
          "24_02_2024_phantom_sep_wf_filter_check\\forward\\median\\")
dicom_path = folder + f"{signal_name}_PolyFit_no_weights.dcm"

image = ImDataParamsBMRR(dicom_path, dicom_enhanced=True)
image.Masks['tissueMask'] = image.get_tissueMaskFilled(10)
image.set_UTEphase()

mask1 = image.Masks["tissueMask"]
fat_mask = np.ones_like(mask1)
fat_mask[image.WFIparams["UTEphase"] > -3] = 0  # Limit set by looking at phantom
water_mask = mask1 != fat_mask

kernel = np.ones((3, 3, 3), np.uint8)
water_mask = nd.binary_erosion(water_mask, kernel, iterations=1)
fat_mask = nd.binary_erosion(fat_mask, kernel, iterations=1)
mix_mask = water_mask.astype(bool) + fat_mask.astype(bool)
fit_masks = water_mask, fat_mask

mask2 = binary_dilation(mask1, [(np.ones((3, 3, 3)), 1)])
mask = binary_erosion(mask1, [(np.ones((5, 5, 5)), 2)])

phase_after_fit = image.WFIparams["UTEphase"]
phase_after_fit[mask1] -= image.WFIparams["phi"].real[mask1]
phase_after_fit[~mask] = 0
fig, axes = plt.subplots(1, 2)
fig1 = axes[0].imshow(phase_after_fit[:, :, 161])

image.WFIparams["UTEphase_after_forward"][mask2] += np.pi
image.WFIparams["UTEphase_after_forward"][~mask1] = 0
x1 = abs(np.sum(np.gradient(image.WFIparams["UTEphase_after_forward"][mask])))
fig2 = axes[1].imshow(image.WFIparams["UTEphase_after_forward"][:, :, 161])
plt.colorbar(fig1)
plt.colorbar(fig2)
plt.show()
x2 = abs(np.sum(np.gradient(phase_after_fit[mask])))
print("B0 (forward) sum of gradients: ", x1)
print("B1 (fit) sum of gradients: ", x2)


x1_water = abs(np.sum(np.gradient(image.WFIparams["UTEphase_after_forward"][water_mask])))
x2_water = abs(np.sum(np.gradient(phase_after_fit[water_mask])))
x1_fat = abs(np.sum(np.gradient(image.WFIparams["UTEphase_after_forward"][fat_mask])))
x2_fat = abs(np.sum(np.gradient(phase_after_fit[fat_mask])))

print("\nB0 (forward) sum of gradients water mask: ", x1_water)
print("B1 (fit) sum of gradients water mask: ", x2_water)

print("\nB0 (forward) sum of gradients fat mask: ", x1_fat)
print("B1 (fit) sum of gradients fat mask: ", x2_fat)
