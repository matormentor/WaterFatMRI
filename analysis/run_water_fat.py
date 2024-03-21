from water_fat_lib.runs import gn_fit_run


signal_name = "BWS_ImDataParams.mat"

anatomies_folder = "Z:\\Kronthaler\\Conferences\\ISMRM2022\\Abstract\\UTE_sDixon_DifferentApplications\\"
anatomies_path = anatomies_folder + f"{signal_name}_ImDataParams.mat"

gn_fit_run(image_name=signal_name, path=anatomies_folder, do_forward=False, is_lung=False, folder="")
