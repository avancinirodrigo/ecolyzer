#!/bin/bash

cp -r ../flask_ecolyzer .
cp app.yaml flask_ecolyzer
cp -r ../ecolyzer flask_ecolyzer

cp ../requirements.txt flask_ecolyzer
cat ../flask_ecolyzer/requirements.txt >> flask_ecolyzer/requirements.txt
