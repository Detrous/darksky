PACKAGES = $$(python -c "from setuptools import find_packages; print(' '.join({p.split('.')[0] + '/' for p in find_packages()}))")

test:
	python -m pytest -s -v --html="artefacts/pytest/pytest.html" --self-contained-html --cov=./ --cov-report html:artefacts/coverage_html . 

style:
	isort -y 
	autopep8 --in-place --aggressive --aggressive --recursive --exclude=venv .

lint-pylint:
	pylint -v --output-format=parseable $(PACKAGES) -j 0

lint-flake8:
	flake8 --config=".flake8" 

lint-isort:
	isort --check-only

lint: lint-pylint lint-flake8 lint-isort
