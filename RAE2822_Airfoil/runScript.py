#!/usr/bin/env python
"""
DAFoam run script for the RAE2822 case
"""

# =============================================================================
# Imports
# =============================================================================
from mpi4py import MPI
from dafoam import PYDAFOAM
import numpy as np

# =============================================================================
# Input Parameters
# =============================================================================

# global parameters
M = 0.729
T0 = 255.56
c = float(np.sqrt(1.4 * 287 * T0))
U0 = c * M
p0 = 108988.0
rho0 = p0 / T0 / 287.0
nuTilda0 = 4.5e-5
k0 = 8.5
epsilon0 = 4.3e4
omega0 = 5.6e4
A0 = 0.01
alpha0 = 2.31


def calcUAndDir(UMag, alpha1):
    dragDir = [float(np.cos(alpha1 * np.pi / 180)), float(np.sin(alpha1 * np.pi / 180)), 0.0]
    liftDir = [float(-np.sin(alpha1 * np.pi / 180)), float(np.cos(alpha1 * np.pi / 180)), 0.0]
    inletU = [float(UMag * np.cos(alpha1 * np.pi / 180)), float(UMag * np.sin(alpha1 * np.pi / 180)), 0.0]
    return inletU, dragDir, liftDir


inletU, dragDir, liftDir = calcUAndDir(U0, alpha0)

# Set the parameters for optimization
daOptions = {
    "solverName": "DARhoSimpleCFoam",
    "primalMinResTol": 1.0e-7,
    "primalBC": {
        "U0": {"variable": "U", "patches": ["inout"], "value": inletU},
        "p0": {"variable": "p", "patches": ["inout"], "value": [p0]},
        "T0": {"variable": "T", "patches": ["inout"], "value": [T0]},
        "nuTilda0": {"variable": "nuTilda", "patches": ["inout"], "value": [nuTilda0]},
        "k0": {"variable": "k", "patches": ["inout"], "value": [k0]},
        "omega0": {"variable": "omega", "patches": ["inout"], "value": [omega0]},
        "epsilon0": {"variable": "epsilon", "patches": ["inout"], "value": [epsilon0]},
        "useWallFunction": False,
    },
    "function": {
        "CD": {
                "type": "force",
                "source": "patchToFace",
                "patches": ["wing"],
                "directionMode": "fixedDirection",
                "direction": dragDir,
                "scale": 1.0 / (0.5 * rho0 * U0 * U0 * A0),
                "addToAdjoint": True,
        },
        "CL": {
                "type": "force",
                "source": "patchToFace",
                "patches": ["wing"],
                "directionMode": "fixedDirection",
                "direction": liftDir,
                "scale": 1.0 / (0.5 * rho0 * U0 * U0 * A0),
                "addToAdjoint": True,
        },
    },
    "checkMeshThreshold": {"maxAspectRatio": 5000.0},
}

DASolver = PYDAFOAM(options=daOptions, comm=MPI.COMM_WORLD)
DASolver()

#
#funcs = {}
#evalFuncs = ["CD", "CL"]
#DASolver.evalFunctions(funcs, evalFuncs)
