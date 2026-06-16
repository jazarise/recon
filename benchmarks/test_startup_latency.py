import timeit

def benchmark_startup():
    # Simulate loading core configurations
    pass

if __name__ == '__main__':
    t = timeit.timeit("benchmark_startup()", setup="from __main__ import benchmark_startup", number=100)
    print(f"Average Startup Overhead: {t/100:.4f} seconds")