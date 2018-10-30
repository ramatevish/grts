from setuptools import setup

setup(
    name="grts",
    version='0.1',
    py_modules=['grts'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        server=server:cli
        sensors=sensors:cli
    ''',
)
