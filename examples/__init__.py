from flask import Flask, jsonify, request
from src.example_files.products import products
import os
from src.example_files.auth import auth
from src.example_files.bookmarks import bookmarks
from src.example_files.request import request
from src.config.connection import database

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)

	if test_config is None:
		app.config.from_mapping(
			SECRET_KEY = os.environ.get("SECRET_KEY")
		)
	else:
		app.config.from_mapping(test_config)

	# Rutas
	@app.route('/ping', methods=['GET'])
	def ping():
		return jsonify({"message": "pong"})

	#comentado
	@app.route('/products', methods=['GET'])
	def get_products():
		return jsonify(products)

	#comentado
	@app.route('/products/:product_name')
	def product():
		return jsonify(products)

	#comentado
	@app.route('/leproduit/<string:product_name>')
	def get_product(product_name):
		product_found = [product for product in products if product['name'] == product_name]
		if len(product_found) > 0:
			return jsonify({"product": product_found[0]})
		return jsonify({"message": "Product not found!"})

	#comentado
	@app.route('/products', methods=['POST'])
	def add_product():
		new_product = {
			"name": request.json['name'],
			"price": request.json['price'],
			"quantity": request.json['quantity']
		}
		products.append(new_product)
		# print(request.json)
		return jsonify({"message": "Product Added Successfully", "products": products})

	#comentado
	@app.route('/products/<string:product_name>', methods=['PUT'])
	def edit_product(product_name):
		product_found = [product for product in products if product['name'] == product_name]
		if len(product_found) > 0:
			product_found[0]['name'] = request.json['name']
			product_found[0]['price'] = request.json['price']
			product_found[0]['quantity'] = request.json['quantity']
			return jsonify({
			"message": "Product Updated",
			"product": product_found[0]
			})
		return jsonify({"message": "Product not found"})

	#comentado
	@app.route('/products/<string:product_name>', methods=['DELETE'])
	def delete_product(product_name):
		product_found = [product for product in products if product['name'] == product_name]
		if len(product_found) > 0:
			products.remove(product_found[0])
			return jsonify({
			"message": "Product deleted",
			"products": products
			})
		return jsonify({})

	@app.get('/hello')
	def index():
		return jsonify({"messages": "hello world"})

	app.register_blueprint(auth)
	app.register_blueprint(bookmarks)
	app.register_blueprint(request)
	app.register_blueprint(database)
  
	return app