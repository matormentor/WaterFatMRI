import torch
import numpy as np
from typing import Tuple


def create_grid_tensors(signal: np.ndarray, return_device=True) -> Tuple:
    x = np.array(range(signal.shape[0]))
    y = np.array(range(signal.shape[1]))
    z = np.array(range(signal.shape[2]))
    data = np.meshgrid(x, y, z, indexing='ij')
    x_mesh, y_mesh, z_mesh = data

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    x_tensor, y_tensor, z_tensor = (torch.as_tensor(x_mesh, device=device).requires_grad_(False),
                                    torch.as_tensor(y_mesh, device=device).requires_grad_(False),
                                    torch.as_tensor(z_mesh, device=device).requires_grad_(False))

    print(f'Set x_tensor, y_tensor and z_tensor in device {device}')
    if return_device:
        return x_tensor, y_tensor, z_tensor, device
    return x_tensor, y_tensor, z_tensor


def polynom_4_func(x, y, z, parameters) -> np.ndarray:
    a = parameters
    x = x/x.shape[0]
    y = y/y.shape[1]
    z = z/z.shape[2]

    result = (a[0]*x**3+a[1]*x**2*y+a[2]*x**2*z+a[3]*x**2+a[4]*x*y**2+a[5]*x*y*z+a[6]*x*y+a[7]*x*z**2+a[8]*x*z+a[9]*x + a[10]*y**3+a[11]*y**2*z+a[12]*y**2 +
              a[13]*y*z**2+a[14]*y*z+a[15]*y+a[16]*z**3+a[17]*z**2+a[18]*z + a[19]*x**3*y+a[20]*x**2*y**2+a[21]*x*y**3+a[22]*y**4+a[23])

    return result


def classic_4_polynom(x, y, z, parameters) -> np.ndarray:

    a = parameters
    x = x/x.shape[0]
    y = y/y.shape[1]
    z = z/z.shape[2]

    result = (a[0]*x**4 + a[1]*y**4 + a[2]*z**4 + a[3]*(x**3)*y + a[4]*(x**3)*z + a[5]*(x**2)*(y**2) + a[6]*(x**2)*(z**2) + a[7]*(x**2)*y*z + a[8]*x*(y**3) +
              a[9]*x*(z**3) + a[10]*x*(y**2)*z + a[11]*x*y*(z**2) + a[12]*(y**2)*(z**2) + a[13])

    return result


def poly_1st_3d(x, y, z, parameters) -> np.ndarray:

    a = parameters
    x = x/x.shape[0]
    y = y/y.shape[1]
    z = z/z.shape[2]

    poly1 = a[0] + a[1]*x + a[2]*y + a[3]*z

    return poly1


def poly_2nd_3d(x, y, z, parameters) -> np.ndarray:

    a = parameters
    x = x/x.shape[0]
    y = y/y.shape[1]
    z = z/z.shape[2]

    poly2 = a[0]*x**2 + a[1]*x*y + a[2]*x*y + a[3]*y*z + a[4]*y**2 + a[5]*z**2

    return poly2


def poly_3rd_3d(x, y, z, parameters) -> np.ndarray:

    a = parameters
    x = x/x.shape[0]
    y = y/y.shape[1]
    z = z/z.shape[2]

    poly3 = (a[0]*x**3 + a[1]*(x**2)*y + a[2]*(x**2)*z + a[3]*x*y**2 + a[4]*x*z**2 + a[5]*x*y*z + a[6]*(y**2)*z + a[7]*(z**2)*y + a[8]*y**3 + a[9]*z**3)

    return poly3


def poly_4th_3d(x, y, z, parameters) -> np.ndarray:

    a = parameters
    x = x/x.shape[0]
    y = y/y.shape[1]
    z = z/z.shape[2]
    poly4 = (a[0]*x**4 + a[1]*(x**3)*y + a[2]*(x**3)*z + a[3]*(x**2)*(y**2) + a[4]*(x**2)*y*z + a[5]*(x**2)*(z**2) + a[6]*x*(y**3) + a[7]*x*(z**3) +
             a[8]*x*(y**2)*z + a[9]*x*y*z**2 + a[10]*y**4 + a[11]*(y**3)*z + a[12]*(y**2)*(z**2) + a[13]*y*z**3 + a[14]*z**4)

    return poly4


def poly_to4th_3d(x, y, z, parameters) -> np.ndarray:

    a = parameters

    poly1 = poly_1st_3d(x, y, z, a[0:4])
    poly2 = poly_2nd_3d(x, y, z, a[4:10])
    poly3 = poly_3rd_3d(x, y, z, a[10:20])
    poly4 = poly_4th_3d(x, y, z, a[20:35])

    poly_out = poly1 + poly2 + poly3 + poly4

    return poly_out


def poly_to2nd_3d(x, y, z, parameters) -> np.ndarray:

    a = parameters

    poly1 = poly_1st_3d(x, y, z, a[0:4])
    poly2 = poly_2nd_3d(x, y, z, a[4:10])

    poly_out = poly1 + poly2

    return poly_out
