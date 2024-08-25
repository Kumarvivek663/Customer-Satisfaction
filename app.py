from flask import Flask, render_template,url_for,request
import joblib
import sqlite3

model = joblib.load('models/logisticregre.lb')
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route("/prediction", methods=['GET', 'POST'])
def prediction():
    if request.method == "POST":
        age = int(request.form['age'])
        flight_distance = int(request.form['flight_distance'])
        inflight_entertainment = int(request.form["inflight_entertainment"])
        baggage_handling = int(request.form["baggage_handling"])
        cleanliness = int(request.form["cleanliness"])
        departure_delay = int(request.form["departure_delay"])
        arrival_delay = int(request.form["arrival_delay"])
        gender = request.form["gender"]
        customer_type = request.form["customer_type"]
        travel_type = request.form["travel_type"]
        class_Type = request.form["class_type"]

        Class_Eco = 0
        Class_Eco_Plus = 0
        if class_Type == 'ECO':
            Class_Eco = 1 
        elif class_Type == 'ECO_PLUS':
            Class_Eco_Plus = 1
        
        UNSEEN_DATA = [[age, flight_distance, inflight_entertainment, baggage_handling,
                        cleanliness, departure_delay, arrival_delay, int(gender),
                        int(customer_type), int(travel_type), Class_Eco, Class_Eco_Plus]]

        prediction = model.predict(UNSEEN_DATA)[0]
        print(prediction)
        labels = {'1': "SATISFIED", '0': "DISSATISFIED"}

        query_to_insert = """
        INSERT INTO CustomerDetails (age, flight_distance, inflight_entertainment, baggage_handling, cleanliness, 
        departure_delay, arrival_delay, gender, customer_type, travel_type, class_Type, Output) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        conn = sqlite3.connect('customerdata.db')
        cur = conn.cursor()

        data = (age, flight_distance, inflight_entertainment, baggage_handling, cleanliness,
                departure_delay, arrival_delay, gender, customer_type, travel_type, class_Type, labels[str(prediction)])


        cur.execute(query_to_insert, data)
        conn.commit()
        print("Your record has been stored in the database")
        
        cur.close()
        conn.close()

        return render_template('output.html', output=labels[str(prediction)])

if __name__ == "__main__":
    app.run(debug=True)
