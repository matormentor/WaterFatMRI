from typing import Callable
from torchmin import minimize
import scipy.optimize as optimize
from water_fat_lib.app.fit.fit_functions import *


def fit(function: Callable, nparams: int, phase: np.ndarray, weights=None, fit_mask=None) -> dict:
    """
    Fits a given function to the given phase using the L-BFGS method.

    Parameters:
    - function (Callable): The function to fit to the data.
    - nparams (int): The number of parameters expected by the function.
    - phase (np.array): Unwrapped phase.
    - weights (np.array): Weights associated with the input data points.
    - fit_mask (np.array): Boolean array indicating which data points to use in the fitting process.

    Returns:
    - fitted_phase (np.array): The resulting fit.

    Hyperparameters set:
    - learning_rate: 1.0
    - gtol: 1e-8, Tolerance on gradients
    - xtol: 1e-12, Tolerance on function/parameter changes
    - max_iter: 1000
    """
    # Set the tensors
    x_tensor, y_tensor, z_tensor, device = create_grid_tensors(phase)

    weights = torch.ones_like(torch.from_numpy(phase)) if weights is None else weights
    fit_mask = torch.ones_like(torch.from_numpy(phase)).to(torch.bool) if fit_mask is None else fit_mask

    # define the error
    def torch_error(parameters_poly):
        y_ground = torch.as_tensor(phase)
        y_predict = function(x_tensor, y_tensor, z_tensor, parameters_poly)
        error = (y_ground[fit_mask] - y_predict[fit_mask].cpu()) * weights[fit_mask]
        l1_error = torch.mean(error ** 2) / 2
        return l1_error

    print(f'Fitting function {function.__name__}...')
    # Fit
    torch.cuda.empty_cache()
    parameters = torch.randn(nparams).to(device).requires_grad_(False)
    try:
        result_polyfit = minimize(torch_error, parameters, method='l-bfgs', options={'disp': True,
                                                                                     'lr': 1.0,
                                                                                     'gtol': 1e-8,
                                                                                     'xtol': 1e-12,
                                                                                     'max_iter': 1000})
    except Exception as e:
        print(e)
        print("##############\nContinuing Fitting without GPU\n###############")
        torch.cuda.empty_cache()
        try:
            result_polyfit = optimize.minimize(torch_error, parameters.cpu().numpy(), method='L-BFGS-B')
        except Exception as e:
            print(e)
            print('Setting Tensors in cpu')

            x_tensor, y_tensor, z_tensor = x_tensor.to('cpu'), y_tensor.to('cpu'), z_tensor.to('cpu')
            print('Fitting...')
            result_polyfit = minimize(torch_error, parameters.cpu(), method='l-bfgs', options={'disp': True,
                                                                                               'lr': 1.0,
                                                                                               'gtol': 1e-8,
                                                                                               'xtol': 1e-12,
                                                                                               'max_iter': 1000})
    print('Finished fitting')

    # Get Filtered Signal
    params = result_polyfit.x
    print(f"Resulting Params: {params}")
    fitted_phase = function(x_tensor, y_tensor, z_tensor, params).cpu()

    return {"fitted_phase": fitted_phase, 'coefficients': params}
