from setuptools import setup

setup(
    name='general_util',
    version='0.0.13',
    packages=['general_util', 'general_util.log', 'general_util.log.proto'],
    install_requires=[
        'aiohttp>=3.10.3',
        'fastapi>=0.83.0',
        'grpcio>=1.65.4',
        'grpcio-tools>=1.65.4',
        'PyYAML>=6.0.2',
        'requests>=2.32.3',
    ],
    author='wilson',
    author_email='wwilson008@gmail.com',
    description='general operator for fastapi write sql and redis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/littlebluewhite/node_object_module',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
)

