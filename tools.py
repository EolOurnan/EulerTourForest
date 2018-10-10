import pstats
import cProfile


def profile_shit(sf):
    cProfile.run(str(sf),
                 'profiling_stats')
    print("# CProfile PROFILING #")
    p = pstats.Stats("profiling_stats")
    p.sort_stats('cumulative').print_stats(60)