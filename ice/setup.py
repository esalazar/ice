from setuptools import setup, find_packages
setup(
    name = "ICE",
    version = "0.1",
    packages = find_packages(),
    # Project uses lxml and slimit
    install_requires = ['lxml', 'slimit'],
    author = "Ryan Lopopolo, Edgar Salazar, William Ung",
    author_email = "rjl@hyperbo.la, esalazar@mit.edu, willcu@mit.edu",
    descriprion = "ICE is used to wrap chrome extensions in order to limit their permissions",
    url = "https://github.com/lopopolo/ice",
    entry_points = {
        'console_scripts' : [
            'ice = ice.converse:main',
        ]
    }
)

