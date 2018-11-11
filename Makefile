clean: # clean the repository
	find . -name "__pycache__" | xargs  rm -rf
	find . -name "*pytest_cache" | xargs rm -rf
	find . -name "*.pyc" | xargs rm -rf
	rm -rf .coverage cover htmlcov logs build dist *.egg-info
