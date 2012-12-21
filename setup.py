from setuptools import setup


setup(
    name='django-paranoia',
    version='0.1.6',
    description='OWASP detection point reporting for Django',
    long_description=open('README.rst').read(),
    author='Andy McKay',
    author_email='andym@mozilla.com',
    license='BSD',
    install_requires=['Django'],
    packages=['django_paranoia',
              'django_paranoia/reporters'],
    url='https://github.com/andymckay/django-paranoia',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django'
    ]
)
