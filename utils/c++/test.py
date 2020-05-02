import ctypes

lib = ctypes.cdll.LoadLibrary(r'.\libfoo.so')
print(lib.square(4))
