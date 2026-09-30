install:
	pip install -r requirements.txt

kafka:
	docker compose up -d kafka

run:
	uvicorn app.main:app --reload

test:
	pytest -q

etl:
	python -m pipeline.batch_etl

dashboard:
	streamlit run dashboard.py

docker-up:
	docker compose up --build
