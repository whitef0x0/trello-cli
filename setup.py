from setuptools import setup, find_packages

setup(
    name='trello-cli',
    version="0.1.1",
    description='Trello CLI',
    author='David Baldwynn',
    url='https://github.com/whitef0x0/trello-cli',
    author_email='david@countable.ca',
    license='BSD License',
    install_requires=["py-trello", "docopt", "python-dotenv"],
    packages=['trello_cli'],
    entry_points={
        'console_scripts': 'trello = trello_cli.start:main'
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License"
    ]
)
