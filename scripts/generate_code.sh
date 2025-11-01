#!/bin/bash

set -e

cd "$(git rev-parse --show-toplevel)"

python3 ./scripts/generate_code.py

cargo fmt
