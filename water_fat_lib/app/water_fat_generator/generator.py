from water_fat_lib.app.helper.phase_theta_operations import *
from water_fat_lib.app.fit.fit_functions import *
from water_fat_lib.app.fit.fit import fit

from scipy.ndimage import binary_erosion
from bmrr_wrapper.Interfaces.ImDataParams.ImDataParamsBMRR import ImDataParamsBMRR

from water_fat_lib.app.helper.setUp import main_set_up, fit_set_up


def phantom_fit_generator(image: ImDataParamsBMRR, theta_name: str, get_water_fat=False, sig_path='', do_forward=True, is_lung: bool = False):
    # method = 'Fit'
    print("Starting Polynom Fit")

    # _______________________________ SETUP ______________________________________

    print('Getting setup...')

    # Initialize mask, unwrap phase and fat model with theta
    filled_mask = image.get_tissueMaskFilled(10)
    image.Masks['tissueMask'] = filled_mask
    image.BFRparams['BFRmask'] = image.Masks['tissueMask']

    image.set_UTEphase()

    # Set Fit Masks

    fat_mask = np.ones_like(filled_mask)
    fat_mask[image.WFIparams["UTEphase"] > -3] = 0  # Limit set by looking at phantom
    water_mask = filled_mask != fat_mask

    kernel = np.ones((3, 3, 3), np.uint8)
    water_mask = binary_erosion(water_mask, kernel, iterations=1)
    fat_mask = binary_erosion(fat_mask, kernel, iterations=1)
    mix_mask = water_mask.astype(bool) + fat_mask.astype(bool)
    fit_masks = water_mask, fat_mask

    is_modelled = main_set_up(image=image, do_forward=do_forward, is_lung=is_lung)

    masked_signal, masked_phase, smooth_phase = fit_set_up(image=image, filled_mask=filled_mask)

    plt.imshow(smooth_phase[:, :, 161])
    img_name = sig_path.split("/")[-1]
    plt.title(f"Phase after Smoothing Check for: {img_name}")
    plt.show()
    # return 0

    # ________________________________ Define weights ___________________________________________

    weights = None

    # _____________________________ Fitting Polynom ____________________________________________   

    fitted_phase = np.zeros_like(masked_phase)
    for fit_mask in fit_masks:
        partial_fitted_phase = fit(function=poly_to2nd_3d, nparams=10, phase=smooth_phase, weights=weights, fit_mask=fit_mask)['fitted_phase']
        fitted_phase[fit_mask] = partial_fitted_phase[fit_mask]

    # _____________________________ Subtracting fitted polynom phase _______________________________________

    phase_after_fit = masked_phase - fitted_phase
    phase_after_fit[~mix_mask] = 0
    image.WFIparams['UTEphase_after_fit'], image.WFIparams['fit_phase'] = phase_after_fit, fitted_phase
    filtered_signal = np.abs(masked_signal) * np.exp(1.0j * phase_after_fit)
    filtered_signal[~filled_mask] = 0

    if get_water_fat:

        print('Getting Water and Fat...')

        if theta_name == 'model_theta':
            fat, water = create_fat_water_sep(signal=filtered_signal,
                                              theta=image.WFIparams['theta'],
                                              tissue_mask=filled_mask)

        else:
            raise KeyError("Please use one of the following thetas: ['model_theta', 'theta_estimation']")

        return water, fat, fitted_phase, filtered_signal, is_modelled

    print('Finished Polynom Fit')
    return 0, 0, 0, 0, False
