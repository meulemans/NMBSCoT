from setuptools import setup

setup(
    name='NMBSCoT',
    version='1.0',
    packages=['NMBSCoT'],
    url='',
    license='',
    author='Sven Meuleman',
    author_email='',
    description='NMBS Cursor-on-Target Gateway',
    keywords=[
        'NMBS','Cursor on Target', 'ATAK', 'TAK', 'CoT'
    ],
    install_requires=[
        'aiohttp',
        'pytak>=3.2.0',
        'pycot>=2.5.0'
    ],
    entry_points={'console_scripts': ['nmbscot = NMBSCoT.commands:cli']}
)
