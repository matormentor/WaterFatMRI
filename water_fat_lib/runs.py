import os

from water_fat_lib.app.water_fat_generator.generators import *
from water_fat_lib.app.water_fat_generator.generator import *
from water_fat_lib.app.data_loader.data_io import load_data, export_data


def phantom_fit_run(image_name, folder, path, do_forward, is_lung):
    data_name = folder + image_name.replace('.mat', '_')
    image_path = os.path.join(os.getcwd(), path, image_name)
    print(image_path)

    image, echo_time_s = load_data(image_path=image_path, return_echo_time=True)

    image.WFIparams['water'], image.WFIparams['fat'], image.WFIparams['phi'], filtered_signal, is_modelled = phantom_fit_generator(
        image=image,
        theta_name='model_theta',
        get_water_fat=True,
        do_forward=do_forward,
        is_lung=is_lung,
        sig_path=f'../output_signals_phi/{data_name}')

    params2save = {'WFIparams': ['water', 'fat', "phi", "forward_phase", "UTEphase_after_forward", "UTEphase_after_fit"],
                   'ImDataParams': ['signal', "B0dir"],
                   'Masks': ['tissueMask']}

    output_path = f"../output_signals_phi/{data_name}_PolyFit_no_weights.dcm"
    print("Dicom saved at: ", os.path.dirname(output_path))
    image.ImDataParams['TE_s'] = echo_time_s
    export_data(image=image, image_name=image_name, params2save=params2save, output_path=output_path)


def fit_run(image_name, folder, path, do_forward, is_lung):
    data_name = folder + image_name.replace('.mat', '_')
    image_path = os.path.join(os.getcwd(), path, image_name)
    print(image_path)

    image, echo_time_s = load_data(image_path=image_path, return_echo_time=True)

    image.WFIparams['water'], image.WFIparams['fat'], image.WFIparams['phi'], filtered_signal, is_modelled = fit_generator(
        image=image,
        theta_name='model_theta',
        get_water_fat=True,
        do_forward=do_forward,
        is_lung=is_lung,
        sig_path=f'../output_signals_phi/{data_name}')

    params2save = {'WFIparams': ['water', 'fat', 'phi', 'forward_phase', "UTEphase_after_forward", "UTEphase_after_fit"],
                   'ImDataParams': ['signal', "B0dir"],
                   'Masks': ['tissueMask']}

    output_path = f"../output_signals_phi/{data_name}_PolyFit_no_weights.dcm"
    image.ImDataParams['TE_s'] = echo_time_s
    export_data(image=image, image_name=image_name, params2save=params2save, output_path=output_path)


def gn_run(image_name, folder, path, do_forward, is_lung):
    reg_list = [1, 10, 100]
    data_name = folder + image_name.replace('.mat', '_')
    image_path = os.path.join(os.getcwd(), path, image_name)
    print(image_path)

    image, echo_time_s = load_data(image_path=image_path, return_echo_time=True)

    for reg in reg_list:
        image.ImDataParams['water'], image.ImDataParams['fat'], phi, filtered_signal = water_fat_gauss_newton_generator(
            image=image,
            theta_name='model_theta',
            reg=reg,
            do_forward=do_forward,
            is_lung=is_lung,
            sig_path=f'../output_signals_phi/{data_name}')

        params2save = {'WFIparams': ['water', 'fat', 'phi', 'forward_phase'],
                       'ImDataParams': ['signal'],
                       'Masks': 'tissueMask'}

        output_path = f"../output_signals_phi/{data_name}_reg{reg}_GN.dcm"
        image.ImDataParams['TE_s'] = echo_time_s
        export_data(image=image, image_name=image_name, params2save=params2save, output_path=output_path)


def gn_run_ute_init(image_name, folder, path, do_forward, is_lung):
    reg_list = [1, 10, 100]
    data_name = folder + image_name.replace('.mat', '_')
    image_path = os.path.join(os.getcwd(), path, image_name)
    print(image_path)

    image, echo_time_s = load_data(image_path=image_path, return_echo_time=True)

    for reg in reg_list:
        image.ImDataParams['water'], image.ImDataParams['fat'], phi, filtered_signal = water_fat_gauss_newton_generator(
            image=image,
            theta_name='model_theta',
            reg=reg,
            do_forward=do_forward,
            is_lung=is_lung,
            initial_phi=[1],
            sig_path=f'../output_signals_phi/{data_name}')

        params2save = {'WFIparams': ['water', 'fat', 'phi', 'forward_phase'],
                       'ImDataParams': ['signal'],
                       'Masks': 'tissueMask'}

        output_path = f"../output_signals_phi/{data_name}_reg{reg}_GN_UTE.dcm"
        image.ImDataParams['TE_s'] = echo_time_s
        export_data(image=image, image_name=image_name, params2save=params2save, output_path=output_path)


def gn_fit_run(image_name, folder, path, do_forward, is_lung):
    reg_list = [1, 10, 100]
    data_name = folder + image_name.replace('.mat', '_')
    image_path = os.path.join(os.getcwd(), path, image_name)
    print(image_path)

    image, echo_time_s = load_data(image_path=image_path, return_echo_time=True)

    for reg in reg_list:
        water1, fat1, fitted_phase, filtered_signal, is_modelled = fit_generator(
            image=image,
            theta_name='model_theta',
            get_water_fat=True,
            do_forward=do_forward,
            is_lung=is_lung)

        image.ImDataParams['water'], image.ImDataParams['fat'], phi, filtered_signal_gn = water_fat_gauss_newton_generator(
            image=image,
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

        output_path = f"../output_signals_phi/{data_name}_reg{reg}_GN_w_init.dcm"
        image.ImDataParams['TE_s'] = echo_time_s
        export_data(image=image, image_name=image_name, params2save=params2save, output_path=output_path)
