import pickle
from sklearn.preprocessing import RobustScaler
import numpy as np
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import psycopg2
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('./BestModel/Final_ModelForPrediction.pkl', 'rb'))
scalar = pickle.load(open('./DataScaling/Scalar1.pkl', 'rb'))

db = psycopg2.connect(host="ec2-54-161-189-150.compute-1.amazonaws.com",user="ihtpstqfswcmcv",password="9c57a4152569a2ccf2ace10d245bd70218055d86b1aadb4b57117b6f05d70108",database="d9c8v7pln18dgt")
cur = db.cursor()

@cross_origin()
@app.route('/', methods=['GET'])
def homepage():
    return render_template('page1.html')


@cross_origin()
@app.route('/form', methods=['GET'])
def form():
    return render_template('form.html')


@cross_origin()
@app.route('/contact', methods=['GET'])
def developer():
    return render_template('Developer.html')


@cross_origin()
@app.route('/predict', methods=['POST', 'GET'])
def predict():

    if request.method == 'POST':
        age = int(request.form['Age'])
        gender = (request.form["gender"])
        bmi = float(request.form['bmi'])
        children = int(request.form["children"])
        smoker = (request.form['smoker'])
        region = (request.form["region"])
        print(age,gender,bmi,children,smoker,region)

        cur.execute("create table if not exists insurance1(age int, gender varchar(10),bmi NUMERIC(5,3), children int, smoker varchar(5), region varchar(15))")
        cur.execute(f"insert into insurance1 values{(age,gender,bmi,children,smoker,region)}")
        db.commit()

        if gender == 'female':
            gender = 0
        else:
            gender = 1

        if smoker == 'yes':
            smoker = 1
        else:
            smoker = 0

        if region == 'northeast':
            region = 0, 0, 0
        elif region == 'northwest':
            region = 1, 0, 0
        elif region == 'southeast':
            region = 0, 1, 0
        else:
            region = 0, 0, 1

        d = [np.array((age, bmi,  children,gender, smoker, *region))]
        d = pd.DataFrame(d)
        print(d)
        print(type(d))
        scaled_data = scalar.transform(d)
        print(scaled_data)
        prediction = model.predict(d)
        predict1 = prediction
        print(predict1)

        return render_template('output.html', result=f"{predict1}")

    else:
        return render_template('page1.html')


if __name__ == "__main__":
    app.run(debug=True)

