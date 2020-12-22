from setuptools import setup

setup(
    name="RepoDestroyer",
    version="1.0",
    py_modules=['cli'],
    install_requires=[
        'Click>=7.1.2',
        'requests>=2.25.0',
        'rich>=9.4.0'
    ],
    entry_points='''
        [console_scripts]
        repo_destroyer=cli:entry_point
    '''
)
