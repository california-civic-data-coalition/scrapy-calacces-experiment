#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='scrapy-calaccess-crawler',
    version='0.0.0',
    license='MIT',
    description='A Scrapy app to scrape campaign-finance data from '
                'the California Secretary of State’s CAL-ACCESS website',
    author='California Civic Data Coalition',
    url='https://github.com/california-civic-data-coalition/scrapy-calaccess',
    author_email='cacivicdata@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=(
        'Scrapy',
        'bs4',
        'requests'
    )
)
