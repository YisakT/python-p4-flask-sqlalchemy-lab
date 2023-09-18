#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = db.session.get(Animal, id)

    if not animal:
        return make_response('<h1>Animal not found</h1>', 404)
    return f'''
        <ul>Name:
            <li>{animal.name}</li>
        </ul>
        <ul>Species:
            <li>{animal.species}</li>
        </ul>
        <ul>Zookeeper:
            <li>{animal.zookeeper.name if animal.zookeeper else 'None'}</li>
        </ul>
        <ul>Enclosure:
            <li>{animal.enclosure.environment if animal.enclosure else 'None'}</li>
        </ul>
    '''


@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = db.session.get(Zookeeper, id)

    if not zookeeper:
        return make_response('<h1>Zookeeper not found</h1>', 404)

    animals_list = ''.join([f'<ul>Animal: {animal.name}</ul>' for animal in zookeeper.animals])
    return f'''<ul>Name: {zookeeper.name}</ul><ul>Birthday: {zookeeper.birthday}</ul>{animals_list}'''

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = db.session.get(Enclosure, id)

    if not enclosure:
        return make_response('<h1>Enclosure not found</h1>', 404)
    
    
    animals_list = 'Animal: ' + ''.join([f'{animal.name}</li><li>Animal: ' for animal in enclosure.animals])[:-12]
    
    return '''
    <ul>Environment: {}
    </ul>
    <ul>Open to Visitors: {}
    </ul>
    <ul>{}  # animals_list goes here
    </ul>
    '''.format(enclosure.environment, enclosure.open_to_visitors, animals_list)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
