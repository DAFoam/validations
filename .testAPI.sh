#!/usr/bin/env bash
  
if [ -z "$WM_PROJECT" ]; then
  echo "OpenFOAM environment not found, forgot to source the OpenFOAM bashrc?"
  exit 1
fi

echo "Running.."
find */runScript* -type f -exec sed -i '/"primalMinResTol"/c\    "primalMinResTol": 0.9,' {} \;
cd RAE2822_Airfoil && ./preProcessing.sh && python runScript.py && cd - || exit 1
