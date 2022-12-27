line_len=120

targets=jupyterblack/ tests/

ISORT_CONFIG=pyproject.toml

# FORMAT ---------------------------------------------------------------------------------------------------------------
fmt: black isort docformatter autoflake

black:
	black -l $(line_len) $(targets)

isort:
	isort --settings-path $(ISORT_CONFIG) $(targets)

docformatter:
	docformatter --in-place --wrap-summaries=$(line_len) --wrap-descriptions=$(line_len) -r $(targets)

autoflake:
	autoflake --in-place --remove-all-unused-imports -r $(targets)

# LINT -----------------------------------------------------------------------------------------------------------------
lint: docformatter-check isort-check black-check autoflake-check flake8 pylint

black-check:
	black --check -l $(line_len) $(targets)


docformatter-check:
	docformatter --wrap-summaries=$(line_len) --wrap-descriptions=$(line_len) -r $(targets) && \
	docformatter --check --wrap-summaries=$(line_len) --wrap-descriptions=$(line_len) -r $(targets)

isort-check:
	isort --diff --color --check-only --settings-path $(ISORT_CONFIG) $(targets)

autoflake-check:
	autoflake --in-place --remove-all-unused-imports -r $(targets)

flake8:
# Workaround: must add --ignore flag for Python3.7 to comply in GitHub CI/CD workflow
	flake8 --ignore=E203,E501,E701 $(targets)

pylint:
	pylint $(targets)

# TYPE CHECK -----------------------------------------------------------------------------------------------------------
mypy:
	mypy --config-file mypy.ini $(targets)

# TEST -----------------------------------------------------------------------------------------------------------------
test:
	pytest -vv $(targets)

# DEPLOY TO PYPI -------------------------------------------------------------------------------------------------------
deploy:
	python setup.py sdist bdist_wheel;
	twine upload dist/*;
	make clean-pyc;
	make clean-build

# CLEAN ----------------------------------------------------------------------------------------------------------------
clean-pyc:
	find . -name *.pyc | xargs rm -f && find . -name *.pyo | xargs rm -f

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info


# OTHERS  --------------------------------------------------------------------------------------------------------------
pre-commit: mypy flake8 isort docformatter

check-all: mypy lint test
