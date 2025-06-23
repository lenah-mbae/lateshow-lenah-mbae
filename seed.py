from app import app
from models import db, Episode, Guest, Appearance
from datetime import datetime
import csv
import random  # for dummy ratings

def seed_database():
    print("🌱 Seeding database...")

    with app.app_context():

        # Clear existing data
        Appearance.query.delete()
        Guest.query.delete()
        Episode.query.delete()

        with open('seed.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')


            episode_number = 1  # Start numbering from 1

            for row in reader:
                # Parse and clean fields
                date_str = row['Show'].strip()
                guest_name = row['Raw_Guest_List'].strip()
                guest_occupation = row['GoogleKnowlege_Occupation'].strip()
                rating = random.randint(1, 5)  # Assign random rating for now

                # Create episode
                episode = Episode(
                    number=episode_number,
                    date=datetime.strptime(date_str, '%m/%d/%y') if len(date_str.split('/')[-1]) == 2 else datetime.strptime(date_str, '%m/%d/%Y')
                )
                db.session.add(episode)

                # Create guest
                guest = Guest(
                    name=guest_name,
                    occupation=guest_occupation
                )
                db.session.add(guest)

                db.session.flush()  # Get IDs

                # Create appearance
                appearance = Appearance(
                    rating=rating,
                    guest_id=guest.id,
                    episode_id=episode.id
                )
                db.session.add(appearance)

                episode_number += 1

            db.session.commit()
            print("✅ Seeding complete!")

if __name__ == '__main__':
    seed_database()
