from flask import Flask
from flask import request
from flask import render_template


def get_form():
	price_from = request.form['price_from']
	price_to = request.form['price_to']
	square_from = request.form['square_from']
	square_to = request.form['square_to']
	floor_from = request.form['floor_from']
	floor_to = request.form['floor_to']
	year_from = request.form['year_from']
	year_to = request.form['year_to']
	room_num = request.form.getlist('room_num[]')
	house_type = request.form.getlist('house_type[]')
	region = request.form.get('region')
	from_owner = request.form.get('from_owner')
	from_agency = request.form.get('from_agency')
	photo = request.form.get('photo')
	get_form_dict = {'price_from':price_from, 'price_to':price_to, 'square_from':square_from,
	'square_to':square_to, 'floor_from':floor_from, 'floor_to':floor_to,
	'year_from':year_from, 'year_to':year_to, 'room_num':room_num,
	'house_type':house_type, 'region':region, 'from_owner':from_owner,
	'from_agency':from_agency, 'photo':photo}
	return get_form_dict

	# price_from, price_to, square_from, square_to, floor_from, 
	# floor_to, year_from, year_to, room_num, house_type, region, from_owner,
	# from_agency, photo