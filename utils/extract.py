import typing as tp


def extract_id(url: str) -> int:
    # Extracts id from an url of the API
    # Example: 'https://pokeapi.co/api/v2/type/4/' => 4
    return int(url.strip().strip('/').split('/')[-1])


def extract_pokemon(data: tp.Dict) -> tp.Dict:
    return dict(
        id=data['id'],
        name=data['name'],
        types=[extract_id(record['type']['url']) for record in data['types']],
        moves=[extract_id(record['move']['url']) for record in data['moves']],
        stats=[
            dict(
                stat_id=extract_id(stat['stat']['url']),
                value=stat['base_stat']
            )
            for stat in data['stats']
        ]
    )


def extract_generation(data: tp.Dict) -> tp.Dict:
    return dict(
        id=data['id'],
        name=data['name'],
        types=[extract_id(record['url']) for record in data['types']],
        pokemon_species=[extract_id(record['url']) for record in data['pokemon_species']],
    )


def extract_move(data: tp.Dict) -> tp.Dict:
    return dict(
        id=data['id'],
        name=data['name'],
        generation=extract_id(data['generation']['url']),
        type=extract_id(data['type']['url']),
        pokemons=[extract_id(record['url']) for record in data['learned_by_pokemon']],
    )


def extract_pokemon_species(data: tp.Dict) -> tp.Dict:
    return dict(
        id=data['id'],
        name=data['name'],
        generation=extract_id(data['generation']['url']),
        pokemons=[extract_id(record['pokemon']['url']) for record in data['varieties']],
    )


def extract_type(data: tp.Dict) -> tp.Dict:
    return dict(
        id=data['id'],
        name=data['name'],
        generation=extract_id(data['generation']['url']),
        pokemons=[extract_id(record['pokemon']['url']) for record in data['pokemon']],
    )
