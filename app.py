# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask,jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")

#static routes
@app.route('/api/v1.0/precipitation')
def precepitation():
 # Create our session (link) from Python to the DB
    session = Session(engine)

    most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_date = most_recent_date[0]
    last_year = dt.datetime(2017,8,23) - dt.timedelta(days=365)
    last_year_data_and_precipitation = session.query(measurement.date, func.sum(measurement.prcp)).group_by(measurement.date).\
    filter(measurement.date> last_year).all()
    session.close()

     prcp = []
    for date, prcp in last_year_data_and_precipitation:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp.append(prcp_dict)
     return jsonify(prcp)
     
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    stations = session.query(station.station).all()
    session.close()

# Convert list of tuples into normal list
    station = list(np.ravel(stations))

     return jsonify(station)
     
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    join = session.query(measurement, station).filter(measurement.station == station.station)
    most_recent_date = session.query(join.date).order_by(join.date.desc()).first()
    last_date = most_recent_date[0]
    last_year = dt.datetime(2017,8,23) - dt.timedelta(days=365)
    last_year_date_and_temp = session.query(join.date, func.sum(join.tobs)).group_by(join.date).\
    filter(join.date> last_year).filter(join.station=='USC00519281').all()
    session.close()

     temp = []
    for date, temp in last_year_date_and_temp:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temp"] = tobs
        temp.append(temp_dict)
     return jsonify(temp)
     
#dynamic routes
@app.route('/api/v1.0/<start>')
def <start>

        session=Session(engine)
        TMIN = session.query(func.min(measurement.tobs)).filter(measurement.date >= start).all
        TAVG = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).all
        TMAX = session.query(func.max(measurement.tobs)).filter(measurement.date >= start).all
        session.close()

        temp_summary_stats = {}
        temp_summary_stats["TMIN"] = TMIN
        temp_summary_stats["TAVG"] = TAVG
        temp_summary_stats["TMAX"] = TMAX

        return jsonify(temp_summary_stats)

@app.route('/api/v1.0/<start>/<end>')
def <start>/<end>

        session=Session(engine)
        TMIN = session.query(func.min(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <=end).all
        TAVG = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <=end).all
        TMAX = session.query(func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <=end).all
        session.close()

        temp_summary_stats = {}
        temp_summary_stats["TMIN"] = TMIN
        temp_summary_stats["TAVG"] = TAVG
        temp_summary_stats["TMAX"] = TMAX

        return jsonify(temp_summary_stats)

if __name__ == '__main__':
    app.run(debug=True)