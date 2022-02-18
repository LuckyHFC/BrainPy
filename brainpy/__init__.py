# -*- coding: utf-8 -*-

__version__ = "2.0.3"


try:
  import jaxlib
  del jaxlib
except ModuleNotFoundError:
  raise ModuleNotFoundError(
    'Please install jaxlib. See '
    'https://brainpy.readthedocs.io/en/latest/quickstart/installation.html#dependency-2-jax '
    'for installation instructions.'
  )


# fundamental modules
from . import errors
from . import tools


# "base" module
from . import base
from .base.base import Base
from .base.collector import Collector, TensorCollector


# "math" module
from . import math
from .math import optimizers
optim = optimizers

# tool modules
from . import connect, initialize, datasets
conn = connect
init = initialize


# "integrators" module
from . import integrators
from .integrators import ode
from .integrators import sde
from .integrators.ode import odeint
from .integrators.ode import set_default_odeint
from .integrators.ode import get_default_odeint
from .integrators.sde import sdeint
from .integrators.sde import set_default_sdeint
from .integrators.sde import get_default_sdeint
from .integrators.joint_eq import JointEq


# "building" module
from .building import brainobjects
from .building import inputs
from .building.brainobjects.base import *
from .building.brainobjects import neurons, synapses


# "simulation" module
from . import simulation
from .simulation.monitor import *
from .simulation.runners import *
from .simulation import measure, parallel


# "analysis" module
from . import analysis


# # "visualization" module
from .visualization import visualize


