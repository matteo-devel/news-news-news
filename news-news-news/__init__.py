import pygooglenews, goose3, requests, re, html, fake_useragent, youtube_dl

NEWSPAPERS = [
        "https://www.corriere.it",
        "https://www.repubblica.it",
        "https://www.ilsole24ore.com",
        "https://www.rainews.it",
        "https://tg24.sky.it",
        "https://www.open.online",
        "https://www.rainews.it"
    ]

def _get_latest_tg1_webpage_url() -> str:
    r = requests.get("https://www.rainews.it/notiziari/tg1")
    r.raise_for_status()

    # get sign-language news section
    match = re.search(
        r'<rainews-aggregator-expandable data=\'{\"title\":\"Edizioni L.i.s.\"(.*?)</rainews-aggregator-expandable>',
        html.unescape(r.text)
    )
    if match == None:
        raise
    match = match.group(1)

    # get latest tg1 webpage url
    match = re.search(r"\/notiziari(.*?).html", match)
    if match == None:
        raise
    return "https://www.rainews.it" + match.group(0)


# get valid JSESSIONID from the server to get the m3u8 url from
def _get_JSESSIONID_value(url: str, headers: dict) -> str:
    s = requests.Session()
    s.get(url=url, headers=headers)
    cookies = s.cookies.get_dict()
    s.close()
    return cookies["JSESSIONID"]


def get_tg1_m3u8_url(url: str):
    # get escaped html of the latest tg1 webpage
    r = requests.get(url)
    r.raise_for_status()

    # search the url to get m3u8 url from
    match = re.search(
        r"<rainews-player data(.*?)</rainews-player", html.unescape(r.text)
    )
    if match == None:
        raise
    match = re.search(r"http(.*?)\"", match.group(1))
    if match == None:
        raise

    # remove trailing quote and add parameter
    url = match.group(0)[:-1] + "&output=61"

    headers = {"User-Agent": str(fake_useragent.UserAgent().chrome)}
    cookies = {"JSESSIONID": _get_JSESSIONID_value(url, headers)}

    r = requests.get(url, cookies=cookies, headers=headers)
    match = re.search(r"<!\[CDATA\[(.*?)]", r.text)
    if match == None:
        raise
    return match.group(1)


def get_tg1():
    m3u8 = get_tg1_m3u8_url(_get_latest_tg1_webpage_url())

    # https://stackoverflow.com/questions/69517841/how-to-set-youtube-dl-python-to-always-pick-1080p
    ydl_opts = {
        "outtmpl": "tg1.mp4",
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([m3u8])

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

get_tg1()
