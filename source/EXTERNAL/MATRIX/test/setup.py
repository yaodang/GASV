from numpy.distutils.core import Extension, setup

extension = Extension(
    name='matrix_fort',
    sources=['matrix_inverse.f90'],
    extra_f90_compile_args=['-O3', '-ffast-math'],
    libraries=['lapack', 'blas']
)

setup(
    name='matrix_fort',
    ext_modules=[extension]
)

