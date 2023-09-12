# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List api routes"""
    return (
        f"Available Routes:<br/>"
        f"//api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("//api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    #query
    results = session.query()
    
    session.close()

    #dicitonary
    all_prcp = []
    for prcp in results:
        prcp_dict = {}
        prcp_dict["Precipitation"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)



if __name__ == "__main__":
    app.run(debu=True)
