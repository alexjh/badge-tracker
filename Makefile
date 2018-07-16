.PHONY: run test build publish docker-run

run:
	FLASK_APP=badge_tracker.py flask run

TESTED_FILES = \
	       app/routes.py \
	       badge_tracker.py \
               config.py


test:
	pytest --doctest-modules \
	       --cov=. \
	       --cov-report term-missing \
	       --flake8 \
	       --pep8 \
	       $(addprefix skills/, $(TESTED_FILES))

build: test
	sudo docker build -t badge-tracker .

reformat:
	black .

publish: test
	sudo docker tag badge-tracker alexharford/badge-tracker:latest
	sudo docker push alexharford/badge-tracker:latest

docker-run: test
	sudo docker run --rm --name badge-tracker \
		-p 5000:5000 \
		badge-tracker
