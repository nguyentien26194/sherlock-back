shell:
	docker exec -it sherlock-back python sherlock/manage.py shell

makemigrations:
	docker exec sherlock-back python sherlock/manage.py makemigrations

migrate:
	docker exec sherlock-back python sherlock/manage.py migrate

format:
	docker exec sherlock-back /bin/bash -c "black . && isort sherlock/"

test:
	docker exec sherlock-back python sherlock/manage.py test sherlock/
