from MateoLib.app.helper.phase_theta_operations import *
from MateoLib.app.fit.fit_functions import *
from MateoLib.app.fit.fit import fit

from bmrr_wrapper.Interfaces.ImDataParams.ImDataParamsBMRR import ImDataParamsBMRR

from MateoLib.app.helper.setUp import main_set_up, fit_set_up, gn_set_up


def fit_generator(image: ImDataParamsBMRR, theta_name: str, get_water_fat=False, sig_path='', do_forward=True, is_lung: bool = False):
    # method = 'Fit'
    print("Starting Polynom Fit")

    # _______________________________ SETUP ______________________________________
    print('Getting setup...')

    # Initialize mask, unwrap phase and fat model with theta
    filled_mask = image.get_tissueMaskFilled(10)
    fit_mask = filled_mask
    if do_forward and is_lung:
        fit_mask = image.get_tissueMask(21)  # normally is with filled and at 10, 21 is a good approximation for Lung.
    image.Masks['tissueMask'] = filled_mask
    image.BFRparams['BFRmask'] = image.Masks['tissueMask']

    image.set_UTEphase()

    is_modelled = main_set_up(image, do_forward=do_forward, is_lung=is_lung)

    masked_signal, masked_phase, smooth_phase = fit_set_up(image=image, filled_mask=filled_mask)

    # ________________________________ Define weights ___________________________________________

    # Find the center of mass set loss weights

    # Center = torch.as_tensor(center_of_mass(filled_mask)).to(device)
    # weights = torch.exp(-(torch.abs(z_tensor - Center[2])/(z_tensor.shape[2])) -
    # 10*(torch.abs(y_tensor - Center[1])/(y_tensor.shape[1]))).cpu()

    # Weight by signal magnitude

    weights = torch.as_tensor(np.abs(masked_signal)) / np.abs(masked_signal).max()
    # weights=None

    # Weight by deviation from mean

    # weights = torch.as_tensor(np.abs(masked_signal - np.mean(masked_signal[fit_mask]))/np.std(masked_signal[fit_mask]))
    # _____________________________ Fitting Polynom ____________________________________________

    fitted_phase = fit(function=poly_to2nd_3d, nparams=10, phase=smooth_phase, weights=weights, fit_mask=fit_mask)['fitted_phase']
    fitted_phase[~filled_mask] = 0

    # _____________________________ Subtracting fitted polynom phase _______________________________________
    phase_after_fit = masked_phase - fitted_phase.numpy()
    image.WFIparams['UTEphase_after_fit'], image.WFIparams['fit_phase'] = phase_after_fit, fitted_phase.numpy()
    filtered_signal = np.abs(masked_signal) * np.exp(1.0j * phase_after_fit)

    filtered_signal[~filled_mask] = 0

    if get_water_fat:

        print('Getting Water and Fat...')

        if theta_name == 'model_theta':
            fat, water = create_fat_water_sep(signal=filtered_signal,
                                              theta=image.WFIparams['theta'],
                                              tissue_mask=filled_mask)

        else:
            raise KeyError("Please use theta: 'model_theta'")

        if sig_path:
            print(theta_name)
            # print('Saving signals')

            # if shift_signal:

            #     water_path = sig_path + 'water' + method + f"Shift_theta{theta_name}" + '.pickle'
            #     with open(water_path, 'wb') as water_file:
            #         pickle.dump(water, water_file, protocol=pickle.HIGHEST_PROTOCOL)

            #     fat_path = sig_path + 'fat' + method + f"Shift_theta{theta_name}" + '.pickle'
            #     with open(fat_path, 'wb') as fat_file:
            #         pickle.dump(fat, fat_file, protocol=pickle.HIGHEST_PROTOCOL)

            #     phi_path = sig_path + 'phi' + method + '.pickle'
            #     with open(phi_path, 'wb') as phi_file:
            #         pickle.dump(fitted_phase, phi_file, protocol=pickle.HIGHEST_PROTOCOL)

            #     signal_path = sig_path + 'signal' + method + f"Shift_theta{theta_name}" + '.pickle'
            #     with open(signal_path, 'wb') as signal_file:
            #         pickle.dump(filtered_signal, signal_file, protocol=pickle.HIGHEST_PROTOCOL)

            # else:

            #     water_path = sig_path + 'water' + method + f"NoShift_theta{theta_name}" + '.pickle'
            #     with open(water_path, 'wb') as water_file:
            #         pickle.dump(water, water_file, protocol=pickle.HIGHEST_PROTOCOL)

            #     fat_path = sig_path + 'fat' + method + f"NoShift_theta{theta_name}" + '.pickle'
            #     with open(fat_path, 'wb') as fat_file:
            #         pickle.dump(fat, fat_file, protocol=pickle.HIGHEST_PROTOCOL)

            #     phi_path = sig_path + 'phi' + method + '.pickle'
            #     with open(phi_path, 'wb') as phi_file:
            #         pickle.dump(fitted_phase, phi_file, protocol=pickle.HIGHEST_PROTOCOL)

            #     signal_path = sig_path + 'signal' + method + f"NoShift_theta{theta_name}" + '.pickle'
            #     with open(signal_path, 'wb') as signal_file:
            #         pickle.dump(filtered_signal, signal_file, protocol=pickle.HIGHEST_PROTOCOL)

            print('Finished Polynom Fit Save')
        print('Finished Polynom Fit')
        return water, fat, fitted_phase.numpy(), filtered_signal, is_modelled

    return 0, 0, 0, 0, False


