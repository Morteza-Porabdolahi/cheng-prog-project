from scipy.optimize import fsolve
import numpy as np

def calculateAverageVelocity(volumetricFlowRate, diameter):
    areaOfPipe = np.pi * (diameter / 2) ** 2

    return volumetricFlowRate / areaOfPipe


def calculateReynolds(averageVelocity, diameter, viscosity, density):
    return density * averageVelocity * diameter / viscosity


def defineFlowRegime(reynoldsNum):
    if reynoldsNum < 2000:
        return "Laminar"
    elif reynoldsNum > 4000:
        return "Turbulent"
    else:
        return "Transition"

def calculateFrictionFactor(reynoldsNum, roughness, diameter, flowRegime):
    frictionInLaminar = 64 / reynoldsNum
    # 0.02 is an initial guess
    frictionInTurbulent = fsolve(
        calculateFrictionInTurbulent(roughness, reynoldsNum, diameter), 0.02
    )

    if flowRegime == "Laminar":
        return frictionInLaminar
    elif flowRegime == "Turbulent":
        return frictionInTurbulent[0]
    else:
        return (frictionInTurbulent[0] + frictionInLaminar) / 2


def calculateFrictionInTurbulent(roughness, reynoldsNum, diameter):
    return lambda friction: (1 / np.sqrt(friction)) + 2 * np.log10(
        ((roughness / diameter) / 3.7) + (2.51 / (reynoldsNum * np.sqrt(friction)))
    )


def calculatePressureDrop(friction, length, diameter, density, averageVelocity):
    return friction * (length / diameter) * ((density * averageVelocity**2) / 2)


def returnValidatedUserInput(message):
    while True:
        try:
            userInput = float(input(message))
        except ValueError:
            print("\033[31mPlease enter a valid input!\033[0m")
        else:
            break

    return userInput

def getInputsFromUser():
    density = returnValidatedUserInput("Density (kg/m^3): ")
    viscosity = returnValidatedUserInput("Viscosity (Pa.S): ")
    volumetricFlowRate = returnValidatedUserInput("Volumetric Flow Rate (m^3 / s): ")

    diameter = returnValidatedUserInput("Diameter (m): ")
    length = returnValidatedUserInput("Length of the pipe (m): ")
    roughness = returnValidatedUserInput("Roughness of the pipe (m): ")

    userInputs = [density, viscosity, volumetricFlowRate, diameter, length, roughness]

    return userInputs

def main():
    density, viscosity, volumetricFlowRate, diameter, length, roughness = getInputsFromUser();

    averageVelocity = calculateAverageVelocity(volumetricFlowRate, diameter)
    reynoldsNum = calculateReynolds(averageVelocity, diameter, viscosity, density)
    flowRegime = defineFlowRegime(reynoldsNum)
    friction = calculateFrictionFactor(reynoldsNum, roughness, diameter, flowRegime)
    pressureDrop = calculatePressureDrop(
        friction, length, diameter, density, averageVelocity
    )

    uptoFourDecimalsFormatter = "%.4f"

    print(
        f"The flow regime in the pipe is {flowRegime} based on calculated Reynolds number ({uptoFourDecimalsFormatter%reynoldsNum}) and also based on friction factor ({uptoFourDecimalsFormatter%friction}), the pressure drop is roughly {uptoFourDecimalsFormatter%(pressureDrop / 1000)}kPa."
    )


if __name__ == "__main__":
    main()
