import numpy as np
from scipy.signal import wiener
from scipy.ndimage import median_filter
import matplotlib.pyplot as plt
from skimage.restoration import unwrap_phase


def get_phase_wiener_filtered(phase, size=(5, 5, 5)):
    phase_wiener_filtered = wiener(phase, size)
    return phase_wiener_filtered


def get_phase_median_filtered(phase, size=5):
    return median_filter(phase, size=size)


def create_fat_water_sep(signal: np.ndarray, theta: float, tissue_mask):
    fat = signal.imag / np.sin(theta)
    water = (signal.real - fat * np.cos(theta))
    fat[~tissue_mask], water[~tissue_mask] = 0, 0
    return fat, water


# _________________________ Signal Shifting and theta Estimation ______________________________
def get_theta_and_zero_estimation(phase_signal_filtered, tissue_mask, show_histogram=True, lower_percentile=0.5, upper_percentile=99.5):
    min_percentile_phase_signal_filtered = np.percentile(phase_signal_filtered, lower_percentile)
    max_percentile_phase_signal_filtered = np.percentile(phase_signal_filtered, upper_percentile)

    left_estimation, zero_estimation = min_percentile_phase_signal_filtered, max_percentile_phase_signal_filtered

    if show_histogram:
        lower_bound_mask_phase_signal_filtered = phase_signal_filtered >= left_estimation

        upper_bound_mask_phase_signal_filtered = phase_signal_filtered <= zero_estimation

        masked_phase_signal_filtered = phase_signal_filtered[tissue_mask & lower_bound_mask_phase_signal_filtered & upper_bound_mask_phase_signal_filtered]

        plt.hist(masked_phase_signal_filtered.flatten(),
                 bins=list(np.arange(min_percentile_phase_signal_filtered, max_percentile_phase_signal_filtered, 0.01)),
                 range=(min_percentile_phase_signal_filtered, max_percentile_phase_signal_filtered))
        plt.axvline(x=left_estimation, color='r')
        plt.axvline(x=zero_estimation, color='k')
        plt.title('Histogram Filtered Signal Phase Polynomial Fit Without Shift')
        plt.show()

    return left_estimation, zero_estimation


def get_phase_filtered_signal_shifted_mask(phase_filtered_signal_shifted, theta_estimation, tissue_mask):
    phase_filtered_signal_shifted_mask = (tissue_mask & (phase_filtered_signal_shifted <= 0) & (phase_filtered_signal_shifted >= theta_estimation))

    return phase_filtered_signal_shifted_mask


def get_signal_shifted(signal, filled_mask, show_histogram=False):
    print('Shifting Signal...')
    phase_signal_filtered = unwrap_phase(np.angle(signal))
    left_estimation, zero_estimation = get_theta_and_zero_estimation(phase_signal_filtered,
                                                                     tissue_mask=filled_mask,
                                                                     show_histogram=show_histogram)
    phase_filtered_signal_shifted = phase_signal_filtered - zero_estimation
    phase_filtered_signal_shifted[~filled_mask] = 0

    theta_estimation = left_estimation - zero_estimation

    phase_filtered_signal_shifted = crop_phase_filtered_signal_shifted(phase_filtered_signal_shifted, theta_estimation)

    filtered_signal_shifted = abs(signal) * np.exp(1.0j * phase_filtered_signal_shifted)

    if show_histogram:
        mask = get_phase_filtered_signal_shifted_mask(phase_filtered_signal_shifted=phase_filtered_signal_shifted,
                                                      theta_estimation=theta_estimation, tissue_mask=filled_mask)
        masked_phase = phase_filtered_signal_shifted[mask]
        plt.hist(masked_phase.flatten(),
                 bins=list(np.arange(masked_phase.min(), masked_phase.max(), 0.01)),
                 range=(masked_phase.min(), masked_phase.max()))
        plt.title('Histogram Filtered Signal Phase After Shift')
        plt.show()

    print('Signal Shifted')

    return filtered_signal_shifted, zero_estimation, theta_estimation


def crop_phase_filtered_signal_shifted(phase_filtered_signal_shifted, theta_estimation):
    phase_filtered_signal_shifted[phase_filtered_signal_shifted >= 0] = 0
    phase_filtered_signal_shifted[phase_filtered_signal_shifted <= theta_estimation] = theta_estimation

    return phase_filtered_signal_shifted
