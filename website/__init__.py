# __init__.py

import os # <-- 1. Thêm import này
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

# 2. Lấy thông tin kết nối từ biến môi trường
DB_USERNAME = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_ENDPOINT = os.environ.get("DB_ENDPOINT") # Đây sẽ là tên service "db" trong Docker
DB_NAME = os.environ.get("DB_NAME")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    
    # 3. Tạo chuỗi kết nối MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}'
    
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all() # Lệnh này sẽ tự tạo các bảng trong MySQL

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# 4. Xóa hàm create_database() cũ đi vì nó không còn cần thiết