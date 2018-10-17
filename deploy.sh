#!/usr/bin/env bash

pipenv  lock --requirements > requirements.txt
git     add -A
git     add -f .secrets
git     add -f requirements.txt
git     status
eb      deploy --profile project-pmb --staged
git     reset head .secrets
git     reset head requirements.txt
rm      requirements.txt
