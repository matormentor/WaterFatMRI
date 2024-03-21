import os
from water_fat_lib.app.water_fat_generator.generators import *
from water_fat_lib.app.water_fat_generator.generator import *
from bmrr_wrapper.Interfaces.ImDataParams.ImDataParamsBMRR import ImDataParamsBMRR


def phantom_fit_run(image_name, folder, path, forward_modelling, is_lung):
    data_name = folder + image_name.replace('.mat', '_')

    if ".mat" in image_name:
        image = ImDataParamsBMRR(os.path.join(os.getcwd(), path, image_name))
    else:
        image = ImDataParamsBMRR(os.path.join(os.getcwd(), path, image_name), dicom_enhanced=True)

    echo_time_s = image.ImDataParams['TE_s'].astype(float)

    if isinstance(image.ImDataParams['TE_s'], np.ndarray):
        image.ImDataParams['TE_s'] = image.ImDataParams['TE_s'].tolist()
    try:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s'][0]]  # set_theta does not work for more than 1 TEs
    except TypeError as e:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s']]
        print(e)

    image.WFIparams['water'], image.WFIparams['fat'], image.WFIparams['phi'], filtered_signal, is_modelled = phantom_fit_generator(
            image=image,
            theta_name='model_theta',
            get_water_fat = True,
            do_forward=forward_modelling,
            is_lung=is_lung,
            sig_path=f'../output_signals_phi/{data_name}')

    params2save = {'WFIparams': ['water', 'fat', "phi", "forward_phase", "UTEphase_after_forward", "UTEphase_after_fit"],
                   'ImDataParams': ['signal', "B0dir"],
                   'Masks': ['tissueMask']}
    signal_path = f"../output_signals_phi/{data_name}_PolyFit_no_weights"
    print("Dicom saved at: ", os.path.dirname(signal_path))
    image.ImDataParams['TE_s'] = echo_time_s
    if ".mat" in image_name:
        image.save_WFIparams(savename=str(signal_path + ".dcm"))
    else:
        image.export_DICOM(filename=signal_path, params2save=params2save, image_shape_changed=True)


def fit_run(image_name, folder, path, forward_modelling, is_lung):
    data_name = folder + image_name.replace('.mat', '_')

    if ".mat" in image_name:
        image = ImDataParamsBMRR(os.path.join(os.getcwd(), path, image_name))
    else:
        image = ImDataParamsBMRR(os.path.join(os.getcwd(), path, image_name), dicom_enhanced=True)

    echo_time_s = image.ImDataParams['TE_s'].astype(float)

    if isinstance(image.ImDataParams['TE_s'], np.ndarray):
        image.ImDataParams['TE_s'] = image.ImDataParams['TE_s'].tolist()
    try:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s'][0]]  # set_theta does not work for more than 1 TEs
    except TypeError as e:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s']]
        print(e)

    image.WFIparams['water'], image.WFIparams['fat'], image.WFIparams['phi'], filtered_signal, is_modelled = fit_generator(
            image=image,
            theta_name='model_theta',
            get_water_fat=True,
            do_forward=forward_modelling,
            is_lung=is_lung,
            sig_path=f'../output_signals_phi/{data_name}')

    params2save = {'WFIparams': ['water', 'fat', 'phi', 'forward_phase', "UTEphase_after_forward", "UTEphase_after_fit"],
                   'ImDataParams': ['signal'],
                   'Masks': ['tissueMask']}
    signal_path = f"../output_signals_phi/{data_name}_PolyFit_no_weights.dcm"
    print("Dicom saved at: ", os.path.dirname(signal_path))
    image.ImDataParams['TE_s'] = echo_time_s
    if ".mat" in image_name:
        image.save_WFIparams(savename=signal_path)
    else:
        image.export_DICOM(filename=signal_path, params2save=params2save, image_shape_changed=True)


def gn_run(image_name, folder, path, forward_modelling, is_lung):
    reg_list = [1, 10, 100]
    data_name = folder + image_name.replace('.mat', '_')
    print(os.path.join(os.getcwd(), path, image_name))

    if ".mat" in image_name:
        image = ImDataParamsBMRR(os.path.join(os.getcwd(), path, image_name))
    else:
        image = ImDataParamsBMRR(os.path.join(os.getcwd(), path, image_name), dicom_enhanced=True)

    echo_time_s = image.ImDataParams['TE_s'].astype(float)

    if isinstance(image.ImDataParams['TE_s'], np.ndarray):
        image.ImDataParams['TE_s'] = image.ImDataParams['TE_s'].tolist()
    try:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s'][0]]  # set_theta does not work for more than 1 TEs
    except TypeError as e:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s']]
        print(e)

    for reg in reg_list:
        water, fat, phi, filtered_signal = water_fat_gauss_newton_generator(image=image,
                                                                            theta_name='model_theta',
                                                                            reg=reg,
                                                                            do_forward=forward_modelling,
                                                                            is_lung=is_lung,
                                                                            sig_path=f'../output_signals_phi/{data_name}')

        params2save = {'WFIparams': ['water', 'fat', 'phi', 'forward_phase'],
                       'ImDataParams': ['signal'],
                       'Masks': 'tissueMask'}

        signal_path = f"../output_signals_phi/{data_name}_reg{reg}_GN.dcm"
        print("Dicom saved at: ", os.path.dirname(signal_path))
        image.ImDataParams['water'] = water
        image.ImDataParams['fat'] = fat
        image.ImDataParams['TE_s'] = echo_time_s

        if ".mat" in image_name:
            image.save_WFIparams(savename=signal_path)
        else:
            image.export_DICOM(filename=signal_path, params2save=params2save, image_shape_changed=True)


