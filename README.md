# ChileScrapper

[![Pip](https://img.shields.io/pypi/v/chilescrapper)](https://pypi.org/project/chilescrapper)
[![Licence](https://img.shields.io/pypi/l/chilescrapper)](https://github.com/CamiloHernandez/chilesiente/blob/master/LICENSE)

A compact scraping library for the major newspapers of Chile

## Installation

ChileScrapper can be installed with Pip:

``pip install chilescrapper``

## Supported Newspapers
| Newspaper    | Name         |
|--------------|--------------|
| El Mercurio  | emol         |
| La Tercera   | la_tercera   |
| El Mostrador | el_mostrador |

## Usage

```
import chilescrapper

scrapper = chilescrapper.Scrapper("la_tercera")
articles = scrapper.fetch(max_n=30)

for article in articles:
    print(article.title)
```

## Licence

This library is licensed under the MIT Licence, please refer to the LICENCE file for more information.
