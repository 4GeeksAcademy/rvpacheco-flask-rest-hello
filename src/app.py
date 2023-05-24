import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config["JWT_SECRET_KEY"] = os.getenv("FLASK_APP_KEY")
jwt = JWTManager(app)

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def users_get():
    users = User.query.all()
    users = [user.serialize() for user in users]
    return jsonify(users)


@app.route('/users/favorites', methods=['GET'])
def user_favorites_get():
    user_id = request.headers.get('user_id')
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    favorites = [favorite.serialize() for favorite in favorites]
    return jsonify(favorites)


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def favorite_create_planet(planet_id):
    user_id = request.headers.get('user_id')
    new_favorite = Favorites(type='planet', element_id=planet_id, user_id=user_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet created"}), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def favorite_create_people(people_id):
    user_id = request.headers.get('user_id')
    new_favorite = Favorites(type='people', element_id=people_id, user_id=user_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite people created"}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def favorite_delete_planet(planet_id):
    user_id = request.headers.get('user_id')
    favorite = Favorites.query.filter_by(type='planet', element_id=planet_id, user_id=user_id).first()
    if favorite is None:
        return jsonify({"msg": "Favorite planet not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def favorite_delete_people(people_id):
    user_id = request.headers.get('user_id')
    favorite = Favorites.query.filter_by(type='people', element_id=people_id, user_id=user_id).first()
    if favorite is None:
        return jsonify({"msg": "Favorite people not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite people deleted"}), 200


@app.route('/people', methods=['GET'])
def people_get():
    people = People.query.all()
    people = [person.serialize()
     for person in people]
    return jsonify(people)


@app.route('/people/<int:people_id>', methods=['GET'])
def person_get(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"msg": "Person not found"}), 404
    return jsonify(person.serialize())


@app.route('/planets', methods=['GET'])
def planets_get():
    planets = Planets.query.all()
    planets = [planet.serialize() for planet in planets]
    return jsonify(planets)


@app.route('/planets/<int:planet_id>', methods=['GET'])
def planet_get(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize())



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)