import datetime

import urllib.request
import dateutil.parser
import bs4

from chilescrapper.article import Article


class Source:
    article_f = None
    home_f = None

    url = ""

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36' \
                 ' (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36 '

    def __init__(self, target):
        if target == "emol":
            self.url = "https://www.emol.com"

            def parse_emol_home(soup, baseurl):
                headlines = soup.find("div", attrs={"class": "cont_736_e_2015"})
                urls = []
                for a_tag in headlines.find_all("a"):
                    url = a_tag.get("href")

                    if not url:
                        continue

                    if "/noticias/" in url:
                        url = url.replace("#comentarios", "")
                        if "emol.com" in url:
                            urls.append(url)
                        else:
                            urls.append(baseurl + url)

                return list(set(urls))

            self.home_f = parse_emol_home

            def parse_emol_article(soup, url):
                art = Article()
                art.url = url

                try:
                    body_container = soup.find("div", attrs={"id": "cuDetalle_cuTexto_textoNoticia"})
                    for extra in body_container.find_all("div", attrs={"class": "flo_left cont_items_detalle_50"}):
                        extra.decompose()

                    art.body = body_container.text
                except AttributeError:
                    # Most likely a special publication. Skip
                    return None

                try:
                    art.title = soup.find("h1", attrs={"id": "cuDetalle_cuTitular_tituloNoticia"}).text
                except AttributeError:
                    pass

                try:
                    art.subtitle = soup.find("h2", attrs={"id": "cuDetalle_cuTitular_bajadaNoticia"}).text
                except AttributeError:
                    pass

                url_blocks = url.split("/")

                try:
                    art.categories = [url_blocks[4]]
                except IndexError:
                    pass

                try:
                    art.date = datetime.date(int(url_blocks[5]), int(url_blocks[6]), int(url_blocks[7]))
                except IndexError:
                    pass

                return art

            self.article_f = parse_emol_article

        elif target == "la_tercera":
            self.url = "https://www.latercera.com"

            def parse_la_tercera_home(soup, baseurl):
                headlines = soup.find_all("div", attrs={"class": "headline | width_full"})

                links = []
                for headline in headlines:
                    link = headline.find("a").get("href")
                    if "www" in link:
                        continue

                    links.append(baseurl + link)

                return links

            self.home_f = parse_la_tercera_home

            def parse_la_tercera_article(soup, url):
                art = Article()
                art.url = url

                art.body = " ".join([paragraph.text for paragraph in soup.find_all("p", attrs={"class": "paragraph"})])
                if art.body == "":
                    # Most likely a special publication. Skip
                    return None

                try:
                    art.title = soup.find("h1").text
                except AttributeError:
                    pass

                try:
                    art.subtitle = soup.find("p", attrs={"class": "excerpt"}).text
                except AttributeError:
                    pass

                try:
                    art.categories = [cat.text for cat in soup.find("ul", attrs={"class": "list-cat-y-tags"}).contents]
                except AttributeError:
                    pass

                try:
                    date = soup.find("time", attrs={"class": "p-left-10"}).attrs["datetime"]
                    art.date = dateutil.parser.parse(date.split("(")[0])
                except AttributeError:
                    pass

                return art

            self.article_f = parse_la_tercera_article

        elif target == "el_mostrador":
            self.url = "https://www.elmostrador.cl/"

            def parse_el_mostrador_home(soup, baseurl):
                alto_impacto = soup.find("article", attrs={"class": "noticia-alto-impacto"}).find("a").get("href")

                col1 = soup.find("section", attrs={"class": "noticias-recientes"})
                col1_urls = []
                for a_tag in col1.find_all("a"):
                    url = a_tag.get("href")

                    if "https://www.elmostrador.cl/autor/" in url or url == "https://www.elmostrador.cl/destacado/":
                        continue

                    col1_urls.append(url)

                col2 = soup.find("section", attrs={"class": "noticias-destacadas noticias-dia"})
                col2_urls = []
                for a_tag in col2.find_all("a"):
                    url = a_tag.get("href")

                    if url == "https://www.elmostrador.cl/dia/":
                        continue

                    col2_urls.append(url)

                return list({alto_impacto, *col1_urls, *col2_urls})

            self.home_f = parse_el_mostrador_home

            def parse_el_mostrador_article(soup, url):
                art = Article()
                art.url = url

                try:
                    body_container = soup.find("div", attrs={"id": "noticia"})
                    for extra in body_container.find_all("section", attrs={
                        "class": "col-xs-12 col-sm-12 col-md-12 articulos-relacionados"}):
                        extra.decompose()

                    art.body = body_container.text
                except AttributeError:
                    # Most likely a special publication. Skip
                    return None

                try:
                    art.title = soup.find("h2", attrs={"class": "titulo-single"})

                    if not art.title:
                        art.title = soup.find("h2", attrs={"class": "col-xs-12 col-sm-10 col-md-10"})

                    if art.title:
                        art.title = art.title.text.strip().replace("\n", "")

                except AttributeError:
                    pass

                try:
                    art.subtitle = soup.find("figcaption").text
                except AttributeError:
                    pass

                url_blocks = url.split("/")

                try:
                    for i in range(len(url_blocks)):
                        if url_blocks[i].isnumeric():
                            art.date = datetime.date(int(url_blocks[i]), int(url_blocks[i+1]), int(url_blocks[i+2]))
                            break
                except ValueError:
                    pass

                return art

            self.article_f = parse_el_mostrador_article

    def get_article_urls(self):
        req = urllib.request.Request(
            self.url,
            data=None,
            headers={
                'User-Agent': self.user_agent
            }
        )

        html = urllib.request.urlopen(req).read()
        soup = bs4.BeautifulSoup(html, "html.parser")

        return self.home_f(soup, self.url)

    def parse_article(self, url):
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': self.user_agent
            }
        )

        html = urllib.request.urlopen(req).read()
        soup = bs4.BeautifulSoup(html, "html.parser")

        return self.article_f(soup, url)
