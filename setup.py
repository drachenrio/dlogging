# encoding: utf-8
from setuptools import setup

setup(
    name="dlogging",
    description="Dynamic logging",
    version="0.5",
    long_description='\n\n'.join(
        open(f, 'rb').read().decode('utf-8')
        for f in ['README.rst', 'LICENSE.txt']),
    author="Axariosu",
    author_email="axariosu@gmail.com",
    url="https://github.com/drachenrio/dlogging",
    download_url='https://github.com/drachenrio/dlogging',
    license='MIT',
    packages=['dlogging'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English',
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[],
    python_requires='>=3.6',
    extras_require={
        "dev": [
            "pytest>=5.0",
        ],
    },
)
