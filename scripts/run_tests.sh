#!/bin/bash
set -eu

function display {
    local WHITE='\033[0;37m'
    local NC='\033[0m'
    echo -e "${WHITE}==== ${1} ====${NC}"
}

SOURCE_FOLDER=./pynetfuzz/
SOURCE_FILES=$(find $SOURCE_FOLDER -maxdepth 2 -name '*.py' -type f | grep -v '__int__\.py\|test[^/]*\.py')
display "Source files"
echo $SOURCE_FILES

TEST_FOLDER=./tests/
TEST_FILES=$(find $TEST_FOLDER -name 'test*.py' -type f | grep -v '__int__\.py\|*\.cfg' | sed 's/\.\///g' )
display "Test files"
echo $TEST_FILES

#Pylint
pylint -r n $SOURCE_FILES 2>/dev/null || true
# Unittests
coverage_run=$(coverage run --source $SOURCE_FOLDER -m unittest $TEST_FILES) || true
# Coverage
coverage report || true