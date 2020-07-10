from setuptools import setup

setup(
    name='nab',
    version='0.1',
    py_modules=['nab'],
    install_requires=[
        'click',
        'matplotlib',
        'pandas',
        'pymysql',
        'ua_parser',
    ],
    entry_points='''
        [console_scripts]
        nab=nab:cli
    ''',
)