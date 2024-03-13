import argparse
import logging
import re
from pathlib import Path
from typing import Any

from google_forms import begin_create_form, create_checkbox_grid_item, create_checkbox_item, create_date_item, create_date_time_item, create_duration_item, create_form, \
    create_grid_item, create_list_item, create_multiple_choice_item, create_paragraph_text_item, create_scale_item, create_section, create_short_text_item, create_time_item, \
    create_title_and_description_item, edit_section, end_create_form, move_section_to_end_of_form


_logger = logging.getLogger(__name__)


def _reset_args(args: dict[str, Any]) -> None:
    args['title'] = ''
    args['description'] = ''
    args['required'] = False
    args['choices'] = []
    args['rows'] = []
    args['columns'] = []


def main(markdown_file: Path) -> None:
    main_title_regex = re.compile(r'^#[\s]*(.*)$')
    confirmation_message_regex = re.compile(r'^_(.*)_$')
    section_regex = re.compile(r'^##[\s]*(.*)$')
    title_regex = re.compile(r'^###[\s]*(.*)$')
    combobox_regex = re.compile(r'^-[\s]*(.*)$')
    radio_button_regex = re.compile(r'^\*[\s]*(.*)$')
    checkbox_regex = re.compile(r'^([-*][\s]*)?\[[\s]*\] (.*)$')
    navigation_regex = re.compile(r'^(.*) \[(.*)\]$')
    paragraph_regex = re.compile(r'^[\s]*```(.|\s)*```[\s]*$')
    short_text_regex = re.compile(r'^`(.*)`$')
    required_regex = re.compile(r'^\*\*(.*)\*\*$')
    scale_regex = re.compile(r'^(.*) (\d)+ --- (\d)+ (.*)$')
    date_regex = re.compile(r'^dd|[\d]{2}/mm|[\d]{2}/yyyy|[\d]{4}$')
    time_regex = re.compile(r'^hh|[\d]{2}:mm|[\d]{2}$')
    date_time_regex = re.compile(r'^dd|[\d]{2}/mm|[\d]{2}/yyyy|[\d]{4} hh|[\d]{2}:mm|[\d]{2}$')
    duration_regex = re.compile(r'^hh|[\d]{2}:mm|[\d]{2}:ss|[\d]{2}$')
    column_row_radio_button_grid_regex = re.compile(r'^####[\s]*(.*)$')
    column_row_checkbox_grid_regex = re.compile(r'^####[\s]*\[[\s]*\] (.*)$')


    current_function = None
    grid = False
    code = begin_create_form()
    created_main_title = False
    created_first_item = False

    row = False

    args = {
        'title': '',
        'confirmation_message': '',
        'description': '',
        'required': False,
        'choices': [],
        'rows': [],
        'columns': [],
        'min': -1,
        'max': -1,
        'min_label': '',
        'max_label': '',
    }

    for i, line in enumerate(markdown_file.open()):
        _logger.debug(f'Processing line {i}: {line}')
        # the order of function calls here matters
        line = line.strip()
        if len(line) == 0:
            continue

        match = column_row_checkbox_grid_regex.match(line)
        if match is not None:
            row = match.group(1).strip().lower() == 'rows'
            current_function = create_checkbox_grid_item
            grid = True
            continue

        match = column_row_radio_button_grid_regex.match(line)
        if match is not None:
            row = match.group(1).strip().lower() == 'rows'
            current_function = create_grid_item
            grid = True
            continue

        # when reaching a new title or section, create the previous item
        match = title_regex.match(line)
        if match is not None:
            if current_function is not None:
                if current_function == create_form:
                    created_main_title = True

                code += current_function(**args)
                grid = False

                if current_function == edit_section:
                    code += move_section_to_end_of_form(args['title'])

                _reset_args(args)
                current_function = None

            elif created_first_item:
                code += create_title_and_description_item(**args)
                grid = False
                _reset_args(args)

            else:
                created_first_item = True

            line = match.group(1)
            match = required_regex.match(line)
            if match is not None:
                args['required'] = True
                args['title'] = match.group(1)

            else:
                args['title'] = line
            continue

        match = section_regex.match(line)
        if match is not None:
            if current_function is not None:
                if current_function == create_form:
                    created_main_title = True

                code += current_function(**args)
                grid = False
                _reset_args(args)
                current_function = None

            elif created_first_item:
                code += create_title_and_description_item(**args)
                grid = False
                _reset_args(args)

            else:
                created_first_item = True

            args['title'] = match.group(1)
            current_function = edit_section
            continue

        match = main_title_regex.match(line)
        if match is not None:
            if created_main_title:
                raise Exception('Main title already created')

            args['title'] = match.group(1)
            current_function = create_form
            continue

        match = confirmation_message_regex.match(line)
        if match is not None:
            confirmation_message = match.group(1)
            args['confirmation_message'] = confirmation_message
            continue

        match = paragraph_regex.match(line)
        if match is not None:
            current_function = create_paragraph_text_item
            continue

        match = short_text_regex.match(line)
        if match is not None:
            current_function = create_short_text_item
            continue

        match = checkbox_regex.match(line)
        if match is not None:
            if created_first_item:
                if grid:
                    if row:
                        args['rows'].append(match.group(2))
                    else:
                        args['columns'].append(match.group(2))

                else:
                    option = match.group(2)
                    match = navigation_regex.match(option)
                    if match is not None:
                        option = match.group(1)
                        section = match.group(2)
                        args['choices'].append(f'item.createChoice("{option}", sections["{section}"])')

                    else:
                        args['choices'].append(option)

                    current_function = create_checkbox_item

            else:
                if current_function == create_form:
                    created_main_title = True
                    code += current_function(**args)
                    _reset_args(args)
                    current_function = None
                    grid = False

                code += create_section(title=match.group(2))

            continue

        match = radio_button_regex.match(line)
        if match is not None:
            if created_first_item:
                if grid:
                    if row:
                        args['rows'].append(match.group(1))
                    else:
                        args['columns'].append(match.group(1))

                else:
                    option = match.group(1)
                    match = navigation_regex.match(option)
                    if match is not None:
                        option = match.group(1)
                        section = match.group(2)
                        args['choices'].append(f'item.createChoice("{option}", sections["{section}"])')

                    else:
                        args['choices'].append(option)

                    current_function = create_multiple_choice_item

            else:
                if current_function == create_form:
                    created_main_title = True
                    code += current_function(**args)
                    _reset_args(args)
                    current_function = None
                    grid = False

                code += create_section(title=match.group(1))

            continue

        match = combobox_regex.match(line)
        if match is not None:
            if created_first_item:
                if grid:
                    if row:
                        args['rows'].append(match.group(1))
                    else:
                        args['columns'].append(match.group(1))

                else:
                    option = match.group(1)
                    match = navigation_regex.match(option)
                    if match is not None:
                        option = match.group(1)
                        section = match.group(2)
                        args['choices'].append(f'item.createChoice("{option}", sections["{section}"])')

                    else:
                        args['choices'].append(option)
                    current_function = create_list_item

            else:
                if current_function == create_form:
                    created_main_title = True
                    code += current_function(**args)
                    _reset_args(args)
                    current_function = None
                    grid = False

                code += create_section(title=match.group(1))

            continue

        match = scale_regex.match(line)
        if match is not None:
            args['min_label'] = match.group(1)
            args['min'] = match.group(2)
            args['max'] = match.group(3)
            args['max_label'] = match.group(4)
            current_function = create_scale_item
            continue

        match = date_time_regex.match(line)
        if match is not None:
            current_function = create_date_time_item
            continue

        match = date_regex.match(line)
        if match is not None:
            current_function = create_date_item
            continue

        match = duration_regex.match(line)
        if match is not None:
            current_function = create_duration_item
            continue

        match = time_regex.match(line)
        if match is not None:
            current_function = create_time_item
            continue

        args['description'] = line

    # finished reading the file, create the last item
    if current_function is not None:
        code += current_function(**args)
        _reset_args(args)
        current_function = None

    code += end_create_form()

    print(code)


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

    main(markdown_file_path)
