# :----------------------------------------------------------------------- INFO
# :[ael-architect/setup.py]
# :author        : fantomH
# :created       : 2024-08-29 08:58:35 UTC
# :updated       : 2024-08-29 08:58:41 UTC
# :description   : "Setup script for ael-architect"

from setuptools import (
    setup,
    find_packages
)

setup(
    name='ael-architect',
    version='1.0.0',
    author="Pascal Malouin",
    author_email="pascal.malouin@gmail.com",
    description="AlterEGO Linux configuration and setup utility.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alterEGO-Linux/ael-architect",
    
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'python-magic',
    ],
    entry_points={
        'console_scripts': [
            'ael-architect=ael_architect:main',
        ]
    }
)
