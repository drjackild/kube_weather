compile-deps:
	@pip-compile requirements.in
	@pip-compile requirements-dev.in

sync-deps:
	@pip-sync requirements.txt requirements-dev.txt

format:
	@black .
	@isort .
