# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name = 'linkstore',
    version = '0.0.9',
    description = 'A dead-simple bookmarking CLI application',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'License :: OSI Approved :: MIT License'
    ],
    keywords = 'link hyperlink store storage',
    author = u'Ángel Sanz',
    author_email = 'angelsanzgit@gmail.com',
    url = 'https://github.com/angelsanz/linkstore',
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        requirement.strip() for requirement in open('requirements.txt').readlines()
    ],
    entry_points = {
        'console_scripts': [
            'linkstore = linkstore.cli:linkstore_cli'
        ]
    }
)
