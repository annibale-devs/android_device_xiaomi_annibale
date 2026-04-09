#!/bin/bash
# Script to dynamically reassemble .part* files

for file in $(find "vendor/xiaomi/annibale" -type f -name "*.part00"); do
    base_name=${file%.part00}
    cat ${base_name}.part* > $base_name
    echo "Reassembly of $base_name complete!"
done
