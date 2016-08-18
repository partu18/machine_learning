VENV_NAME='ml_venv'

all:
	virtualenv $(VENV_NAME)
	$(VENV_NAME)/bin/pip install -r requirements.txt

clean:
	rm -rf $(VENV_NAME)
