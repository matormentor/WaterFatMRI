import copy

import numpy as np
import matplotlib.pyplot as plt
from typing import NamedTuple
from bmrr_wrapper.Interfaces.ImDataParams import ImDataParamsBMRR


def get_plt_entries(img: ImDataParamsBMRR, map_params_to_keys: dict = None, vmax=0):
    map_params_to_keys = {"WFIparams": ['water', "fat"]} if map_params_to_keys is None else map_params_to_keys
    plt_entry = []
    filled_mask = img.get_tissueMaskFilled(10)
    for params, keys in map_params_to_keys.items():
        for key in keys:
            attr = "real"
            image_to_plot = getattr(getattr(img, params)[key], attr)
            if key == "signal":
                img.Masks['tissueMask'] = img.get_tissueMaskFilled(10)
                img.set_UTEphase()
                image_to_plot = img.WFIparams["UTEphase"]
                key = "UTEphase"
            if filled_mask is None:
                filled_mask = np.ones_like(image_to_plot).astype(bool)
            plt_lim_low = np.percentile(image_to_plot[filled_mask], 2)
            plt_lim_high = np.percentile(image_to_plot[filled_mask], 98)
            # pltLimLow = image.min()
            # pltLimHigh = image.max()
            if (key in ["water", "fat"]) and (vmax == 1):
                plt_lim_low = 0
                # plt_lim_high = 1
            # elif key == "phi":
            #     plt_lim_low = -2.9
            #     plt_lim_high = -2.7
            plt_entry.append([image_to_plot, {'title': key, 'window': [plt_lim_low, plt_lim_high], 'cmap': 'gray'}])
    return plt_entry


def line_plot_keys(image: ImDataParamsBMRR, keys: list = None, shift=False, title="", center=None):
    """
    :param image: ImDataParamsBMRR instance
    :param keys: default = ["UTEphase_after_forward", "UTEphase_after_fit", "phi"]
    :param shift: if shift by pi
    :param center: point where line plots will go through
    :param title: title of the img
    """
    center = get_water_center_phantom() if center is None else center
    x, y, z = center.x, center.y, center.z

    keys = ["UTEphase", "UTEphase_after_fit", "phi", "forward_phase"] if keys is None else keys
    mask = image.get_tissueMaskFilled(10)
    image.Masks['tissueMask'] = mask
    image.set_UTEphase()
    fig = plt.figure(layout='constrained', figsize=(18, 8))
    axes = fig.subplots(3, 1)
    signals = []
    for i, key in enumerate(keys):
        signals.append(copy.deepcopy(image.WFIparams[key]))
        if shift:
            signals[i] += np.pi
            signals[i][~mask] = 0
            if key == "forward_phase":
                signals[i] += 2
                # signals[i] -= np.pi
                signals[i][~mask] = 0

    # x-axes
    axes[0].plot(range(0, signals[0].shape[0]), signals[0][:, y, z])
    axes[0].plot(range(0, signals[1].shape[0]), signals[1][:, y, z], "-.")
    axes[0].plot(range(0, signals[2].shape[0]), signals[2][:, y, z], "--")
    axes[0].plot(range(0, signals[3].shape[0]), signals[3][:, y, z], ":")
    axes[0].set_title(f'{title}: x-axes')
    # axes[0].legend([keys[0], keys[1], keys[2], keys[3]], fontsize='xx-small', bbox_to_anchor=(1.3, 1))

    # y-axes
    axes[1].plot(range(0, signals[0].shape[1]), signals[0][x, :, z])
    axes[1].plot(range(0, signals[1].shape[1]), signals[1][x, :, z], "-.")
    axes[1].plot(range(0, signals[2].shape[1]), signals[2][x, :, z], "--")
    axes[1].plot(range(0, signals[3].shape[0]), signals[3][x, :, z], ":")
    axes[1].set_title('y-axes')
    axes[1].legend([keys[0], keys[1], keys[2], keys[3]], fontsize='xx-small', bbox_to_anchor=(1.3, 1))

    # z-axes
    axes[2].plot(range(0, signals[0].shape[1]), signals[0][x, y, :])
    axes[2].plot(range(0, signals[1].shape[1]), signals[1][x, y, :], "-.")
    axes[2].plot(range(0, signals[2].shape[1]), signals[2][x, y, :], "--")
    axes[2].plot(range(0, signals[3].shape[0]), signals[3][x, y, :], ":")
    axes[2].set_title('z-axes')
    # axes[2].legend([keys[0], keys[1], keys[2], keys[3]], fontsize='xx-small', bbox_to_anchor=(1.3, 1))
    plt.show()
    

def line_plot_3_regs(reg_1: ImDataParamsBMRR, reg_2: ImDataParamsBMRR, reg_3: ImDataParamsBMRR):
    center = get_center_of_signal(reg_1)
    x, z = center.x, center.z
    # y-axes
    plt.plot(range(0, reg_1.ImDataParams["signal"].shape[1]), reg_1.WFIparams["phi"][x, :, z])
    plt.plot(range(0, reg_2.WFIparams["phi"].shape[1]), reg_2.WFIparams["phi"][x, :, z], ":")
    plt.plot(range(0, reg_3.WFIparams["phi"].shape[1]), reg_3.WFIparams["phi"][x, :, z], "--")
    plt.title('y-axes')
    plt.legend(["reg1", "reg10", "reg100"], fontsize='xx-small')
    plt.show()


