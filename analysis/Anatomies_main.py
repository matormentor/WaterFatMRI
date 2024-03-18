from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR
from plot_helper import line_plot_vs_2_images

signal_name = "HWS"

folder_2 = "C:\\Users\\USUARIO\\Desktop\\Thesis\\MRIThesis\\signals\\07_03_2024_2nd_polyfit_abstract\\no_forward\\"
WFIpath_2_GN_reg_10 = folder_2 + f"{signal_name}_ImDataParams__reg10_GN_w_init.dcm_WFIparams.mat"

folder_4 = "C:\\Users\\USUARIO\\Desktop\\Thesis\\MRIThesis\\signals\\07_03_2024_4th_polyfit_abstract\\no_forward\\"
WFIpath_4_GN_reg_10 = folder_4 + f"{signal_name}_ImDataParams__reg10_GN_w_init.dcm_WFIparams.mat"

anatomies_folder = "Z:\\Kronthaler\\Conferences\\ISMRM2022\\Abstract\\UTE_sDixon_DifferentApplications\\"
anatomies_path = anatomies_folder + f"{signal_name}_ImDataParams.mat"

image_gn_4_reg_10 = ImDataParamsBMRR(anatomies_path)
image_gn_4_reg_10.load_WFIparams(WFIpath_4_GN_reg_10)

image_gn_2_reg_10 = ImDataParamsBMRR(anatomies_path)
image_gn_2_reg_10.load_WFIparams(WFIpath_2_GN_reg_10)

line_plot_vs_2_images(image_gn_4_reg_10, image_gn_2_reg_10)
