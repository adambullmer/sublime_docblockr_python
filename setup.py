#!/usr/bin/env python
"""Setup Utils."""

if __name__ == '__main__':
    import logging

    from pkg_resources import Requirement
    from setuptools import setup, find_packages

    log = logging.getLogger(__name__)

    with open('requirements.txt') as f:
        REQUIREMENTS = []
        for req in f.readlines():
            req = req.strip()
            try:
                Requirement.parse(req)
            except:
                log.warning('failed to parse `{0}` from requirements.txt, skipping\n'.format(req))
                continue
            if len(req) is 0:
                continue
            REQUIREMENTS.append(req)

    setup(
        name='DocBlockr Python',
        version='1.4.0',
        description='',
        author='Adam Bullmer',
        author_email='psycodrumfreak@gmail.com',
        url='https://github.com/adambullmer/sublime_docblockr_python',
        packages=find_packages(),
        include_package_data=True,
        install_requires=REQUIREMENTS,
        zip_safe=False,
    )
