from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/")
def hello():
	return "<b>Hello, World!</b>"

@app.route("/post", methods=['GET'])
def post_info():
	data = request.args
	if not isinstance(data, dict):
	    return abort(400)

	name = data.get('name')
	age = data.get('age')
	city = data.get('city')

	if (not isinstance(name, str) or len(name) == 0) and (not isinstance(age, str) or len(age) == 0) and (not isinstance(city, str) or len(city) == 0):
	    return abort(400)

	return f"<p>Name: {name}</p><p>Age: {age}</p><p>City: {city}</p>"

if __name__ == '__main__':
	app.run(threaded=True)
