from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR
from plot_helper import line_plot_keys, get_fat_center_phantom

signal_name = "IM_0078"
folder = "D:\\MRIsignals\\25_03_2024_phantom_set_fit_mask_b1_only_water\\forward\\"
dicom_path = folder + f"{signal_name}_PolyFit_no_weights.dcm"

image = ImDataParamsBMRR(dicom_path, dicom_enhanced=True)

line_plot_keys(image=image, title='water')
line_plot_keys(image=image, title='fat', center=get_fat_center_phantom())
