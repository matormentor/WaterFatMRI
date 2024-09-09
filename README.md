# WaterFatMRI 

Novel Water Fat 3D Separation for MRI signals using one Echo developed for Ultra Short Echo Time

### Presented research in ISMRM 2024
![image](https://github.com/user-attachments/assets/53e6c191-4402-4861-8f1c-aa0f16ce0cb7)

## Algorithm 
![image](https://github.com/user-attachments/assets/2a81bd3e-11b0-497e-8e20-d3c2e1a84f53)

## Presentation

May be found in the following [link](defense_thesis.pptx)

## Usage

The **Analysis** folder contains all the *already* processed signal manipulation and visualization 
The **Water Fat Lib** contains all the necessary logic for the method, optimization, image processing and machine learning methos

## Dependencies

There is a small dependency on the **BMRR Python** library which is not included in the package. But can be refactored easily using any type of class/struct and DICOM parser.

## Hypothesis

Initialization of a non-linear second order optimization method used to capture the unwanted phase contributions form the MRI scan helps improve the convergence path while increasing computational space and time efficiency

## Thesis

Found under the [link](Thesis.pdf)




