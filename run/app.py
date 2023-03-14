from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from forms import getLifespanForm
import pickle
import numpy as np
import pandas as pd
from icecream import ic

app = Flask(__name__)
# Secret key for use with CSRF token
# TODO: put key in environment variable
app.config['SECRET_KEY'] = 'ebc72148568923ee1fdd713b4a247f4c97548a11a409fbfc'

# load the model from disk
filename = 'finalized_model.pkl'
model = pickle.load(open(filename, 'rb'))


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
        session['new_params'] = session.get('params')
        return redirect(url_for('predict'))
    return render_template('index.html', form=form)

@app.route('/predict')
def predict():
    params = session.get('new_params')
    params_copied = params.copy()
    params_copied['bmi'] = params_copied['mass'] / (params_copied['length']/100)**2
    params['bmi'] = params_copied['bmi']
    params_copied['mass_square'] = params_copied['mass']**2
    params_copied['bmi_square'] = params_copied['bmi']**2
    params_copied['exercise_sqrt'] = np.power(params_copied['exercise'], 1/2)
    params_copied.pop('mass')
    ic(params_copied)
    params_df = pd.DataFrame(params_copied, index=[0])
    params_df = params_df.reindex(columns=['genetic', 'length', 'bmi', 'exercise', 'smoking', 'alcohol', 'sugar', 'mass_square', 'bmi_square', 'exercise_sqrt'])
    print(params_df)
 
   
    prediction = model.predict(params_df)
    ic(prediction)
    return render_template('predict.html', params=params, prediction=prediction)

@app.route('/ajax_prediction', methods = ['POST'])
def ajax_request():
    session_params = session.get('new_params')
    ic(session_params)
    ajax_param_name = request.form['parameter_name']
    ajax_param_value = request.form['parameter_value']
    # update parameter and make new prediction
    params_copied = session_params.copy()
    params_copied[ajax_param_name] = float(ajax_param_value)
    session_params[ajax_param_name] = float(ajax_param_value)
    session['new_params'] = session_params
    params_copied['bmi'] = params_copied['mass'] / (params_copied['length']/100)**2
    session_params['bmi'] = params_copied['bmi']
    params_copied['mass_square'] = params_copied['mass']**2
    session_params['mass_square'] = params_copied['mass_square']
    params_copied['bmi_square'] = params_copied['bmi']**2
    session_params['bmi square'] = params_copied['bmi_square']
    params_copied['exercise_sqrt'] = np.power(params_copied['exercise'], 1/2)
    params_copied.pop('mass')
    ic(params_copied)
    ic(session_params)
    params_df = pd.DataFrame(params_copied, index=[0])
    params_df = params_df.reindex(columns=['genetic', 'length', 'bmi', 'exercise', 'smoking', 'alcohol', 'sugar', 'mass_square', 'bmi_square', 'exercise_sqrt'])
    print(params_df)
    prediction = model.predict(params_df)
    return jsonify(prediction=round(prediction[0], 1))

if __name__ == "__main__":
    app.run()