def line_plot_gn_w_init(image_gn: ImDataParamsBMRR, image_gn_w_init: ImDataParamsBMRR):
    center = get_center_of_signal(image_gn)
    x, y, z = center.x, center.y, center.z
    mask = image_gn.get_tissueMaskFilled(10)
    image_gn.Masks['tissueMask'] = mask
    image_gn.set_UTEphase()
    fig = plt.figure(layout='constrained', figsize=(15, 8))
    axes = fig.subplots(3, 1)
    ute_phase = image_gn.WFIparams['UTEphase']
    fit = image_gn_w_init.WFIparams['fit_phase']
    gn_phase = image_gn.WFIparams["phi"]
    gn_w_init_phase = image_gn_w_init.WFIparams["phi"]

    # x-axes
    axes[0].plot(range(0, ute_phase.shape[0]), ute_phase[:, y, z])
    axes[0].plot(range(0, fit.shape[0]), fit[:, y, z], ":")
    axes[0].plot(range(0, gn_phase.shape[0]), gn_phase[:, y, z], "--")
    axes[0].plot(range(0, gn_w_init_phase.shape[0]), gn_w_init_phase[:, y, z], "-.")
    axes[0].set_title('x-axes')
    axes[0].legend(["UTE_Phase", "fit", "gn_phase", "gn_w_init_phase"], fontsize='xx-small')

    # y-axes
    axes[1].plot(range(0, ute_phase.shape[1]), ute_phase[x, :, z])
    axes[1].plot(range(0, fit.shape[1]), fit[x, :, z], ":")
    axes[1].plot(range(0, gn_phase.shape[1]), gn_phase[x, :, z], "--")
    axes[1].plot(range(0, gn_w_init_phase.shape[1]), gn_w_init_phase[x, :, z], "-.")
    axes[1].set_title('y-axes')
    axes[1].legend(["UTE_Phase", "fit", "gn_phase", "gn_w_init_phase"], fontsize='xx-small')

    # z-axes
    axes[2].plot(range(0, ute_phase.shape[2]), ute_phase[x, y, :])
    axes[2].plot(range(0, fit.shape[2]), fit[x, y, :], ":")
    axes[2].plot(range(0, gn_phase.shape[2]), gn_phase[x, y, :], "--")
    axes[2].plot(range(0, gn_w_init_phase.shape[2]), gn_w_init_phase[x, y, :], "-.")
    axes[2].set_title('z-axes')
    axes[2].legend(["UTE_Phase", "fit", "gn_phase", "gn_w_init_phase"], fontsize='xx-small')
    plt.show()


def line_plot_vs_2_images(image1: ImDataParamsBMRR, image2: ImDataParamsBMRR):
    mask = image1.get_tissueMaskFilled(10)
    center = get_center_of_signal(image1)
    ute_phase_after_gn_1 = image1.WFIparams["UTEphase_after_gn"]
    ute_phase_after_gn_2 = image2.WFIparams["UTEphase_after_gn"]
    ute_phase_after_gn_1[~mask] = 0
    ute_phase_after_gn_2[~mask] = 0
    ute_phase_after_gn_1 = ute_phase_after_gn_1[40, :, center.z]
    ute_phase_after_gn_2 = ute_phase_after_gn_2[40, :, center.z]
    phi_1 = image1.WFIparams["phi"][40, :, center.z]
    phi_2 = image2.WFIparams["phi"][40, :, center.z]
    fit_phase_1 = image1.WFIparams["fit_phase"][40, :, center.z]
    fit_phase_2 = image2.WFIparams["fit_phase"][40, :, center.z]

    fig = plt.figure(layout='constrained', figsize=(15, 8))
    axes = fig.subplots(3, 1)

    axes[0].plot(fit_phase_1)
    axes[0].plot(fit_phase_2)
    axes[0].legend(["3D 4th degree", "3D 2th degree"], fontsize='xx-small', loc='lower left')
    axes[0].set_title('Polynomial fit')
    axes[1].plot(phi_1)
    axes[1].plot(phi_2)
    axes[1].legend(["after 3D 4th degree", "after 3D 2th degree"], fontsize='xx-small', loc='lower left')
    axes[1].set_title('Gauss Newton fit')
    axes[2].plot(ute_phase_after_gn_1)
    axes[2].plot(ute_phase_after_gn_2)
    axes[2].legend(["after 3D 4th degree", "after 3D 2th degree"], fontsize='xx-small', loc='lower left')
    axes[2].set_title("Resulting Phase")
    plt.show()


def get_center_of_signal(image: ImDataParamsBMRR):
    x = image.ImDataParams["signal"].shape[0] // 2
    y = image.ImDataParams["signal"].shape[1] // 2
    z = image.ImDataParams["signal"].shape[2] // 2
    return Center(x=x, y=y, z=z)


class Center(NamedTuple):
    x: int
    y: int
    z: int


def get_water_center_phantom():
    return Center(x=161, y=161, z=161)


def get_fat_center_phantom():
    return Center(x=119, y=144, z=161)
