#! /bin/bash
source /var/www/myapp/myenv/bin/activate

# All options to the run_tests.sh script will be passed on to pytest. The -k option allows you to run a subset of tests by selecting keyword expressions. For example:
#   pytest -k "MyClass and not method"
# This will run tests which contain names that match the given string expression, which can include Python operators that use filenames, class names and function names as variables. The example above will run TestMyClass.test_something but not TestMyClass.test_method_simple.

PYTHONPATH=$PYTHONPATH:/var/www/myapp python3 -m pytest $@