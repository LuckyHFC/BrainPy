# -*- coding: utf-8 -*-

from .base_objects import BaseEnsemble
from .base_objects import BaseType
from .base_objects import _SYN_CONN
from .base_objects import _SYN_TYPE
from .neuron_group import NeuGroup
from .types import SynState
from .. import numpy as np
from .. import profile
from ..connectivity import Connector
from ..connectivity import post2syn
from ..connectivity import pre2syn

__all__ = [
    'SynType',
    'SynConn',
    'post_cond_by_post2syn',
    'delay_push',
    'delay_pull',
]

_SYN_NO = 0


class SynType(BaseType):
    """Abstract Synapse Type.

    It can be defined based on a collection of synapses or a single synapse model.
    """

    def __init__(self, name, requires, steps, vector_based=True):
        super(SynType, self).__init__(requires=requires, steps=steps, name=name, vector_based=vector_based, type_=_SYN_TYPE)


class SynConn(BaseEnsemble):
    """Synaptic connections.

    """

    def __init__(self, create_func, delay=0., pre_group=None, post_group=None, conn=None, num=None,
                 monitors=None, vars_init=None, pars_update=None, name=None):
        # name
        # ----
        if name is None:
            global _SYN_NO
            name = f'SynConn{_SYN_NO}'
            _SYN_NO += 1
        else:
            name = name

        # pre or post neuron group
        # ------------------------
        self.pre_group = pre_group
        self.post_group = post_group
        if pre_group is not None and post_group is not None:
            # check
            # ------
            assert isinstance(pre_group, NeuGroup), '"pre" must be an instance of NeuGroup.'
            assert isinstance(post_group, NeuGroup), '"post" must be an instance of NeuGroup.'
            assert conn is not None, '"conn" must be provided.'

            # connections
            # ------------
            if isinstance(conn, Connector):
                conn_res = conn(pre_group.geometry, post_group.geometry)
                pre_idx, post_idx = conn_res['i'], conn_res['j']
            elif isinstance(conn, np.ndarray):
                assert np.ndim(conn) == 2, f'"conn" must be a 2D array, not {np.ndim(conn)}D.'
                conn_shape = np.shape(conn)
                assert conn_shape[0] == pre_group.num and conn_shape[1] == post_group.num, \
                    f'The shape of "conn" must be ({pre_group.num}, {post_group.num})'
                pre_idx, post_idx = [], []
                for i in enumerate(pre_group.num):
                    idx = np.where(conn[i] > 0)[0]
                    pre_idx.extend([i * len(idx)])
                    post_idx.extend(idx)
                pre_idx = np.asarray(pre_idx, dtype=np.int_)
                post_idx = np.asarray(post_idx, dtype=np.int_)
            else:
                assert isinstance(conn, dict), '"conn" only support "dict" or a 2D "array".'
                assert 'i' in conn, '"conn" must provide "i" item.'
                assert 'j' in conn, '"conn" must provide "j" item.'
                pre_idx = np.asarray(conn['i'], dtype=np.int_)
                post_idx = np.asarray(conn['j'], dtype=np.int_)

            num = len(pre_idx)
            self.pre2syn = pre2syn(pre_idx, post_idx, pre_group.num)
            self.post2syn = post2syn(pre_idx, post_idx, post_group.num)
            self.pre_ids = pre_idx
            self.post_ids = post_idx
            self.pre = pre_group.ST
            self.post = post_group.ST

        else:
            assert num is not None, '"num" must be provided when "pre" and "post" are none.'
        assert 0 < num < 2 ** 64, 'Total synapse number "num" must be a valid number in "uint64".'

        # delay
        # -------
        if delay is None:
            delay_len = 0
        elif isinstance(delay, (int, float)):
            dt = profile.get_dt()
            delay_len = int(np.ceil(delay / dt))
        else:
            raise ValueError("NumpyBrain currently doesn't support other kinds of delay.")
        self.delay_len = delay_len  # delay length

        # initialize
        # ----------
        super(SynConn, self).__init__(create_func=create_func, name=name, num=num, pars_update=pars_update,
                                      vars_init=vars_init, monitors=monitors, cls_type=_SYN_CONN)

        # ST
        # --
        self.ST = SynState(self.vars_init)(size=self.num, delay=delay_len)

    def _merge_steps(self):
        codes_of_calls = super(SynConn, self)._merge_steps()
        codes_of_calls.append(f'{self.name}.ST._update_delay_indices()')
        return codes_of_calls

    @property
    def _keywords(self):
        return super(SynConn, self)._keywords + ['delay_len']


def post_cond_by_post2syn(syn_val, post2syn):
    num_post = len(post2syn)
    g_val = np.zeros(num_post, dtype=np.float_)
    for i in range(num_post):
        syn_idx = post2syn[i]
        g_val[i] = syn_val[syn_idx]
    return g_val


def delay_push(func):
    """Delay push."""
    func.__name__ = f'_npbrain_delay_push_{func.__name__}'
    return func


def delay_pull(func):
    """Delay pull."""
    func.__name__ = f'_npbrain_delay_pull_{func.__name__}'
    return func

