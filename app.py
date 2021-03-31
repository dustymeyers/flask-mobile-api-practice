import flask
import psycopg2
from flask import request, jsonify, make_response
from psycopg2.extras import RealDictCursor

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello World!</h1><p>Let's add some phones with python and flask!</p>"

@app.route('/api/mobile/add', methods=['POST'])
def api_add():
    # print(request.form)
    model = request.form['model']
    price = request.form['price']
    try:
        connection = psycopg2.connect(user="dustymeyers",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgress_db")
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        print(model, price)
        insertQuery = "INSERT INTO mobile (model, price) VALUES (%s, %s)"
        
        # this is like pool.query(insertQuery, [model, price])
        cursor.execute(insertQuery, (model, price))

        connection.commit()
        count = cursor.rowcount
        print(count, "Book inserted")

        result = {'status': 'CREATED'}
        return make_response(jsonify(result), 201)
    except (Exception, psycopg2.Error) as error:
        # there was a problem
        if(connection):
          print("Failed to insert mobile phone", error)

          result={'status': 'ERROR'}
          return make_response(jsonify(result), 500)
    finally:
      if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

app.run()