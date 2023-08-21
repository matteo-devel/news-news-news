#! /usr/bin/python3
import pygooglenews, goose3, requests, re, curses

NEWSPAPERS = [
        "https://www.corriere.it",
        "https://www.repubblica.it",
        "https://www.ilsole24ore.com",
        "https://www.rainews.it",
        "https://tg24.sky.it",
        "https://www.open.online",
        "https://www.rainews.it"
        ]

def get_tg1_opening():
    s = requests.Session()
    r = s.get("https://www.rainews.it/notiziari/tg1")

    sign_language_news_aggregator = ""
    match = re.search(r"<rainews-aggregator-expandable data=\'{&quot;title&quot;:&quot;Edizioni L.i.s.&quot;(.*?)</rainews-aggregator-expandable>", r.text)
    if match != None: sign_language_news_aggregator = match.group(1)
    else: raise # TODO

    match = re.search(r"<rainews-aggregator-expandable data=\'{&quot;title&quot;:&quot;Edizioni L.i.s.&quot;(.*?)</rainews-aggregator-expandable>", r.text)
    if match != None: s.get(url = "https://www.rainews.it" + match.group(1))
    else: raise

    print(r.text)

def get_news(newspapers = NEWSPAPERS):
    gn = pygooglenews.GoogleNews(lang = "it", country = "IT")
    article_extractor = goose3.Goose()

    filtered_entries = [ entry for entry in gn.top_news()["entries"] if entry.source.href in newspapers]
    for entry in filtered_entries:

        resolved_link = requests.head(url = entry.link, cookies = {'CONSENT' : 'YES+'}, allow_redirects=True).url #https://stackoverflow.com/questions/70560247/bypassing-eu-consent-request
        article = article_extractor.extract(url = resolved_link)

        print({
            "title": entry.title,
            "published": entry.published,
            "sourceLink": entry.source.href,
            "sourceName": entry.source.title,
            "articleLink": resolved_link,
            "text": article.cleaned_text,
            "summary": article.meta_description
            })
        input()

get_tg1_opening()
#get_news()
