# validations

[![api_tests](https://github.com/DAFoam/validations/actions/workflows/api_tests.yml/badge.svg)](https://github.com/DAFoam/validations/actions/workflows/api_tests.yml)

This repo contains configuration files to validation the primal solvers in DAFoam.

Go to a subfolder and generate the mesh by running:

<pre>
./preProcessing.sh
</pre>

Then, we can run the primal:

<pre>
mpirun -np 4 python runScript.py 
</pre>