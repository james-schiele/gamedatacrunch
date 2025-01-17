import json

from gamedatacrunch.config.topgames.download import download
from gamedatacrunch.utils import get_data_folder, get_cached_database_filename
from config.topgames.test_pull_for_released_filter import test_url_page


def load(file_name=None, url=test_url_page):
    if file_name is None:
        file_name = get_data_folder() + get_cached_database_filename()

    try:
        with open(file_name, "r", encoding="utf8") as f:
            data = json.load(f)

    except FileNotFoundError:
        data = download(url=test_url_page)

        with open(file_name, "w", encoding="utf8") as f:
            json.dump(data, f)

    del data["cached"]

    return data


def load_app_ids(file_name=None, url=test_url_page, verbose=True):
    data = load(file_name=file_name, url=url)

    app_ids = [int(app["i"]) for app_batch in data.values() for app in app_batch]

    app_ids = sorted(app_ids, key=int)

    if verbose:
        print("#appIDs = {}".format(len(app_ids)))

    return app_ids


if __name__ == "__main__":
    data = load()
    app_ids = load_app_ids()
