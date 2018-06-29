.PHONY: run test build publish docker-run

run:
	FLASK_APP=badge_tracker.py flask run

TESTED_FILES = \
	       app/routes.py \
	       etsy_api.py \
	       exchange.py \
               config.py


test:
	pytest --doctest-modules \
	       --cov=. \
	       --cov-report term-missing \
	       --flake8 \
	       --pep8 \
	       $(addprefix etsy-check/, $(TESTED_FILES))

build: test
	sudo docker build -t ajh-etsy .

reformat:
	black etsy-check

publish: test
	sudo docker tag ajh-etsy alexharford/etsy-check:latest
	sudo docker push alexharford/etsy-check:latest

docker-run: test
	source ./creds.sh && \
	sudo docker run --rm --name ajh-etsy \
		-e ETSY_API_KEY=$${ETSY_API_KEY} \
		-e CURRENCY_API_KEY=$${CURRENCY_API_KEY} \
		-p 5000:5000 \
		ajh-etsy