def gn_run_ute_init(image_name, folder, path, forward_modelling, is_lung):
    reg_list = [1, 10, 100]
    data_name = folder + image_name.replace('.mat', '_')
    print(os.path.join(os.getcwd(), path, image_name))

    if ".mat" in image_name:
        image = ImDataParamsBMRR(os.path.join(os.getcwd(), path, image_name))
    else:
        image = ImDataParamsBMRR(os.path.join(os.getcwd(), path, image_name), dicom_enhanced=True)

    echo_time_s = image.ImDataParams['TE_s'].astype(float)

    if isinstance(image.ImDataParams['TE_s'], np.ndarray):
        image.ImDataParams['TE_s'] = image.ImDataParams['TE_s'].tolist()
    try:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s'][0]]  # set_theta does not work for more than 1 TEs
    except TypeError as e:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s']]
        print(e)

    for reg in reg_list:
        water, fat, phi, filtered_signal = water_fat_gauss_newton_generator(image=image,
                                                                            theta_name='model_theta',
                                                                            reg=reg,
                                                                            do_forward=forward_modelling,
                                                                            is_lung=is_lung,
                                                                            initial_phi=[1],
                                                                            sig_path=f'../output_signals_phi/{data_name}')

        params2save = {'WFIparams': ['water', 'fat', 'phi', 'forward_phase'],
                       'ImDataParams': ['signal'],
                       'Masks': 'tissueMask'}

        signal_path = f"../output_signals_phi/{data_name}_reg{reg}_GN.dcm"
        print("Dicom saved at: ", os.path.dirname(signal_path))
        image.ImDataParams['water'] = water
        image.ImDataParams['fat'] = fat
        image.ImDataParams['TE_s'] = echo_time_s

        if ".mat" in image_name:
            image.save_WFIparams(savename=signal_path)
        else:
            image.export_DICOM(filename=signal_path, params2save=params2save, image_shape_changed=True)


def gn_fit_run(image_name, folder, path, forward_modelling, is_lung):
    reg_list = [10]  # [1, 10, 100]
    data_name = folder + image_name.replace('.mat', '_')

    if ".mat" in image_name:
        image = ImDataParamsBMRR(os.path.join(os.getcwd(), path, image_name))
    else:
        image = ImDataParamsBMRR(os.path.join(os.getcwd(), path, image_name), dicom_enhanced=True)

    echo_time_s = image.ImDataParams['TE_s'].astype(float)

    if isinstance(image.ImDataParams['TE_s'], np.ndarray):
        image.ImDataParams['TE_s'] = image.ImDataParams['TE_s'].tolist()
    try:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s'][0]]  # set_theta does not work for more than 1 TEs
    except TypeError as e:
        image.ImDataParams['TE_s'] = [image.ImDataParams['TE_s']]  # If it is a float
        print(e)

    for reg in reg_list:
        water1, fat1, fitted_phase, filtered_signal, is_modelled = fit_generator(image=image,
                                                                                 theta_name='model_theta',
                                                                                 get_water_fat=True,
                                                                                 do_forward=forward_modelling,
                                                                                 is_lung=is_lung)

        # I.ImDataParams['signal'] = np.expand_dims(filtered_signal, axis=3)

        water, fat, phi, filtered_signal_gn = water_fat_gauss_newton_generator(image=image,
                                                                               theta_name='model_theta',
                                                                               reg=reg,
                                                                               do_forward=False,
                                                                               initial_phi=fitted_phase,
                                                                               initial_water=water1,
                                                                               initial_fat=fat1,
                                                                               is_modelled=is_modelled,
                                                                               is_lung=is_lung,
                                                                               sig_path=f'../output_signals_phi/{data_name}')

        params2save = {'WFIparams': ['water', 'fat', 'phi', 'forward_phase', "fit_phase"],
                       'ImDataParams': ['signal'],
                       'Masks': 'tissueMask'}

        signal_path = f"../output_signals_phi/{data_name}_reg{reg}_GN_w_init.dcm"
        print("Dicom saved at: ", os.path.dirname(signal_path))
        image.ImDataParams['water'] = water
        image.ImDataParams['fat'] = fat
        image.ImDataParams['TE_s'] = echo_time_s

        if ".mat" in image_name:
            image.save_WFIparams(savename=signal_path)
        else:
            image.export_DICOM(filename=signal_path, params2save=params2save, image_shape_changed=True)
