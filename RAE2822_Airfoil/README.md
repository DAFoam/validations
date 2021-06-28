To run this validation case, first download the RAE2822 folder that corresponds to the simulation you would like to run: coarse mesh, medium mesh (Spalart Allmaras), medium mesh (kOmegaSST), or fine mesh.

Once you start a docker container, use the following command to generate the mesh by running the preProcessing.sh script.

<pre>
./preProcessing.sh
</pre>

Next, run the optimization with 4 CPU cores as follows.

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

To extract the pressure distribution from the optimization, open the Paraview.foam file in Paraview and check only wing under “Mesh Regions” and only p under “Cell Arrays”. Next, take a z normal slice and right click slice1 -> add filter -> data analysis -> plot on sorted lines. From here you can save the data to be plotted and compared with experimental data.
