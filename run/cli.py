import click
from art import text2art
from colorama import Fore
from colorama import init as colorama_init
import numpy as np
import pandas as pd
import pickle

""" CLI app using click and art libraries """

# init colorama
colorama_init(autoreset=True)

# load the pipeline from disk
filename = 'finalized_model.pkl'
model = pickle.load(open(filename, 'rb'))

def prompt_param(message, acceptable_range, default):
    """Function to prompt for parameters

    Args:
        message (str): message to show in prompt
        acceptable_range (tuple(int, int)): acceptable range for input
        default (int): default value to accept as prompt

    Returns:
        float: entered value by user
    """

    while True:
        param = click.prompt(f'Patient\'s {message} | default:', type=int, default=default)
        if param in range(acceptable_range[0], acceptable_range[1]):
            break
        else:
            click.echo(f"Please provide a number between {str(acceptable_range[0])} and {str(acceptable_range[1])}.")
    return float(param)

# init and run click
@click.command()
def makeCLI():
     # Compose and format output text
    artl1 = text2art("Welcome  to...", font='small',)
    artl2 = text2art("make it work", font='c_ascii')
    artl3 = text2art("Project  1", font='small')
    print(f"{Fore.BLUE}{artl1}")
    print(f"{Fore.BLUE}{artl2}")
    print(f"{Fore.BLUE}{artl3}")

    # Ask for user to continue
    click.pause()

    # Clear terminal
    click.clear()

    # Ask to enter parameters
    enter_params = "Enter the following parameters to predict the lifespan:"
    print(f"{Fore.LIGHTRED_EX}{enter_params}")

    # Define allowed ranges for user input
    parameters_prompts = dict()
    entered_parameters = dict()
    parameters_prompts['genetic'] = ["genetic age", (60, 110), 85]
    parameters_prompts['length'] = ["length in cm", (150, 215), 185]
    parameters_prompts['mass'] = ["Weight in kg", (50, 165), 80]
    parameters_prompts['exercise'] = ["Exercise in hr/day", (0, 8), 2]
    parameters_prompts['alcohol'] = ["Alcohol in glasses/day", (0, 10), 0]
    parameters_prompts['smoking'] = ["Smoking in cig./day", (0, 25), 0]
    parameters_prompts['sugar'] = ["Sugar in cubes/day", (0, 15), 4]
    
    # loop over all parameters to prompt to user
    for k, v in parameters_prompts.items():
        entered_parameters[k] = prompt_param(v[0], v[1], v[2])
    
    # Calculate bmi and power transforms
    entered_parameters['bmi'] = entered_parameters['mass'] / (entered_parameters['length']/100)**2
    entered_parameters['mass_square'] = entered_parameters['mass']**2
    entered_parameters['bmi_square'] = entered_parameters['bmi']**2
    entered_parameters['exercise_sqrt'] = np.power(entered_parameters['exercise'], 1/2)

    # remove mass from dict
    entered_parameters.pop('mass')

    # Convert dict to dataframe
    params_df = pd.DataFrame(entered_parameters, index=[0])

    # Reorder columns to match trained model
    params_df = params_df.reindex(columns=['genetic', 'length', 'bmi', 'exercise', 'smoking', 'alcohol', 'sugar', 'mass_square', 'bmi_square', 'exercise_sqrt'])
    
    # make a prediction based on the parameters given by the user
    prediction = model.predict(params_df)
    
    # send the prediction back to the user
    click.echo(f"\nBased on the given parameters, the predicted lifespan is: \033[1m{Fore.GREEN}{round(prediction[0], 1)}\033[1m")

if __name__ == '__main__':
    makeCLI()