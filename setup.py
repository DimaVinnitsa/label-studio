"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import setuptools
import label_studio_withoutsignin
import sys

# python 3.9 warning
if sys.version_info[0] == 3 and sys.version_info[1] >= 9:
    print()
    print('~========================================================~')
    print('| Your python version is %i.%i and Label Studio has a      |' % (sys.version_info[0], sys.version_info[1]))
    print('| lot of installation problems with this Python version. |')
    print('| Please use Python 3.6 - 3.8 to avoid problems with     |')
    print('| your installation.                                     |')
    print('~========================================================~')
    print()

print(label_studio_withoutsignin.package_name, label_studio_withoutsignin.__version__)

# Readme
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Module dependencies
requirements, dependency_links = [], []
with open('deploy/requirements.txt') as f:
    for line in f.read().splitlines():
        if line.startswith('-e git+'):
            dependency_links.append(line.replace('-e ', ''))
        else:
            requirements.append(line)

setuptools.setup(
    name=label_studio_withoutsignin.package_name,
    version=label_studio_withoutsignin.__version__,
    author='dmytro.bershov',
    author_email="",
    description='Label Studio without sign in user access',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DimaVinnitsa/label-studio',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    dependency_links=dependency_links,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'label-studio=label_studio_withoutsignin.server:main',
        ],
    }
)
