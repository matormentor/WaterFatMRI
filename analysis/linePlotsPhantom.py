from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR
from plot_helper import line_plot_keys, get_fat_center_phantom

signal_name = "IM_0078"
folder = "C:\\Users\\USUARIO\\Desktop\\Thesis\\MRIThesis\\signals\\14_03_2024_2nd_polyfit_phantom\\salt\\forward\\"
dicom_path = folder + f"{signal_name}_PolyFit_no_weights"

image = ImDataParamsBMRR(dicom_path, dicom_enhanced=True)

line_plot_keys(image=image, title='water')
line_plot_keys(image=image, title='fat', center=get_fat_center_phantom())
