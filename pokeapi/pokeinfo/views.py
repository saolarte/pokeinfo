from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponseNotFound

from.models import Pokemon, Evolution, Stats

def fetch_pokemon(poke_name):
    body = {}
    poke = Pokemon.objects.filter(name = poke_name)
    if len(poke) > 0:
        body['id'] = poke[0].poke_id
        body['name'] = poke[0].name
        body['height'] = poke[0].height
        body['weight'] = poke[0].weight
        return body

def fetch_stats(poke_id):
    body = {'stats': {}}
    stats = Stats.objects.filter(poke_id = poke_id)
    for stat in stats:
        body['stats'][stat.stat_name] = stat.stat_score
    return body

def fetch_evolution(poke_id):
    body = {'evolution': []}
    evolution = Evolution.objects.filter(poke_id = poke_id)
    for evol in evolution:
        evolution_type = "preevolution" if evol.evolution_type == 0 else "evolution"
        body['evolution'].append({  'id' : evol.id_evolution,
                                    'evolution_type' : evolution_type,
                                    'name' : evol.name,
                                    }) 
    return body


def fetch(request, poke_name):
    poke_info = fetch_pokemon(poke_name)
    if poke_info:
        poke_stats = fetch_stats(poke_info['id'])
        poke_evolution = fetch_evolution(poke_info['id'])
        response = {**poke_info, **poke_stats, **poke_evolution}
        return JsonResponse(response)
    else:
        return HttpResponseNotFound({"Pokemon not found in database"})