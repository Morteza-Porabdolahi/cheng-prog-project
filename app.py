from scipy.optimize import fsolve
import numpy as np

pipesWithRoughness = {
    "Commercial Steel": 0.000045,
    "Stainless Steel": 0.000015,
    "Copper (New)": 0.0000015,
    "PVC (Polyvinyl Chloride)": 0.0000015,
    "Cast Iron (New)": 0.00026,
    "Ductile Iron (Cement Lined)": 0.00012,
    "Galvanized Iron": 0.00015,
    "Glass (Smooth)": 0.000001,
    "Asbestos Cement": 0.00006,
    "Plastic (Polyethylene, etc.)": 0.0000015
}

listOfPipes = list(pipesWithRoughness)
numericalListOfPipes = listOfPipes.copy()

for i in range(0, len(listOfPipes)):
    numericalListOfPipes[i] = f"{i + 1}.{numericalListOfPipes[i]}"
    

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
    if flowRegime == "Laminar":
        return 64 / reynoldsNum
    elif flowRegime == "Turbulent":
        # 0.02 is an initial guess
        return fsolve(
            calculateFrictionInTurbulent(roughness, reynoldsNum, diameter), 0.02
        )[0]
    else:
        frictionInLaminar = 64 / reynoldsNum
        # 0.02 is an initial guess
        frictionInTurbulent = fsolve(
            calculateFrictionInTurbulent(roughness, reynoldsNum, diameter), 0.02
        )[0]

        return (frictionInTurbulent + frictionInLaminar) / 2


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


def returnValidatedPipeSelection(message):
    while True:
        try:
            userInput = input(message)

            # If it's an empty string, proceed to the next input
            if not userInput.strip():
                return None

            userInput = int(userInput)
            
            if userInput < 1 or userInput > len(listOfPipes):
                raise IndexError()
        except ValueError:
            print("\033[31mPlease enter a valid number or leave it empty for entering a custom roughness!\033[0m")
        except IndexError:
            print(f"\033[31mPlease enter a value between 1 and {len(listOfPipes)}\033[0m")
        else:
            break

    return userInput
    

def getInputsFromUser():
    density = returnValidatedUserInput("Density (kg/m^3): ")
    viscosity = returnValidatedUserInput("Viscosity (Pa.S): ")
    volumetricFlowRate = returnValidatedUserInput("Volumetric Flow Rate (m^3 / s): ")

    diameter = returnValidatedUserInput("Diameter (m): ")
    length = returnValidatedUserInput("Length of the pipe (m): ")
    selectedPipe = returnValidatedPipeSelection(f'Please select one of the pipes below or skip to provide a custom roughness (pipes are considered as new ones) \n {" | ".join(numericalListOfPipes)}: ')
    roughness = None

    if type(selectedPipe) == type(None):
        roughness = returnValidatedUserInput("Roughness of the pipe (m): ")
    elif isinstance(selectedPipe, int):
        roughness = pipesWithRoughness[listOfPipes[selectedPipe - 1]]

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
