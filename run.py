from flask import g, Flask, render_template, request, redirect,jsonify, url_for, flash
import views 

app = Flask(__name__)
app.register_blueprint(views.app_views)

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)