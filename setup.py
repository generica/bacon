from setuptools import setup, find_packages

setup(
    name='bacon',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'bacon = bacon.bacon',
        ]
    },
    url="https://brettpemberton.xyz/bacon",
    maintainer="Brett Pemberton",
    maintainer_email="brett@pemberton.at",
    test_suite="test",
)
