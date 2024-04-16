import requests, json, pandas as pd, plotly.express as px
base_url = 'https://pokeapi.co/api/v2/'
pokemon_info = {'Name': [], 'Types': [], 'Generation': [] , 'Attribute': [], 'IV': []}

#function to gather pokemon per gen(made to also get other gens)
def catch_pokemon_gen(n):
    url = f'https://pokeapi.co/api/v2/generation/{n}'
    p = requests.get(url)
    info = p.json()
    poke_list = []

    for pokemon in info['pokemon_species']:
        name = pokemon['name']
        poke_list.append(name)

    return poke_list

gen1 = catch_pokemon_gen(1)
gen2 = catch_pokemon_gen(2)
gen3 = catch_pokemon_gen(3)
gen4 = catch_pokemon_gen(4)

#function to gather pokemon types
def catch_pokemon_type(name):
    url = base_url + 'pokemon/' + name
    p = requests.get(url)
    info = p.json()
    types = [type['type']['name'] for type in info['types']]#since a pokemon can have 2 types, we read both and add them in a list
    return types

#function to gather pokemon info on its attributes
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

#function for gathering info in a DF
def catch_all_info(list):
    for pokemon in list:
        try:
            types = catch_pokemon_type(pokemon)
            attribute, iv = catch_pokemon_iv(pokemon)
            pokemon_info['Name'].append(pokemon)
            pokemon_info['Types'].append(types)
            pokemon_info['Attribute'].append(attribute)
            pokemon_info['IV'].append(iv)
        except Exception as e:
            print(f'error on pokemon {pokemon}')
    return pokemon_info

#used this space to gather info per gen since requests took long time
#and creating dataframe per generation
gen1_info = catch_all_info(gen1)
gen1df = pd.DataFrame(gen1_info)
gen1df.index += 1
pokemon_info = {'Name': [], 'Types': [], 'Attribute': [], 'IV': [],}

gen2_info = catch_all_info(gen2)
gen2df = pd.DataFrame(gen2_info)
gen2df.index += 1
pokemon_info = {'Name': [], 'Types': [], 'Attribute': [], 'IV': [],}

gen3_info = catch_all_info(gen3)
gen3df = pd.DataFrame(gen3_info)
gen3df.index += 1
pokemon_info = {'Name': [], 'Types': [], 'Attribute': [], 'IV': [],}

gen4_info = catch_all_info(gen4)
gen4df = pd.DataFrame(gen4_info)
gen4df.index += 1
pokemon_info = {'Name': [], 'Types': [], 'Attribute': [], 'IV': [],}

#sum of generations into a single DataFrame
total = [gen1df, gen2df, gen3df, gen4df]
totaldf = pd.concat(total)
totaldf = totaldf.reset_index()

#overall type DataFrame
total_types = totaldf['Types'].str[0]
total_types = total_types.value_counts()
types_df = pd.DataFrame(total_types).reset_index()
types_df = types_df.astype({'Types':'str', 'count': 'int'})

#overall attributes DataFrame
total_attributes = totaldf['Attribute']
total_attributes = total_attributes.value_counts()
attributes_df = pd.DataFrame(total_attributes).reset_index()

#overall types plot
type_colors = { 'water':'#6890F0','normal':'#A8A878','bug':'#A8B820','grass':'#78C850','fire':'#F08030','electric':'#F8D030','psychic':'#F85888','poison':'#A040A0','rock':'#B8A038','ground':'#E0C068','fighting':'#C03028','fairy':'#EE99AC','ice':'#98D8D8','dark':'#705848','ghost':'#705898','dragon':'#7038F8','steel':'#B8B8D0'}
type_plot = px.pie(types_df, names='Types', values='count',color='Types',color_discrete_map=type_colors)
type_plot.show()

#overall attributes plot
attribute_colors= {'attack':'#DC143C','special-attack':'#6495ED','speed':'#E9967A','defense':'#FFD700','hp':'#B22222','special-defense':'#8FBC8F'}
attribute_plot = px.bar(attributes_df, x = 'Attribute', y = 'count', color='Attribute',color_discrete_map = attribute_colors)
attribute_plot.show()
