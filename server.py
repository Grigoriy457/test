from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/")
def hello():
	return "<b>Hello, World!</b>"

@app.route("/post", methods=['POST', 'GET'])
def post_info():
	data = request.json
	print(data)
	if not isinstance(data, dict):
	    return abort(400)

	name = data.get('name')
	age = data.get('age')
	city = data.get('city')

	if (not isinstance(name, str) or len(name) == 0) and (not isinstance(age, str) or len(age) == 0) and (not isinstance(city, str) or len(city) == 0):
	    return abort(400)

	return f"Name: {name}\nAge: {age}\nCity: {city}"

if __name__ == '__main__':
	app.run(threaded=True)