from setuptools import setup

setup(
    name='things2do',
    version='0.1',
    py_modules=['things2do'],
    install_requires=[
        'Click',
        'Tabulate'
    ],
    entry_points='''
        [console_scripts]
        things2do=things2do:cli
    '''
)