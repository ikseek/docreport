from distutils.core import setup
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('docstatereport/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='docstatereport',
    version=main_ns['__version__'],
    packages=['docstatereport'],
    url='https://github.com/ikseek/docreport',
    license='',
    author='Igor Kozyrenko',
    author_email='igor@unity3d.com',
    description='',
    entry_points={
        'console_scripts': [
            'docstatereport = docstatereport.cli:main',
    ]},
)
