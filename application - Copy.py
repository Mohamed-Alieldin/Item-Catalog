#!/usr/bin/env python3


from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, Category, CategoryItem, User
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


#Connect to Database and create database session
engine = create_engine('sqlite:///Catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']



#Store it in the session for later validation
@app.route('/login')
@app.route('/login/')
def showLogin():
  login_status = False
  if 'username' in login_session:
    login_status = True

  print("Login Get Request")
  state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))  
  login_session['state'] = state
  print("the state created in the get request %s"%state)
  return render_template('login.html', thestate=state, login_status = login_status)


@app.route('/gconnect', methods = ['POST'])
def gconnect():
  if request.args.get('state') != login_session['state']:
    response = make_response(json.dumps('Invalid State Parameter'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  code = request.data
  try:
    oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)
  except FlowExchangeError:
    response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  
  # check that the access token is valid
  access_token = credentials.access_token
  url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"%access_token
  h = httplib2.Http()
  result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
  #If there was an error in the access token info, abort
  if result.get('error') is not None:
    response = make_response(json.dumps(result.get('error')),500)
    response.headers['Content-Type'] = 'application/json'
  # Verify that the access token is used for the intended user
  google_id = credentials.id_token['sub']
  if result['user_id'] != google_id:
    response = make_response(json.dumps("Token's user ID doesn not match given user ID"),401)
    response.headers['Content-Type'] = 'application/json'
    return response
  # Verify that the access token is valid for this app
  if result['issued_to'] != CLIENT_ID:
    response = make_response(json.dumps("Token's client ID does not match App's."), 401)
    print("Token's client ID does not match App's.")
    response.headers['Content-Type'] = 'application/json'
    return response

  # Check to see if the user is logged in the system
  stored_credentials = login_session.get('credentials')
  stored_google_id = login_session.get('google_id')
  if stored_credentials is not None and google_id == stored_google_id:
    response = make_response(json.dumps('Current user is already connected'), 200)
    response.headers['Content-Type'] = 'application/json'

  # Store the access token in the session for later use (none of the IF statements were true)
  login_session['credentials_token'] = credentials.access_token
  login_session['google_id'] = google_id

  #Get user info
  userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
  params = {'access_token': credentials.access_token, 'alt': 'json'}
  answer = requests.get(userinfo_url, params=params)
  data = answer.json()

  login_session['username'] = data['name']
  login_session['picture'] = data['picture']
  login_session['email'] = data['email']

  # see if user exists, if not make a new one
  current_Userid = GetUserId(login_session['email'])
  if not current_Userid:
    current_Userid = CreateUser(login_session)
  login_session['user_id'] = current_Userid

  output = ''  
  output += '<h1>Welcome, '
  output += login_session['username']
  output += '!</h1>'
  flash("you are now logged in as %s" % login_session['username'])
  print("done!")
  return output


# Disconnect - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
  credentialsToken = login_session.get('credentials_token')
  if credentialsToken is None:
    response = make_response(json.dumps('current user not connected'),401)
    response.headers['Content-Type'] = 'application/json'
    return response
  
  url = "https://accounts.google.com/o/oauth2/revoke?token=%s"%credentialsToken
  h = httplib2.Http()
  result = h.request(url, 'GET')[0]
  print("the result is {}".format(result))
  if result['status'] == '200':
    #reset the user's session
    del login_session['credentials_token']
    del login_session['google_id']
    del login_session['username']
    del login_session['picture']
    del login_session['email']

    response = make_response(json.dumps('Successfully Disconnected'), 200)
    response.headers['Content-Type'] = 'application/json'
    flash("You have logged out.")
    return redirect(url_for('showCategories'))
  else:
    # For whatever reason the given token was invalid
    response = make_response(json.dumps('Falied to revoke token for given user'), 400)
    response.headers['Content-Type'] = 'application/json'
    return response

# APIs EndPoints Area
# One Category Item API EndPoint -- returns a specific item of a specific category
@app.route('/catalog/items/<item_name>/JSON')
def categoryItemJSON(item_name):
  try:
    session = DBSession()
    item = session.query(CategoryItem).filter_by(title = item_name).all()
    return jsonify(Item= [r.serialize for r in item])
  except:
    response = make_response(json.dumps('Category does not exist'), 404)
    response.headers['Content-Type'] = 'application/json'
    return response

# Category Items API EndPoint -- returns the items of a specific category
@app.route('/catalog/<category_name>/items/JSON')
def categoryItemsJSON(category_name):
  try:
    session = DBSession()
    current_category = session.query(Category).filter_by(name = category_name).first()
    category_items = session.query(CategoryItem).filter_by(category_id = current_category.id).all()
    return jsonify(Category_Items= [r.serialize for r in category_items])
  except:
    response = make_response(json.dumps('Category does not exist'), 404)
    response.headers['Content-Type'] = 'application/json'
    return response

# All Items API EndPoint-- returns all items
@app.route('/catalog/items/JSON')
def itemsJSON():
    session = DBSession()
    items = session.query(CategoryItem).all()
    return jsonify(items= [r.serialize for r in items])

# All Categories API EndPoint -- returns all categories
@app.route('/catalog/categories/JSON')
def categoriesJSON():
    session = DBSession()
    categories = session.query(Category).all()
    return jsonify(categories= [r.serialize for r in categories])

# App Pages Area
@app.route('/')
@app.route('/catalog/')
def showCategories():
  login_status = False
  if 'username' in login_session:
    login_status = True
  session = DBSession()
  categories = session.query(Category).order_by(Category.id)
  latestItems = session.query(CategoryItem).order_by(CategoryItem.id.desc()).limit(10).all()
  
  # Making a list to include the category name for each item
  latestItems_list = []
  for i in latestItems:
    item_dict = {}
    item_dict['title'] = i.title
    category_name = session.query(Category).filter_by(id = i.category_id).one().name
    item_dict['category_name'] = category_name
    latestItems_list.append(item_dict)
  
  if login_status == True:
    return render_template('catalog_user.html', categories = categories, items = latestItems_list, login_status = login_status)
  else:
    return render_template('catalog_public.html', categories = categories, items = latestItems_list, login_status =login_status)

@app.route('/catalog/<category_name>/items/')
def showCategoryItems(category_name):
  login_status = False
  if 'username' in login_session:
    login_status = True
  session = DBSession()
  categories = session.query(Category).order_by(Category.id)

  # Getting Category-Id for the current category
  curent_category_id = session.query(Category).filter_by(name =category_name ).one().id
  # Getting the items
  itemscount = session.query(CategoryItem).filter_by(category_id = curent_category_id).count()
  items = session.query(CategoryItem).filter_by(category_id = curent_category_id).order_by(CategoryItem.id)

  return render_template('categoryitems.html', categories = categories, category_name = category_name,
   itemscount = itemscount, items = items, login_status = login_status)

@app.route('/catalog/items/new', methods=['GET','POST'])
def newCategoryItem():  
  if 'username' not in login_session:
    return redirect('/login')
  login_status = True
  if request.method == 'GET':
    session = DBSession()
    categories = session.query(Category).order_by(Category.id)
    return render_template('newItem.html', categories = categories, login_status = login_status)
  
  if request.method == 'POST':
    session = DBSession()
    user_id = login_session['user_id']
    newItem_CategoryId = session.query(Category).filter_by(name = request.form['category']).one().id
    newItem = CategoryItem(title = request.form['title'], description = request.form['description'], category_id = newItem_CategoryId, user_id= user_id)
    session.add(newItem)
    session.commit()
    flash('Item is successfully created.')
    return redirect(url_for('showCategories'))

@app.route('/catalog/<category_name>/<item_name>/')
def showItem(category_name, item_name):
  if 'username' in login_session:
    login_status = True
    session = DBSession()
    current_item = session.query(CategoryItem).filter_by(title = item_name).one()
    creator = GetUserInfo(current_item.user_id)
    if creator == None:
      return render_template('item_public.html', item = current_item, login_status = login_status)
    if creator.id == login_session['user_id']:
      return render_template('item_user.html', item = current_item, login_status = login_status)
    else:
      return render_template('item_public.html', item = current_item, login_status = login_status)
  else:
    login_status = False
    session = DBSession()
    current_item = session.query(CategoryItem).filter_by(title = item_name).one()
    return render_template('item_public.html', item = current_item, login_status = login_status)

@app.route('/catalog/<item_name>/edit/', methods = ['GET', 'POST'])
def editItem(item_name):
  if 'username' not in login_session:
    return redirect('/login')
  login_status = True
  if request.method == 'GET':
    session = DBSession()
    current_CategoryId = session.query(CategoryItem).filter_by(title = item_name).one().category_id
    current_categoryName = session.query(Category).filter_by(id = current_CategoryId).one().name
    current_item = session.query(CategoryItem).filter_by(title = item_name).one()
    categories = categories = session.query(Category).order_by(Category.id)
    return render_template('editItem.html', item = current_item, categories = categories,
     category_name = current_categoryName ,login_status = login_status)

  if request.method == 'POST':
    session = DBSession()
    NewCategory = session.query(Category).filter_by(name = request.form['category']).one()
    item_edit = session.query(CategoryItem).filter_by(title = item_name).one()
    # Editing the item data
    item_edit.title = request.form['title']
    item_edit.description = request.form['description']
    item_edit.category_id = NewCategory.id
    session.commit()
    flash('Item is successfully edited.')
    return redirect(url_for('showCategoryItems', category_name = NewCategory.name ))


@app.route('/catalog/<item_name>/delete/', methods = ['GET', 'POST'])
def deleteItem(item_name):
  if 'username' not in login_session:
    return redirect('/login')
  login_status = True
  if request.method == 'GET':
    session = DBSession()
    current_CategoryId = session.query(CategoryItem).filter_by(title = item_name).one().category_id
    current_categoryName = session.query(Category).filter_by(id = current_CategoryId).one()
    return render_template('deleteItem.html', item_name = item_name, category_name = current_categoryName,login_status = login_status)
  if request.method == 'POST':
    session = DBSession()
    item_delete = session.query(CategoryItem).filter_by(title = item_name).one()
    current_categoryName = session.query(Category).filter_by(id = item_delete.category_id).one().name
    session.delete(item_delete)
    session.commit()
    flash('Item is successfully deleted')
    return redirect(url_for('showCategoryItems', category_name = current_categoryName ))

# Users Functions Area
def GetUserId(email):
  session = DBSession()
  try:
    user = session.query(User).filter_by(email = email).one()
    return user.id
  except:
    return None

def GetUserInfo(user_id):
  session = DBSession()
  try:
    user = session.query(User).filter_by(id = user_id).one()
    return user
  except:
    return None

def CreateUser(login_session):
  newUser = User(name = login_session['username'], email = login_session['email'],
  picture=login_session['picture'])
  session = DBSession()
  session.add(newUser)
  session.commit()
  user = session.query(User).filter_by(email = login_session['email']).one()
  return user.id

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)
