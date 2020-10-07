# -*- coding: utf-8 -*-

__version__ = "1.0.0"

# "profile" module
from . import profile, inputs

# "core" module
from . import core_system
from .integration import integrate
from .core_system.network import *
from .core_system.neuron_group import *
from .core_system.synapse_connection import *
from .core_system import types


#
from . import visualization as visualize
from . import connectivity as connect

#
# # reload functions
# def _reload():
#     global judge_spike
#     global clip
#
#     judge_spike = get_spike_judger()
#     clip = get_clip()
#
#

