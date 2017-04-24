#!/bin/bash

# Enables all project specific git hooks.

cd .git/hooks
find ../../githooks -type f -exec ln -sf {} . \;
cd ../..
