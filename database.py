import sqlite3  
conn = sqlite3.connect('customerdata.db')  
query_to_create_table = """
CREATE TABLE CustomerDetails (
    age INT,
    flight_distance INT,
    inflight_entertainment INT,
    baggage_handling INT,
    cleanliness INT,
    departure_delay INT,
    arrival_delay INT,
    gender VARCHAR(30),
    customer_type VARCHAR(30),
    travel_type VARCHAR(30),
    class_Type VARCHAR(30),
    Output VARCHAR(30)
);
"""

cur = conn.cursor()  
cur.execute(query_to_create_table) 

print("Your database and table are created!")
cur.close() 
conn.close()
