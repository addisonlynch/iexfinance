#! /bin/bash

echo "black check..."
black --check .
rc=$?; if [[ $rc != 0 ]]; then
	echo "black check failed."
	exit $rc;
fi
echo "PASSED"

echo "flake8 check..."
flake8 .
rc=$?; if [[ $rc != 0 ]]; then
	echo "flake8 check failed."
	exit $rc;
fi
echo "PASSED"

echo "flake8-rst docs check..."
flake8-rst --filename="*.rst" .
rc=$?; if [[ $rc != 0 ]]; then
    echo "flake8-rst docs check failed."
		echo "Run the pytests manually in case you're hitting this bug: https://github.com/kataev/flake8-rst/issues/24."
    exit $rc;
fi
echo "PASSED"

echo "pytest..."

pytest -x iexfinance/tests
rc=$?;

if [[ $rc != 0 ]]; then
	echo "Pytest failed."
	exit $rc
fi
echo "PASSED"

echo 'All tests passed!'
