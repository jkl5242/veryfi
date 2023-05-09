from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://airflow:airflow@postgres:5432/airflow'
db = SQLAlchemy(app)

class ParsedTotal(db.Model):
    __tablename__ = 'parsed_total'
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer)
    value = db.Column(db.Numeric)
    score = db.Column(db.Numeric)
    ocr_score = db.Column(db.Numeric)
    bounding_box = db.Column(db.ARRAY(db.Numeric))

@app.route('/api/business/<int:business_id>', methods=['GET'])
def get_business_total(business_id):
    # Query the parsed_total table for the given business_id
    query_result = ParsedTotal.query.filter(ParsedTotal.business_id == business_id, ParsedTotal.value.isnot(None)).all()

    # Calculate the sum of value
    total_sum = sum([row.value for row in query_result])

    # Return the results as a JSON response
    response = {
        'business_id': business_id,
        'total_sum': total_sum
    }
    return jsonify(response)

@app.route('/api/score/<float:score>', methods=['GET'])
def get_score_total(score):
    # Query the parsed_total table for the given score
    query_result = ParsedTotal.query.filter(ParsedTotal.score == score, ParsedTotal.value.isnot(None)).all()

    # Calculate the sum of value
    total_sum = sum([row.value for row in query_result])

    # Return the results as a JSON response
    response = {
        'score': score,
        'total_sum': total_sum
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)