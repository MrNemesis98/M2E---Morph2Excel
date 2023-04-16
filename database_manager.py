import os
import urllib.request


def get_database_status():
    # returned stati:
    # 0 = database available and up to date (no options, except deleting database)
    # 1 = database not up to date (-> option: update)
    # 2 = database not available (-> option: download)

    if not os.path.exists("data"):
        os.makedirs("data")
        return 2

    else:
        if not os.path.exists("data/wiki_morph.json"):
            return 2
        else:
            local_size = os.path.getsize("data/wiki_morph.json")
            url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
            access = urllib.request.urlopen(url)
            remote_size = int(access.headers["Content-Length"])
            if local_size != remote_size:
                return 1
            else:
                return 0


def download_database():
    url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
    urllib.request.urlretrieve(url, "data/wiki_morph.json")

