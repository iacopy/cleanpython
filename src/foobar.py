"""
Basic script.
"""
# Standard Library
import argparse
import logging
import time

# My stuff
import download

# Configure logging
# (see https://docs.python.org/3/howto/logging-cookbook.html#logging-to-multiple-destinations)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",  # no milliseconds
    filename="myapp.log",
    filemode="a",
)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
# set a format which is simpler for console use
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger("").addHandler(console)


def main(urls: list, path: str) -> list:
    """
    Main function.
    """
    logging.debug("Starting main function")
    start_time = time.time()
    ret = [download.download(url, path) for url in urls]
    elapsed_time = time.time() - start_time
    logging.info("Downloaded %s files in %.3f seconds", len(urls), elapsed_time)
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="URLs to download")
    parser.add_argument("-p", "--path", default=".", help="Path to download to")
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    args = parser.parse_args()

    # Modify logging level based on verbosity flag
    console.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    main(args.urls, args.path)
