import pstats
p = pstats.Stats('profile_MC')
p.sort_stats('cumulative').print_stats(30)

#p.strip_dirs().sort_stats(-1).print_stats()
