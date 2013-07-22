import os
import re

from setuptools import setup


version = None
with open(os.path.join(os.path.dirname(__file__),
          'django_paranoia/__init__.py')) as f:
    for line in f.readlines():
        m = re.search("__version__\s*=\s*(.*)", line)
        if m:
            version = m.group(1).strip()[1:-1] # quotes
            break
assert version, 'Could not find __version__ in __init__.py'


setup(
    name='django-paranoia',
    version=version,
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
