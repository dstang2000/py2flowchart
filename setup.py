import setuptools


def main():
  with open('README.md', 'r', encoding="utf-8") as fp:
    readme = fp.read()

  setuptools.setup(
    name='py2flowchart',
    version='0.0.1',
    description='Generates flowchart from Python functions.',
    long_description=readme,
	long_description_content_type="text/markdown",
    url='https://github.com/dstang2000/py2flowchart',
    author='Tang Dashi',
    author_email='dstang2000@263.net',
    license='MIT',
    classifiers=[
        'Framework :: IPython',
        'Framework :: Jupyter',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Text Processing :: Markup',
    ],
    keywords='python flow flowchart',
    packages=['py2flowchart'],
    install_requires=[
        'dill>=0.3.2',
    ],
    python_requires='>=3.6',
  )


main()
