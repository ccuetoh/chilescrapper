from distutils.core import setup

setup(
    name='chilescrapper',
    packages=['chilescrapper'],
    version='0.1.1',
    license='MIT',
    description='Compact scraping library for the major newspapers of Chile',
    author='Camilo Hernández',
    author_email='camilohernandezcueto@gmail.com',
    url='https://www.camiloh.com',
    download_url='https://github.com/CamiloHernandez/chilescrapper/archive/v0.1.tar.gz',
    keywords=['Scrapper', 'Chile', 'Data Mining', 'Newspaper'],
    install_requires=[
        'urllib3',
        'beautifulsoup4',
        'PyYAML',
        'python-dateutil'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
