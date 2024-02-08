from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='fastapi-request-limiter',
    packages=['request_limiter_middleware'],
    version='1.0.1',
    license='BSD',

    description='This middleware provides request limiting functionality for FastAPI applications, allowing you to control and manage the rate of incoming requests based on client IP addresses.',

    author='Armen-Jean Andreasian',
    author_email='armen_andreasian@proton.me',

    url='https://github.com/Armen-Jean-Andreasian',
    keywords=['FastAPI', 'request-limiter', 'python'],

    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: FastAPI',
        'Development Status :: 4 - Beta',
    ],

    python_requires='>=3.8',

    long_description=long_description
    ,
    long_description_content_type='text/markdown',
)
