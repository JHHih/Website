
from flask import Flask

def create_app():
    app = Flask(__name__,
        static_folder='static',
        template_folder='templates')
    
    app.config['SECRET_KEY'] = 'dev_secret_key'
    
    from .views import views
    app.register_blueprint(views)
    
    return app
