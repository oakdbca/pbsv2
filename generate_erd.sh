#!/bin/bash

timestamp=$(date +%s)
project=pbsv2
output_folder=diagrams/erd
filename=$project$timestamp

echo "Generating ERD for $project"

poetry run python manage.py graph_models -o $filename.dot
dot -Tpdf $filename.dot -o $output_folder/$filename.pdf
rm -f $filename.dot

echo "ERD file generated: $output_folder/$filename.pdf"
