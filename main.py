import argparse
import logging
from pathlib import Path

from google_forms import create_google_apps_script


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('markdown_file', type=str,
                        help='path to markdown file')
    parser.add_argument('-l', '--log_level', type=str, default='warning',
                        choices=('debug', 'info', 'warning', 'error', 'critical'),
                        help='log level')
    args = parser.parse_args()

    int_log_level = {
        'debug': logging.DEBUG,  # 10
        'info': logging.INFO,  # 20
        'warning': logging.WARNING,  # 30
        'error': logging.ERROR,  # 40
        'critical': logging.CRITICAL,  # 50
    }[args.log_level]

    logging.basicConfig(level=int_log_level)

    markdown_file_path = Path(args.markdown_file)
    markdown_file = markdown_file_path.read_text()

    print(create_google_apps_script(markdown_file))
