#!/usr/bin/env python
from distutils.core import setup
import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='pd-sprintstats',
      version='1.11',
      description='Gathers some statistics for a sprint from JIRA',
      author='Jason Diller',
      author_email='jdiller@pagerduty.com',
      url='',
      install_requires=required,
      scripts=['sprintstats'],
)
