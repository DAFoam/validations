#!/usr/bin/env python
"""
DAFoam run script for the RAE2822 airfoil at transonic conditions
"""

# =============================================================================
# Imports
# =============================================================================
import os
import argparse
import numpy as np
from mpi4py import MPI
import openmdao.api as om
from mphys.multipoint import Multipoint
from dafoam.mphys import DAFoamBuilder, OptFuncs
from mphys.scenario_aerodynamic import ScenarioAerodynamic
from pygeo.mphys import OM_DVGEOCOMP
from pygeo import geo_utils
from dafoam import PYDAFOAM


# =============================================================================
# Input Parameters
# =============================================================================

# NOTE: Input Parameters Must Also be Specified in "0/include/freestreamconditions"

U0 = 233.603
p0 = 108988.0
T0 = 255.56
nuTilda0 = 4.5e-5
CL_target = 0.7
twist0 = 2.52517169
A0 = 0.01
alpha0= 2.31
k0= 8.5
omega0= 5.6e4
epsilon0= 4.3e4
# rho is used for normalizing CD and CL
rho0 = p0 / T0 / 287


def calcUAndDir(UMag, alpha1):
    dragDir = [float(np.cos(alpha1 * np.pi / 180)), float(np.sin(alpha1 * np.pi / 180)), 0.0]
    liftDir = [float(-np.sin(alpha1 * np.pi / 180)), float(np.cos(alpha1 * np.pi / 180)), 0.0]
    inletU = [float(UMag * np.cos(alpha1 * np.pi / 180)), float(UMag * np.sin(alpha1 * np.pi / 180)), 0.0]
    return inletU, dragDir, liftDir


inletU, dragDir, liftDir = calcUAndDir(U0, alpha0)


# Input parameters for DAFoam
daOptions = {
    "designSurfaces": ["wing"],
    "solverName": "DAHisaFoam",
#    "primalInitCondition": {"U": [Ux, Uy, 0.0], "p": p0, "T": T0},
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
            "direction": [1.0, 0.0, 0.0],
            "scale": 1.0 / (0.5 * U0 * U0 * A0 * rho0),
        },
        "CL": {
            "type": "force",
            "source": "patchToFace",
            "patches": ["wing"],
            "directionMode": "fixedDirection",
            "direction": [0.0, 1.0, 0.0],
            "scale": 1.0 / (0.5 * U0 * U0 * A0 * rho0),
        },
    },
    "checkMeshThreshold": {"maxNonOrth": 70.0, "maxSkewness": 6.0, "maxAspectRatio": 5000.0},

}


DASolver = PYDAFOAM(options=daOptions, comm=MPI.COMM_WORLD)
DASolver()

#
#funcs = {}
#evalFuncs = ["CD", "CL"]
#DASolver.evalFunctions(funcs, evalFuncs)
