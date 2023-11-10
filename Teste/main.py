import requests, json, pandas as pd, matplotlib as plt
base_url = 'https://pokeapi.co/api/v2/'
pokemon_info = {'Name': [], 'Types': [], 'Generation': [] , 'Attribute': [], 'IV': []}

#function to fetch all pokemons names
def catch_pokemon_gen(n):
    url = 'https://pokeapi.co/api/v2/generation/{}'.format(n)
    p = requests.get(url)
    info = p.json()
    pokemon_list = []

    for pokemon in info['pokemon_species']:
        pokemon_name = pokemon['name']
        pokemon_list.append(pokemon_name)

    return pokemon_list
gen1 = catch_pokemon_gen(1)
gen2 = catch_pokemon_gen(2)
gen3 = catch_pokemon_gen(3)
gen4 = catch_pokemon_gen(4)

all_names = [*gen1,*gen2,*gen3,*gen4]

#function to fetch the pokemon type
def catch_pokemon_type(name):
    url = base_url + 'pokemon/' + name
    p = requests.get(url)
    info = p.json()
    types = [type['type']['name'] for type in info['types']]
    return types

#function to fetch pokemon stats
def catch_pokemon_iv(name):
    url = base_url + 'pokemon/' + name
    p = requests.get(url)
    info = p.json()
    attributes = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
    highest_attribute = attributes[0]
    highest_attribute_iv = 0

    for i in range(len(attributes)):
        iv_value = info['stats'][i]['base_stat']

        if iv_value > highest_attribute_iv:
            highest_attribute_iv = iv_value
            highest_attribute = attributes[i]

    return highest_attribute, highest_attribute_iv 

def catch_all_info(list):
    for pokemon in list:
        types = catch_pokemon_type(pokemon)
        attribute, iv = catch_pokemon_iv(pokemon)
        pokemon_info['Name'].append(pokemon)
        pokemon_info['Types'].append(types)
        pokemon_info['Attribute'].append(attribute)
        pokemon_info['IV'].append(iv)
    return pokemon_info
    