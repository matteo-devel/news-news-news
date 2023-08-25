#! /usr/bin/python3
import pygooglenews, goose3, requests, re, curses, html

NEWSPAPERS = [
        "https://www.corriere.it",
        "https://www.repubblica.it",
        "https://www.ilsole24ore.com",
        "https://www.rainews.it",
        "https://tg24.sky.it",
        "https://www.open.online",
        "https://www.rainews.it"
        ]

# return the link to download the last sign-language video news
def get_tg1_opening_download_url():

    r = requests.get("https://www.rainews.it/notiziari/tg1")

    # get sign-language news section
    match = re.search(r"<rainews-aggregator-expandable data=\'{&quot;title&quot;:&quot;Edizioni L.i.s.&quot;(.*?)</rainews-aggregator-expandable>", r.text)
    if match == None: raise
    match = match.group(1)

    # get last news webpage url
    match = re.search(r"\/notiziari(.*?).html", match)
    if match == None: raise

    requests.get("https://www.rainews.it" + match.group(0))

    # search the url to download the video from
    match = re.search(r"http:\/\/mediapolisvod(.*?)&quot;", r.text)
    if match == None: raise

    # unescape the match, remove trailing quote and add parameter
    url = html.unescape(match.group(0))[:-1] + "&output=61"
    print(url)

    cookies = {'JSESSIONID' : 'ZjUur+3RP8e7N3SDEVFDbkLu',}
    r = requests.get(url, cookies=cookies)
    print(r.text)
def get_tg1_opening():
    pass

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

get_tg1_opening_download_url()
#get_news()