def water_fat_gauss_newton_generator(image: ImDataParamsBMRR, reg: float, theta_name='', sig_path='', initial_phi=None, initial_water=None, initial_fat=None,
                                     do_forward=True, is_modelled=False, is_lung: bool = False):
    initial_phi = [] if initial_phi is None else initial_phi
    initial_water = [] if initial_water is None else initial_water
    initial_fat = [] if initial_fat is None else initial_fat

    method = 'GN'
    if len(initial_phi) > 0:
        method = 'GN_w_Fit_Initialization'

    print(f"Starting {method}")

    print('Getting setup...')

    filled_mask = image.get_tissueMaskFilled(10)  # normally is with filled and at 10
    image.Masks['tissueMask'] = filled_mask
    image.BFRparams['BFRmask'] = image.Masks['tissueMask']

    if not is_modelled:
        image.set_UTEphase()

    main_set_up(image=image, do_forward=do_forward, is_lung=is_lung)

    gn_set_up(image=image, reg=reg, initial_phi=initial_phi, initial_water=initial_water, initial_fat=initial_fat)

    print('Fitting...')

    image.UTEWFIgn()

    print('Finished fitting')

    phase_after_gn = image.WFIparams['UTEphase'] - image.WFIparams['phi']

    image.WFIparams['UTEphase_after_gn'] = phase_after_gn

    filtered_signal = np.abs(image.ImDataParams['signal'][..., 0]) * np.exp(1.0j * phase_after_gn)

    filtered_signal[~filled_mask] = 0

    phi = image.WFIparams['phi']
    print('Getting Water and Fat')

    fat, water = create_fat_water_sep(filtered_signal,
                                      theta=image.WFIparams['theta'],
                                      tissue_mask=filled_mask)

    if sig_path:
        print(theta_name)
        # print('Saving signals')
        #
        # water_path = sig_path + 'water' + method + f"NoShift_reg{reg}_theta{theta_name}" + '.pickle'
        # with open(water_path, 'wb') as water_file:
        #     pickle.dump(water, water_file, protocol=pickle.HIGHEST_PROTOCOL)
        #
        # fat_path = sig_path + 'fat' + method + f"NoShift_reg{reg}_theta{theta_name}" + '.pickle'
        # with open(fat_path, 'wb') as fat_file:
        #   pickle.dump(fat, fat_file, protocol=pickle.HIGHEST_PROTOCOL)
        #
        # phi_path = sig_path + 'phi' + method + f'_reg{reg}.pickle'
        # with open(phi_path, 'wb') as phi_file:
        #     pickle.dump(phi, phi_file, protocol=pickle.HIGHEST_PROTOCOL)
        #
        # signal_path = sig_path + 'signal' + method + f"NoShift_reg{reg}_theta{theta_name}" + '.pickle'
        # with open(signal_path, 'wb') as signal_file:
        #     pickle.dump(filtered_signal, signal_file, protocol=pickle.HIGHEST_PROTOCOL)

    print(f'Finished {method}')
    return water, fat, phi, filtered_signal
