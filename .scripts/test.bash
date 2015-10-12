#!/usr/bin/env bash

set -e

.scripts/lint.bash

.scripts/unit_test.bash
.scripts/acceptance_test.bash
.scripts/end-to-end_test.bash
