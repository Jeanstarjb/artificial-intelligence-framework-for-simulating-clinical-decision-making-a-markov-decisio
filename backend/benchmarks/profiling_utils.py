import cProfile
import pstats
import io
from pstats import SortKey
from memory_profiler import profile

class PerformanceProfiler:
    def __init__(self):
        self.profiler = cProfile.Profile()
    
    def profile_function(self, func, *args, **kwargs):
        self.profiler.enable()
        result = func(*args, **kwargs)
        self.profiler.disable()
        return result
    
    def get_stats(self, sort_key=SortKey.CUMULATIVE):
        s = io.StringIO()
        ps = pstats.Stats(self.profiler, stream=s).sort_stats(sort_key)
        ps.print_stats()
        return s.getvalue()

    @staticmethod
    @profile
    def memory_profile(func, *args, **kwargs):
        return func(*args, **kwargs)