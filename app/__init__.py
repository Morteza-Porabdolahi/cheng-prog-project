from scipy.optimize import fsolve
import numpy as np

def calculateAverageVelocity(volumetricFlowRate, diameter):
    areaOfPipe = np.pi * (diameter / 2) ** 2
    
    return volumetricFlowRate / areaOfPipe

def calculateReynolds(averageVelocity ,diameter, viscosity, density):
    return density * averageVelocity * diameter / viscosity

def defineFlowRegime(reynoldsNum): 
    if reynoldsNum < 2000:
        return 'Laminar'
    elif reynoldsNum > 4000:
        return 'Turbulent'
    else:
        return 'Transition'

def calculateFrictionFactor(reynoldsNum, roughness, flowRegime, diameter):    
    frictionInLaminar = 64 / reynoldsNum
    # 0.02 is an initial guess
    frictionInTurbulent = fsolve(calculateFrictionInTurbulent(roughness, reynoldsNum, diameter), 0.02)

    if flowRegime == 'Laminar':
        return frictionInLaminar
    elif flowRegime == 'Turbulent':
        return frictionInTurbulent
    else:
        return (frictionInTurbulent + frictionInLaminar) / 2

def calculateFrictionInTurbulent(roughness, reynoldsNum, diameter):
    return lambda friction: (1 / np.sqrt(friction)) + 2 * np.log10(((roughness / diameter) / 3.7) + (2.51 / (reynoldsNum * np.sqrt(friction))))
    
def calculatePressureDrop(friction, length, diameter, density, averageVelocity):
    return friction * (length / diameter) * ((density * averageVelocity ** 2) / 2)

def returnValidatedUserInput(msg):
    while True:
        try:
            userInput = float(input(msg))
        except ValueError: 
            print('Please enter a valid input!')
        else:
            break;
        
    return userInput
       
def main():
    # [kg/m^3]
    density = returnValidatedUserInput('Density (kg/m^3): ')
    # [Pa.s]
    viscosity = returnValidatedUserInput('Viscosity (Pa.S): ') 

    # [m]
    diameter = returnValidatedUserInput('Diameter (m): ')
    # [m]
    length = returnValidatedUserInput('Length of the pipe (m): ')
    # [m]
    roughness = returnValidatedUserInput('Roughness of the pipe (m): ')

    # [m^3 / s]
    volumetricFlowRate = returnValidatedUserInput('Volumetric Flow Rate (m^3 / s): ')

    averageVelocity = calculateAverageVelocity(volumetricFlowRate, diameter)

    reynoldsNum = calculateReynolds(averageVelocity, diameter, viscosity, density)
    flowRegime = defineFlowRegime(reynoldsNum)
    friction, = calculateFrictionFactor(reynoldsNum, roughness, flowRegime, diameter)
    pressureDrop = calculatePressureDrop(friction, length, diameter, density, averageVelocity)

    uptoFourDecimalsFormatter = "%.4f"

    print(f'The flow regime in the pipe is {flowRegime} based on calculated Reynolds number ({uptoFourDecimalsFormatter%reynoldsNum}) and also based on friction factor ({uptoFourDecimalsFormatter%friction}), the pressure drop is roughly {uptoFourDecimalsFormatter%(pressureDrop / 1000)}kPa.')

if __name__ == '__main__':
    main()
