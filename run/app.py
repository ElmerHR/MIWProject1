from flask import Flask, render_template, redirect, url_for, session
from forms import getLifespanForm
import pickle
import numpy as np
import pandas as pd
from icecream import ic

app = Flask(__name__)
# Secret key for use with CSRF token
# TODO: put key in environment variable
app.config['SECRET_KEY'] = 'ebc72148568923ee1fdd713b4a247f4c97548a11a409fbfc'

# load the pipeline from disk
filename = 'finalized_model.sav'
pipe = pickle.load(open(filename, 'rb'))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = getLifespanForm()
    if form.validate_on_submit():
        ic()
        session['params'] = {
                                'genetic': float(form.genetic.data),
                                'length': float(form.length.data),
                                'mass': float(form.mass.data),
                                'exercise': float(form.exercise.data),
                                'smoking': float(form.smoking.data),
                                'alcohol': float(form.alcohol.data),
                                'sugar': float(form.sugar.data)
                                }
        return redirect(url_for('predict'))
    return render_template('index.html', form=form)

@app.route('/predict')
def predict():
    params = session.get('params')
    params['bmi'] = params['mass'] / (params['length']/100)**2
    params['mass_square'] = params['mass']**2
    params['bmi_square'] = params['bmi']**2
    params['exercise_sqrt'] = np.power(params['exercise'], 1/2)
    params.pop('mass')
    ic(params)
    params_df = pd.DataFrame(params, index=[0])
    params_df = params_df.reindex(columns=['genetic', 'length', 'bmi', 'exercise', 'smoking', 'alcohol', 'sugar', 'mass_square', 'bmi_square', 'exercise_sqrt'])
    print(params_df)
 
   
    prediction = pipe.predict(params_df)
    ic(prediction)
    return render_template('predict.html')

if __name__ == "__main__":
    app.run()