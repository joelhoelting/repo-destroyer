from setuptools import setup

setup(
    name="RepoDestroyer",
    version="1.0",
    py_modules=['cli'],
    install_requires=[
        'Click',
        'requests',
        'rich'
    ],
    entry_points='''
        [console_scripts]
        repo_destroyer=cli:entry_point
    '''
)
