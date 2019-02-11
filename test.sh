#! /bin/bash

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
    exit $rc;
fi
echo "PASSED"

echo "pytest..."
pytest -x tests
rc=$?;

if [[ $rc != 0 ]]; then
	echo "Pytest failed."
	exit $rc
fi
echo "PASSED"

echo 'All tests passed!'
