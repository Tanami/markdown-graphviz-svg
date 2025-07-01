import os
import sys
from setuptools import setup, find_packages

VERSION = '1.1'

if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(VERSION))
    print("  git push --tags")
    sys.exit()

setup(
    name="markdown_graphviz_svg",
    version=VERSION,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=['Markdown>=2.3.1'],
    author="Tanami Muller",
    author_email="weitzeug@gmail.com",
    description="Embeds Graphviz's SVG output into Markdown.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/Tanami/markdown-graphviz-svg",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)