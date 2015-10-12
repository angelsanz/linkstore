#!/usr/bin/env bash

set -e

run_flake8_and_ignore_bdd_constants() {
    flake8_output_ignoring_bdd_constants=$(flake8 | grep --invert-match "F821 undefined name '\(description\|context\|it\|given\|when\|then\|before\|after\|self\)'$" || true)
    echo "$flake8_output_ignoring_bdd_constants"

    [[ -z "$flake8_output_ignoring_bdd_constants" ]] || exit 1
}

run_flake8_and_ignore_bdd_constants
