import matplotlib.pyplot as plt
import numpy as np
from water_fat_lib.app.plot.signal_loader.signal_loader import load_fat_water
from typing import List


def plot_just_negative(fat: np.array, water: np.array, title: str, imag_slice=59, save_path=''):
    if not imag_slice:
        imag_slice = fat.shape[2] // 2
    fatsuplim = 0.0
    watersuplim = 0.0
    fatlowlim = fat[:, :, imag_slice].min()
    waterlowlim = water[:, :, imag_slice].min()
    if fatlowlim >= 0.0:
        fatlowlim = -0.0001
    if waterlowlim >= 0.0:
        waterlowlim = -0.0001

    # plotting
    fig, axes = plt.subplots(1, 2, layout='constrained', figsize=(7, 5))
    axes[0].set_title('fat')
    axes[1].set_title('water')
    fig.suptitle(title, y=1)
    img3 = axes[0].imshow(fat[:, :, imag_slice], vmin=fatlowlim, vmax=fatsuplim, cmap='gray')
    img4 = axes[1].imshow(water[:, :, imag_slice], vmin=waterlowlim, vmax=watersuplim, cmap='gray')
    bar = img4
    if fatsuplim > watersuplim:
        bar = img3
    fig.colorbar(bar, ax=[axes[0], axes[1]], shrink=0.7)
    if save_path:
        plt.savefig(save_path, format='png')


def plot_water_fat(fat: np.array, water: np.array, title: str, fulldynamicrange=False, imag_slice=None, save_path=''):
    if not imag_slice:
        imag_slice = fat.shape[3] // 2

    # plotting
    cm = 1 / 2.54
    fig, axes = plt.subplots(fat.shape[0], 2, layout='constrained', figsize=(5 * cm, 5 * cm), sharex=True, sharey=True)
    val_list = []
    img_list = []
    for i in range(0, fat.shape[0], 1):
        fatsuplim = fat[i, :, :, imag_slice].max()
        watersuplim = water[i, :, :, imag_slice].max()
        fatlowlim = fat[i, :, :, imag_slice].min()
        waterlowlim = water[i, :, :, imag_slice].min()
        if not fulldynamicrange:
            fatsuplim = np.percentile(fat[i, :, :, imag_slice], 99)
            watersuplim = np.percentile(water[i, :, :, imag_slice], 99)
            fatlowlim = 0
            waterlowlim = 0
        val_list.append(max(fatsuplim, watersuplim))
        # fig.suptitle(title, y=0.88)
        img3 = axes[i, 0].imshow(fat[i, :, :, imag_slice], vmin=fatlowlim, vmax=1, cmap='gray')
        axes[i, 0].tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
        img4 = axes[i, 1].imshow(water[i, :, :, imag_slice], vmin=waterlowlim, vmax=1, cmap='gray')
        axes[i, 1].tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
        img_list.append(img4)
        if fatsuplim > watersuplim:
            img_list.pop()
            img_list.append(img3)
        row_names = ["GN", "GN + Init."]
        axes[i, 0].set_ylabel(row_names[i], fontsize="large")

    axes[0, 0].set_title('Fat', fontsize="large")
    axes[0, 1].set_title('Water', fontsize="large")
    print(title)
    # fig.suptitle(title, y=1.02)
    # index = val_list.index(max(val_list))
    # fig.colorbar(img_list[index], ax=axes, shrink=0.7)

    if save_path:
        plt.savefig(save_path, format='png', bbox_inches="tight")


def plot_phis(signal_phis: np.array, titles: np.array, reg: float, imag_slice=None, save_path=''):
    if not imag_slice:
        imag_slice = signal_phis.shape[3] // 2
    fig, axes = plt.subplots(1, signal_phis.shape[0], layout='constrained', figsize=(15, 7))
    val_list = []
    img_list = []
    for i in range(0, signal_phis.shape[0], 1):
        phisuplim = signal_phis[i, :, :, imag_slice].max()
        philowlim = signal_phis[i, :, :, imag_slice].min()
        val_list.append(phisuplim)
        # plotting
        axes[i].set_title(titles[i])
        img = axes[i].imshow(signal_phis[i, :, :, imag_slice], vmin=philowlim, vmax=phisuplim, cmap='gray')
        img_list.append(img)
        axes[i].tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
        # fig.colorbar(img, ax=axes[i], shrink=0.77)
    # index = val_list.index(max(val_list))
    # fig.colorbar(img_list[index], ax=axes, shrink=0.7)
    fig.suptitle(fr"Fitted Phase $\phi$ with regularization {reg}", y=0.92)
    if save_path:
        plt.savefig(save_path, format='png')


def plot_load_water_fat(signal_path: str, signal_name: str, methods: List[str], theta_value: str, reg=None, fig_path=''):
    title = ""
    list_fat = []
    list_water = []
    method_names = []
    for method in methods:
        method_name = method
        if method == 'FitShift':
            method_name = 'Polynomial Fit with Shift'
        elif method == 'FitNoShift':
            method_name = 'Polynomial Fit'  # Default is no shift
        elif method == 'GNNoShift':
            method_name = 'Gauss Newton'  # Default is no shift
        elif method == 'GN_w_Fit_InitializationShift':
            method_name = 'Gauss Newton with Polynomial Fit Initialization with Shift'
        elif method == 'GN_w_Fit_InitializationNoShift':
            method_name = 'Gauss Newton with Polynomial Fit Initialization'  # Default is No Shift
        method_names.append(method_name)
        print(method_name)
        print(reg)

        if reg:
            fig_path = fig_path + f"fat_water{signal_name}_reg{reg}"
            title = f"Fat Water {signal_name} with Reg {reg}"
        else:
            fig_path = fig_path + f"fat_water{signal_name}_{method}"
            title = f"Fat Water {signal_name} {method_name}"
        if "NoShift" in method:
            theta_value = "model_theta"
        else:
            theta_value = "theta_estimation"
        fat, water = load_fat_water(path=signal_path, signal_name=signal_name, method=method, theta_value=theta_value,
                                    reg=reg)
        list_fat.append(fat)
        list_water.append(water)
    fig_path += ".png"
    print(theta_value)
    list_fat = np.array(list_fat)
    list_water = np.array(list_water)
    plot_water_fat(fat=list_fat, water=list_water, title=title, fulldynamicrange=False, save_path=fig_path)
