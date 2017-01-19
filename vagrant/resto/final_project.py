from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route("/")
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant)
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		resto = Restaurant(name=request.form['name'])
		session.add(resto)
		session.commit()
		flash("New restaurant created!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			menuItem.name = request.form['name']
		session.add(resto)
		session.commit()
		flash("Restaurant edited!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html', restaurant = resto)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(resto)
		session.commit()
		flash("Restaurant deleted!")
		return redirect(url_for('showRestaurants'))
	return render_template('deleterestaurant.html', restaurant = resto)

@app.route("/restaurant/<int:restaurant_id>/")
@app.route("/restaurant/<int:restaurant_id>/menu/")
def showMenu(restaurant_id):
	resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html', restaurant = resto, items=items)

@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New menu item created!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	menuitem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			menuitem.name = request.form['name']
		if request.form['description']:
			menuitem.description = request.form['description']
		if request.form['price']:
			menuitem.price = request.form['price']
		if request.form['course']:
			menuitem.course = request.form['course']
		session.add(menuitem)
		session.commit()
		flash("Menu item edited!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:		
		return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, menuitem=menuitem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	menuitem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':		
		session.delete(menuitem)
		session.commit()
		flash("Menu item deleted!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:		
		return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menuitem=menuitem)


@app.route('/restaurants/JSON')
def restaurantsJSON():
	restaurants = session.query(Restaurant)
	return jsonify(Restaurants=[i.serialize for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem=menuItem.serialize)





if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)