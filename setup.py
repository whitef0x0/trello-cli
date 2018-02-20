from setuptools import setup, find_packages

setup(
    name='trello-cli',
    version="0.0.1",
    description='Trello CLI',
    author='david_countable',
    url='https://github.com/whitef0x0/trello-cli',
    author_email='david@correspond.io',
    license='BSD License',
    install_requires=["py-trello", "docopt", "python-dotenv"],
    packages=find_packages(),
    entry_points={
        'console_scripts': 'trello = trello.main:main'
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License"
    ]
)
