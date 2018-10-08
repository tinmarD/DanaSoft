from setuptools import setup

install_requires = ['numpy']

setup(
    name='danasoft',
    version='0.1.0',
    description='DanaSoft PyQt Interface',
    long_description='',
    author='Martin Deudon',
    author_email='martin.deudon@protonmail.com',
    url='https://github.com/tinmarD/DanaSoft',
    license='MIT',
    packages=['danasoft'],
    install_requires=install_requires,
    python_requires='>=2.7,<3.0',
    entry_points={
        'console_scripts': ['danasoft = danasoft.danasoft:main']
    }
)
