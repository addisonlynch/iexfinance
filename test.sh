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

if [[ -z ${IEX_TOKEN} ]]; then
	exit "IEX_TOKEN not found. Please export a test test 'IEX_TOKEN' in your environment to run pytests: export IEX_TOKEN=\"Tpk_...\""
fi

if [[ !(${IEX_TOKEN} != "Tpk*" && ${IEX_TOKEN} != "Tsk*") ]]; then
	exit "The IEX_TOKEN exported is not a test token. This should not be used for tests."
fi

pytest -x iexfinance/tests
rc=$?;

if [[ $rc != 0 ]]; then
	echo "Pytest failed."
	exit $rc
fi
echo "PASSED"

echo 'All tests passed!'
