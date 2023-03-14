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

    genetic = click.prompt('Patient\'s genetic age | default:', type=int, default=85)
    length = click.prompt('Patient\'s length in cm | default:', type=float, default=185)
    mass = click.prompt('Patient\'s weight in kg | default:', type=float, default=80)
    exercise = click.prompt('Patient\'s exercise in hr/day | default:', type=float, default=2)
    alcohol = click.prompt('Patient\'s alcohol in glasses/day | default:', type=float, default=0)
    smoking = click.prompt('Patient\'s smoking in sigarettes/day| default:', type=float, default=0)
    sugar = click.prompt('Patient\'s sugar in cubes/day | default:', type=float, default=4)
    
    # save params to dict
    params = {
                'genetic': float(genetic),
                'length': float(length),
                'mass': float(mass),
                'exercise': float(exercise),
                'smoking': float(smoking),
                'alcohol': float(alcohol),
                'sugar': float(sugar)
            }
    
    # Calculate bmi and power transforms
    params['bmi'] = params['mass'] / (params['length']/100)**2
    params['mass_square'] = params['mass']**2
    params['bmi_square'] = params['bmi']**2
    params['exercise_sqrt'] = np.power(params['exercise'], 1/2)

    # remove mass from dict
    params.pop('mass')

    # Convert dict to dataframe
    params_df = pd.DataFrame(params, index=[0])

    # Reorder columns to match trained model
    params_df = params_df.reindex(columns=['genetic', 'length', 'bmi', 'exercise', 'smoking', 'alcohol', 'sugar', 'mass_square', 'bmi_square', 'exercise_sqrt'])
    
    # make a prediction based on the parameters given by the user
    prediction = model.predict(params_df)
    
    # send the prediction back to the user
    click.echo(f"\nBased on the given parameters, the predicted lifespan is: \033[1m{Fore.GREEN}{round(prediction[0], 1)}\033[1m")

if __name__ == '__main__':
    makeCLI()