#!/bin/bash

# Change to the target directory
cd simulations/aldp

# Find all .pt files and rename them to test.pt
find . -type f -name "*.pt" -execdir mv {} test.pt \;