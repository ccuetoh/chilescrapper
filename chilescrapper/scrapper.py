from chilescrapper import sources


class Scrapper:
    source = None

    def __init__(self, source=None, user_agent=None):
        try:
            self.source = sources.Source(source)
        except ValueError:
            print("Error while starting scrapper: No such source")

        if user_agent:
            self.source.user_agent = user_agent

    def fetch(self, max_n=50):
        urls = self.source.get_article_urls()

        parsed = 0
        articles = []
        for url in urls:
            if parsed >= max_n:
                break

            article = self.source.parse_article(url)

            if article:
                parsed += 1
                articles.append(article)

        return articles
