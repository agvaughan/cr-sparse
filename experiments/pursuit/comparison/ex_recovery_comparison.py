# Configure JAX to use 64-bit precision
from jax.config import config
config.update("jax_enable_x64", True)

from functools import partial

from cr.sparse.pursuit.eval import RecoveryTrialsAtFixed_M_N


evaluation = RecoveryTrialsAtFixed_M_N(
    M = 200,
    N = 1000,
    Ks = range(2, 90+1, 2),
    num_dict_trials = 25,
    num_signal_trials = 20
)

# Add solvers
from cr.sparse.pursuit import iht
from cr.sparse.pursuit import htp
from cr.sparse.pursuit import sp
from cr.sparse.pursuit import cosamp

# Iterative Hard Thresholding [also Normalized one]
iht_solve_jit = partial(iht.solve_jit, normalized=False)
niht_solve_jit = partial(iht.solve_jit, normalized=True)

evaluation.add_solver('IHT', iht_solve_jit)
evaluation.add_solver('NIHT', niht_solve_jit)

# Hard Thresholding Pursuit [also Normalized one]
htp_solve_jit = partial(htp.solve_jit, normalized=False)
nhtp_solve_jit = partial(htp.solve_jit, normalized=True)

evaluation.add_solver('HTP', htp_solve_jit)
evaluation.add_solver('NHTP', nhtp_solve_jit)

# Subspace Pursuit
evaluation.add_solver('SP', sp.solve_jit)

# Compressive Sampling Matching Pursuit
evaluation.add_solver('CoSaMP', cosamp.solve_jit)

# Run evaluation
evaluation('record_recovery_comparison.csv')
