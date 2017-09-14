from setuptools import setup, find_packages

setup(
    name='tebless',
    packages=find_packages(),
    version='1.0.3',
    description='This library is a collection of widgets that supported from blessed',
    author='Michel Betancourt',
    author_email='MichelBetancourt23@gmail.com',
    license='MIT',
    url='https://github.com/Akhail/Tebless',
    download_url='https://github.com/Akhail/Tebless/tarball/1.0',
    keywords='cli python widgets',
    install_requires=['blessed==1.14.2'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ]
)