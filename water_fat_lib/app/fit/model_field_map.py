from bmrr_wrapper.Interfaces.ImDataParams.ImDataParamsBMRR import ImDataParamsBMRR
import numpy as np  
from bmrr_wrapper.Backend.qsm.helper import simulate_RDF_ppm


def get_fieldmap_masks_for_lung(image: ImDataParamsBMRR, is_lung: bool = False):
    not_filled_mask = image.get_tissueMaskFilled(10)
    if is_lung:
        not_filled_mask = image.get_tissueMask(22)
    lung_mask = np.zeros_like(not_filled_mask).astype(int)
    lung_mask[~not_filled_mask] = 9  # +9 as described in https://onlinelibrary.wiley.com/doi/10.1002/mrm.25350
    return lung_mask


def get_phase(image: ImDataParamsBMRR, is_lung: bool = False):
    lung_mask = get_fieldmap_masks_for_lung(image=image, is_lung=is_lung)
    field_map_ppm = simulate_RDF_ppm(chi_ppm=lung_mask.copy(), voxelSize_mm=image.ImDataParams['voxelSize_mm'], B0dir=image.ImDataParams["B0dir"])
    field_map_hz = field_map_ppm * image.ImDataParams['centerFreq_Hz']/1e6  # frequency field_map in Hz
    phase = -2*np.pi*field_map_hz*image.ImDataParams['TE_s']  # - because of tests in 02_02_2023
    return phase


def subtract_b0_phase(image: ImDataParamsBMRR, is_lung: bool = False):
    phase = get_phase(image=image, is_lung=is_lung)
    print('subtracting phase')
    image.WFIparams['forward_phase'] = phase
    image.WFIparams['UTEphase'] -= phase
    image.WFIparams["UTEphase_after_forward"] = image.WFIparams["UTEphase"]
    print('phase_subtracted')
