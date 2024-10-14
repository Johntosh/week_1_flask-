from flask import Flask, request
from flask_migrate import Migrate
from models import Hero, HeroPower, Power, db
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)
Migrate(app, db)


@app.route('/')
def index():
    """Return a string indicating that the API is live."""

    return '''
        <h1>Superheroes API</h1>
    
        <h2><code>GET /</code></h2>
        <p>Returns a welcome message indicating the API is live <em>(This page)</em>.</p>
    
        <h2><code>GET /heroes</code></h2>
        <p>Returns a list of all heroes, excluding their related powers.</p>
    
        <h2><code>GET /heroes/&lt;id&gt;</code></h2>
        <p>Fetches details for a specific hero by their ID. Returns 404 Not Found if the hero is not found.</p>
    
        <h2><code>GET /powers</code></h2>
        <p>Returns a list of all available powers.</p>
    
        <h2><code>GET /powers/&lt;id&gt;</code></h2>
        <p>Returns details of a specific power by ID. Returns 404 Not Found if the power is not found.</p>
    
        <h2><code>PATCH /powers/&lt;id&gt;</code></h2>
        <p>Allows updates to a power's details using a JSON payload. Returns 404 Not Found if the power is not found.</p>
    
        <h2><code>POST /hero_powers</code></h2>
        <p>Creates a new hero-power relationship, with custom strength, using a JSON payload. Returns 400 Bad Request if the JSON payload is invalid.</p>
    '''


@app.route('/heroes', methods=['GET'])
def get_heroes():
    """Get a list of all the heroes."""

    heroes = Hero.query.all()

    return [hero.to_dict(rules=('-hero_powers', )) for hero in heroes]


@app.route('/heroes/<int:id>')
def hero_by_id(id):
    """Return a hero by id."""

    hero = Hero.query.get(id)

    if not hero:
        return {'error': 'Hero not found'}, 404

    return hero.to_dict()


@app.route('/powers')
def powers():
    """Get a list of all the powers."""

    powers = Power.query.all()
    return [power.to_dict(rules=('-hero_powers', )) for power in powers]


@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def get_or_update_power(id):
    """Get a power by id or update a power by id."""

    power = Power.query.get(id)

    if not power:
        return {'errors': ['Power not found']}, 404

    if request.method == 'GET':
        return power.to_dict(rules=('-hero_powers', ))

    elif request.method == 'PATCH':
        try:
            for key, value in request.json.items():
                setattr(power, key, value)
            db.session.commit()
        except ValueError as e:
            return {'errors': [str(e)]}, 400
        except:
            return {'errors': ['An unexpected error occurred.']}, 500

        return power.to_dict(rules=('-hero_powers', ))


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    """Create a new hero-power relationship."""

    try:
        data = request.json

        # Query the database to check if if hero_id and power_id exist
        hero = db.session.get(Hero, data['hero_id'])
        power = db.session.get(Power, data['power_id'])

        if hero is None:
            raise ValueError('Invalid hero_id provided.')
        if power is None:
            raise ValueError('Invalid power_id provided.')

        new_hero_power = HeroPower(strength=data['strength'],
                                   power_id=data['power_id'],
                                   hero_id=data['hero_id'])
        db.session.add(new_hero_power)
        db.session.commit()

        return new_hero_power.to_dict(), 201
    except (ValueError, KeyError, IntegrityError) as e:
        errors = []
        if isinstance(e, ValueError):
            errors.append(str(e))
        elif isinstance(e, KeyError):
            errors.append(f"Missing required field: {e}")
        elif isinstance(e, IntegrityError) and 'UNIQUE' in str(e):
            errors.append("Duplicate hero-power.")
        return {"errors": errors}, 400
    except:
        return {'errors': ['An unexpected error occurred.']}, 500


if __name__ == '__main__':
    app.run(port=5555, debug=True)
