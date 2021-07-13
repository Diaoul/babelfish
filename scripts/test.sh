#!/bin/bash

set -ex

pytest --verbose --cov=babelfish --cov-report=term-missing --cov-report=xml tests/
