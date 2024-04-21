from flask import Flask
# from flask_session import Session

def create_app() -> Flask: 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = b'DKFJSOFJ1342'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

    # app.config.from_file('./config.json', load=json.load)
    # Session(app)
    # app.config['SESSION_TYPE'] = 'memcached' # session info is stored via memcache api
    # app.config['SESSION_PERMANENT'] = True # session are persisent, thus they are not ended when the brwoser closes
    # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60) # sessions lasts for 60 minutes unless renewed or explicitly cancelled.
    # app.config['SESSION_REFRESH_EACH_REQUEST'] = True # session renew feature is enabled
