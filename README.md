Populate database through manage.py command

1. Log into docker container:
docker exec -it {container_id} bash

2. Run the command:
python manage.py evochain {chain_id}



Retrieve pokemon info through a GET request to endpoint:

localhost:8001/pokeinfo/{pokemon_name}