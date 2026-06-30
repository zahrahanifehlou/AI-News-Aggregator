"""CLI entrypoint: run the pipeline and email the digest."""

import logging

from app.services.pipeline import process_news, send_newsletter


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    articles = process_news()
    send_newsletter(articles)


if __name__ == "__main__":
    main()
