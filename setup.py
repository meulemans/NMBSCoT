from setuptools import setup

setup(
    name='NMBSCoT',
    version='1.0',
    packages=['nmbscot'],
    url='',
    license='',
    author='Sven Meuleman',
    author_email='',
    description='NMBS Cursor-on-Target Gateway',
    keywords=[
        'NMBS','Cursor on Target', 'ATAK', 'TAK', 'CoT'
    ],
    entry_points={'console_scripts': ['nmbscot = nmbscot.commands:cli']}
)
