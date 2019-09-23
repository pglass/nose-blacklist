import setuptools

long_description = open('README.rst').read()

VERSION = '0.0.2'

setup_params = dict(
    name='nose-blacklist',
    version=VERSION,
    author='Paul Glass',
    author_email='pnglass@gmail.com',
    url='https://github.com/pglass/nose-blacklist',
    keywords='nose blacklist skip exclude',
    packages=setuptools.find_packages(),
    license='MIT',
    package_data={'': ['LICENSE']},
    package_dir={'noseblacklist': 'noseblacklist'},
    include_package_data=True,
    description='test exclusion for nose with blacklists',
    long_description=long_description,
    install_requires=[
        'nose',
        'six'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Testing',
    ],
    entry_points = {
        'nose.plugins.0.10': [
            'blacklist = noseblacklist.plugin:BlacklistPlugin',
        ]
    },
)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
