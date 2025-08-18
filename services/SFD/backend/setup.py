from setuptools import setup, find_packages

setup(
    name='sfd-backend',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.0',
        'djangorestframework',
        'psycopg2-binary',
        'python-decouple',
        'django-cors-headers',
        'django-redis',
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'manage = manage:main',
        ],
    },
)
