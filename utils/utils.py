import sys
import os
import hashlib
import pathlib
import functools


def load_plugins():
    # print(os.listdir())
    plugin_path = pathlib.Path(f"{os.getcwd()}/scraper")
    sys.path.append(str(plugin_path))
    plugins = plugin_path.glob("*.py")
    for plugin in plugins:
        if plugin.stem == "base_scraper":
            continue
        class_name = ""
        for word in plugin.stem.split("_"):
            class_name += word.capitalize()
        # module_name = "scraper." + plugin.stem
        module_name = plugin.stem
        module = __import__(module_name, fromlist=[class_name])
        instance = getattr(module, class_name)
        instance().add_to_shared_data()


def cookie_parser(cookie_str):
    if cookie_str is None:
        return {}
    cookies_dict = {}
    cookies = cookie_str.split(";")
    for cookie in cookies:
        key, value = cookie.strip().split("=", 1)
        cookies_dict[key] = value
    return cookies_dict


def listen_error(exception, on_error=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                return func(*args, **kw)
            except exception:
                if on_error is not None:
                    on_error()
                sys.exit(1)

        return wrapper

    return decorator


def string_to_md5(string):
    md5 = hashlib.md5()
    md5.update(str(string).encode("utf-8"))
    return md5.hexdigest()


def show_banner(text="ILP"):
    print(
        "\n ___ _     ____\n|_ _| |   |  _ \\\n | || |   | |_) |\n | || |___|  __/\n|___|_____|_|"
    )


def set_title(text="ILP"):
    if os.name == "nt":
        os.system("title " + text)
    elif os.name == "posix":
        sys.stdout.write("\x1b]2;" + text + "\x07")
        sys.stdout.flush()


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SharedData(metaclass=SingletonMeta):
    _shared_data = {"scrapers": {}}

    @classmethod
    def set_data(cls, key, value):
        cls._shared_data[key] = value

    @classmethod
    def get_data(cls, key):
        return cls._shared_data.get(key, None)


def create_scraper_instance(
    site_name: str, book_id: int, alias: str = None, cookies=None, debug=False
):
    load_plugins()
    shared_data = SharedData()
    scraper_dict = shared_data.get_data("scrapers")
    scraper = scraper_dict[site_name]
    scraper.set_debug(debug)
    scraper.set_id(book_id, call_back_init=scraper.__init__)
    scraper.set_cookies(cookies)
    scraper.set_logger(debug=debug)
    return scraper
