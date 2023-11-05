from flask import jsonify

app = Flask(__name__)

@app.route('/api/data')

def data(my_data):
    # Python dictionary
    # my_data = {
    #     'name': 'John Doe',
    #     'age': 30
    # }
    # jsonify serializes the dictionary to JSON format
    return jsonify(my_data)

if __name__ == '__main__':
    app.run()