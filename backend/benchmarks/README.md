# Performance Testing Guide

## Benchmark Tests
```bash
make benchmark  # Runs all performance benchmarks
```

## Memory Profiling
```python
from profiling_utils import PerformanceProfiler
profiler = PerformanceProfiler()
profiler.memory_profile(my_function, args)
```

## Load Testing
```bash
make load-test  # Starts Locust load testing UI on http://localhost:8089
```

## Optimization Targets
1. MDP value iteration <100ms for 1000 states
2. DDN belief update <5ms per observation
3. API response <500ms under 1000 RPM