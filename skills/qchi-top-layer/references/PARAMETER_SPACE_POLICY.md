# PARAMETER_SPACE_POLICY

- Define full parameter set with units/ranges/constraints.
- Classify regions: allowed / numerically unstable / unphysical.
- Run coarse-to-fine sweeps.
- Save run manifest: params, seeds, solver version, script hash.
- Output required analyses:
  - sensitivity ranking
  - boundary/crossover detection (if applicable)
  - approximation-failure regions
