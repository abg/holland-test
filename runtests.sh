#!/bin/bash
export NOSE_TEST_CONFIG_FILE=${NOSE_TEST_CONFIG_FILE:-"test.conf"}

coverage erase
nosetests -v 
coverage combine
coverage report
