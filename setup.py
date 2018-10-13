from setuptools import setup, find_packages


with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='foosball',
    author='Chad Lung',
    author_email='chad.lung@gmail.com',
    version='1.0.0',
    description='Foosball API Service',
    long_description=readme,
    license='MIT',
    url='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Review',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    tests_require=[
        'coverage==4.5.1'
        'nose==1.3.7'
        'pep8==1.7.1'
        'pylint==2.1.1'
        'testtools==2.3.0'
        'tox==3.5.2'
    ],
    install_requires=[
        'falcon==1.4.1',
        'jsonschema==2.6.0'
    ],
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'foosball = foosball.__main__:main'
        ],
    },
)
