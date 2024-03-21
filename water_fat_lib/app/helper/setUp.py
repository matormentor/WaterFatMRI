from typing import NamedTuple, MutableSequence

from MateoLib.app.fit.model_field_map import subtract_b0_phase
from MateoLib.app.helper.phase_theta_operations import get_phase_median_filtered


class FitSetUp(NamedTuple):
    masked_signal: MutableSequence
    masked_phase: MutableSequence
    smooth_phase: MutableSequence


def main_set_up(image, do_forward, is_lung):

    is_modelled = False
    if do_forward:
        subtract_b0_phase(image, is_lung=is_lung)
        is_modelled = True

    # scale magnitude between 0 and 1
    image.normalize_signalMag()  # WHY??
    # choose Ren Marrow Fat model
    image.set_FatModel('Ren marrow')
    image.set_paddingParams()

    image.set_theta()
    print('Theta: ', image.WFIparams['theta'])

    return is_modelled


def fit_set_up(image, filled_mask):
    print('Setting up variables')
    # Set variables
    signal = image.ImDataParams['signal'][..., 0]
    phase = image.WFIparams['UTEphase']

    # _______________________________ MASKING/SMOOTHING ______________________________________

    # Mask signal
    masked_signal, masked_phase = signal, phase
    masked_signal[~filled_mask], masked_phase[~filled_mask] = 0, 0

    # Smooth the phase for better fitting
    smooth_phase = get_phase_median_filtered(masked_phase)
    smooth_phase[~filled_mask] = 0
    return FitSetUp(masked_signal, masked_phase, smooth_phase)


def gn_set_up(image, reg, initial_phi, initial_fat, initial_water):
    # run separation
    image.AlgoParams['lamdaUTE_1'] = reg
    image.AlgoParams['max_iter'] = 100
    image.AlgoParams['reltol_update'] = 0.01
    if len(initial_phi) > 0:
        image.AlgoParams['initial_phi'] = initial_phi
        # image.AlgoParams["initial_phi"] = copy.deepcopy(image.WFIparams["UTEphase"])  # TODO: try UTEphase initialization:
        # print("set UTEphase as initialization.")
    if len(initial_fat) > 0:  # initial_fat.size(dim=0) > 0
        image.AlgoParams['initial_fat'] = initial_fat
    if len(initial_water) > 0:
        image.AlgoParams['initial_water'] = initial_water
