import os

from setuptools import find_packages, setup

packages = find_packages()

setup(
    name='sample',
    version='1.0.0',
    description=__doc__,
    long_description='Sample app',
    keywords='Sample app',
    license='MIT',
    author='Mirek Simek',
    author_email='miroslav.simek@vscht.cz',
    url='https://github.com/oarepo/invenio-records-draft',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_config.module': [
            'sample = config',
        ],
        'invenio_jsonschemas.schemas': [
            'sample = sample.jsonschemas'
        ],
        'invenio_search.mappings': [
            'sample = sample.mappings',
        ],
        'invenio_base.api_apps': [
            'sample = sample.ext:SampleExt',
            'oarepo_actions = oarepo_actions:Actions'
        ],
        'invenio_base.apps': [
            'sample = sample.ext:SampleExt',
            'oarepo_actions = oarepo_actions:Actions'
        ]
        # 'invenio_pidstore.fetchers': [
        #     'recid = sample.fetchers:sample_pid_fetcher'
        # ],
        # 'invenio_pidstore.minters': [
        #     'recid = sample.minters:sample_pid_minter'
        # ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
    ],
)
