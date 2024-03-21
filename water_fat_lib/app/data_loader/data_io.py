from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR

import os
import numpy as np


def load_data(image_path, return_echo_time=False):

    if ".mat" in image_path:
        image = ImDataParamsBMRR(image_path)
    else:
        image = ImDataParamsBMRR(image_path, dicom_enhanced=True)

    echo_time_s = image.ImDataParams['TE_s'].astype(float)

    if isinstance(image.ImDataParams['TE_s'], np.ndarray):
        image.ImDataParams['TE_s'] = image.ImDataParams['TE_s'].tolist()
    try:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s'][0]]  # set_theta does not work for more than 1 TEs
    except TypeError as e:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s']]  # If it is a float
        print(e)

    if return_echo_time:
        return image, echo_time_s
    return image


def export_data(image: ImDataParamsBMRR, image_name: str, params2save: dict, output_path: str):
    if ".mat" in image_name:
        image.save_WFIparams(savename=output_path)
    else:
        image.export_DICOM(filename=output_path, params2save=params2save, image_shape_changed=True)
    print("Dicom saved at: ", os.path.dirname(output_path))
