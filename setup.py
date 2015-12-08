from distutils.core import setup

setup(
    name='docstatereport',
    version='0.1',
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
