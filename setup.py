from setuptools import setup, find_packages

setup(
    name="bacon",
    version="0.2.3",
    packages=find_packages(),
    package_data={
        'bacon': ['samples/*'],
    },
    entry_points={
        'console_scripts': [
            'bacon = bacon.bacon:main',
        ]
    },
    author="Brett Pemberton",
    author_email="brett@pemberton.at",
    maintainer="Brett Pemberton",
    maintainer_email="brett@pemberton.at",
    description="Simple OS configuration management",
    license="GPL3",
    url="https://brettpemberton.xyz/bacon",
    test_suite="bacon.test.test_bacon",
)
