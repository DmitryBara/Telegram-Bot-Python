TAG_NAME = dmitry/memes_creator_bot

start:
	docker-compose up --build

stop:
	docker stop bot_master

inst-pytest:
	docker exec -it bot_master pip install pytest

test:
	docker exec -it bot_master python -m pytest tests

