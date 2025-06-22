from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///podcast.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    episode_list = [episode.to_dict(rules=('-appearances',)) for episode in episodes]
    return jsonify(episode_list), 200

@app.route('/episodes/<int:episode_id>', methods=['GET'])
def get_episode_by_id(episode_id):
    episode = Episode.query.get(episode_id)
    if episode is None:
        return jsonify({'error': 'Episode not found'}), 404
    return jsonify(episode.to_dict()), 200


@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    guest_list = [guest.to_dict(rules=('-appearances',)) for guest in guests]
    return jsonify(guest_list), 200

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()

    try:
        rating = data['rating']
        episode_id = data['episode_id']
        guest_id = data['guest_id']

        new_appearance = Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)

        db.session.add(new_appearance)
        db.session.commit()

        guest = Guest.query.get(guest_id)
        episode = Episode.query.get(episode_id)

        response_data = {
            'id': new_appearance.id,
            'rating': new_appearance.rating,
            'episode_id': new_appearance.episode_id,
            'guest_id': new_appearance.guest_id,
            'episode': episode.to_dict(),
            'guest': guest.to_dict()
            
        }

        return jsonify(response_data), 201
    
    except KeyError as e:
        return jsonify({'error': ['validation errors']}), 400


if __name__ == '__main__':
    app.run(debug=True)

