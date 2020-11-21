import json

import requests
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError

from ...models import Pokemon, Evolution, Stats


def get_information(name):
    """
    Retrieve Pokemon information from pokeapi endpoint given Pokemon name
    Returns: Dict with Pokemon information
    """
    info_dict = {}
    endpoint = 'https://pokeapi.co/api/v2/pokemon/{}/'
    pokemon = requests.get(endpoint.format(name)).json()
    information_fields = ['id', 'name', 'height', 'weight', 'stats' ]
    for info in information_fields:
        info_dict[info] = pokemon[info]
    return info_dict


def get_evolution_chain(chain_id):
    """
    Retrieve evolution chain given chain id
    Returns: List with pokemon info according to evolution chain
    """
    endpoint = 'https://pokeapi.co/api/v2/evolution-chain/{}/'
    endpoint = endpoint.format(chain_id)
    pokemon_info_list =[]
    status = False
    try:
        res = requests.get(endpoint).json()
        status = True
    except json.decoder.JSONDecodeError as error:
        print(str(error))
        print(endpoint)
    
    if status:
        evol_chain = res['chain']
        member = evol_chain
        while True:
            pokemon_info_list.append(get_information(member['species']['name']))
            if(len(member['evolves_to']) > 0):
                member = member['evolves_to'][0]
            else:
                break
        return True, pokemon_info_list
    else:
        return False, []


def insert_pokemon(pokemon_info_list):
    """
    Inserts pokemon info to database
    """
    for pokemon in pokemon_info_list:
        try:
            pokemon_object = Pokemon.objects.create(poke_id = pokemon['id'],
                                            name = pokemon['name'],
                                            height = pokemon['height'] ,
                                            weight = pokemon['weight'])
        except IntegrityError:
            print('Pokemon {} already exists in database'.format(pokemon['name']))
    
def insert_evolution(pokemon_info_list):
    """
    Inserts evolution data.
    Inserts rows with evolution_type = 0 if it's a preevolution 
    Inserts rows with evolution_type = 1 if it's an evolution 

    """
    for idx, pokemon in enumerate(pokemon_info_list):
        for i in range (idx-1, -1, -1):
            try:
                evolution_object = Evolution.objects.create(poke_id = pokemon['id'],
                                                            evolution_type = 0,  
                                                            id_evolution = pokemon_info_list[i]['id'],
                                                            name = pokemon_info_list[i]['name'])
            except IntegrityError:
                pass   
        for i in range (idx+1, len(pokemon_info_list)):
            try:
                evolution_object = Evolution.objects.create(poke_id = pokemon['id'],
                                                            evolution_type = 1,  
                                                            id_evolution = pokemon_info_list[i]['id'],
                                                            name = pokemon_info_list[i]['name'])
            except IntegrityError:
                pass    


def insert_stats(pokemon_info_list):
    for pokemon in pokemon_info_list:
        stats = pokemon['stats']
        for stat in stats:
            try:
                evolution_object = Stats.objects.create(poke_id = pokemon['id'],
                                                        stat_name =  stat['stat']['name'],  
                                                        stat_score = stat['base_stat'])
            except IntegrityError:
                pass   


def populate_db(pokemon_info_list):
    insert_pokemon(pokemon_info_list)
    insert_evolution(pokemon_info_list)
    insert_stats(pokemon_info_list)



class Command(BaseCommand):
    help = 'Retrieve evolution chain from PokeApi'

    def add_arguments(self, parser):
        parser.add_argument('chain_id', nargs='+', type=int)

    def handle(self, *args, **options):
        status, pokemon_info_list = get_evolution_chain(options['chain_id'][0])
        if status:
            populate_db(pokemon_info_list)
            self.stdout.write("Evolution chain saved ")

        else:
            self.stdout.write("There was an error getting info from Endpoint")
        