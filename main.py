import argparse
import re
from pathlib import Path
from typing import Any


def _begin_create_form():
    return 'function createForm() {\n'


def _end_create_form():
    return '}'


def _concatenate_lines(lines: list[str] | tuple[str], identation_level: int = 1, identation: str = 2 * ' '):
    return '\n'.join([f'{identation * identation_level}{line}' for line in lines])


def _create_form(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    confirmation_message = kwargs.get('confirmation_message', '')

    lines = [f'var form = FormApp.create("{title}")']

    if len(description) > 0:
        lines.append(f'  .setDescription("{description}")')

    if len(confirmation_message) > 0:
        lines.append(f'  .setConfirmationMessage("{confirmation_message}")')

    lines[-1] += ';\n'

    lines.append('var sections = {};\n')

    return _concatenate_lines(lines)


def _create_section(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#addpagebreakitem
    title = kwargs.get('title', '')

    lines = ['var section = form.addPageBreakItem()',
             f'  .setTitle("{title}");\n',
             f'sections["{title}"] = section;\n']

    return '\n' + _concatenate_lines(lines)


def _edit_section(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#addpagebreakitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')

    lines = [f'sections["{title}"]',
             f'  .setTitle("{title}")']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _create_short_text_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#addtextitem
    title = kwargs.get('title', '')
    required = kwargs.get('required', False)

    lines = ['form.addTextItem()',
             f'  .setTitle("{title}")']

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _create_paragraph_text_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#addparagraphtextitem
    title = kwargs.get('title', '')
    required = kwargs.get('required', False)

    lines = ['form.addParagraphTextItem()',
             f'  .setTitle("{title}")']

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _create_multiple_choice_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#addmultiplechoiceitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)
    choices = kwargs.get('choices', [])

    if any(c.startswith('item.createChoice(') for c in choices):
        lines = ['var item = form.addMultipleChoiceItem()',
                 f'  .setTitle("{title}");\n']

        lines.append('item.setChoices([')
        for choice in choices:
            lines.append(f'    {choice},')

        lines[-1] = lines[-1][:-1]
        lines.append('  ])')

    else:
        lines = ['form.addMultipleChoiceItem()',
                 f'  .setTitle("{title}")',
                 f'  .setChoiceValues({choices})']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    # TODO .showOtherOption(true);

    return '\n' + _concatenate_lines(lines)


def _create_checkbox_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#addcheckboxitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)
    choices = kwargs.get('choices', [])

    if any(c.startswith('item.createChoice(') for c in choices):
        lines = ['var item = form.addMultipleChoiceItem()',
                 f'  .setTitle("{title}");']

        lines.append('item.setChoices([')
        for choice in choices:
            lines.append(f'    {choice},')

        lines[-1] = lines[-1][:-1]
        lines.append('  ])')

    else:
        lines = ['form.addMultipleChoiceItem()',
                 f'  .setTitle("{title}")',
                 f'  .setChoiceValues({choices})']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _create_list_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#addlistitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)
    choices = kwargs.get('choices', [])

    if any(c.startswith('item.createChoice(') for c in choices):
        lines = ['var item = form.addMultipleChoiceItem()',
                 f'  .setTitle("{title}");']

        lines.append('item.setChoices([')
        for choice in choices:
            lines.append(f'    {choice},')

        lines[-1] = lines[-1][:-1]
        lines.append('  ])')

    else:
        lines = ['form.addMultipleChoiceItem()',
                 f'  .setTitle("{title}")',
                 f'  .setChoiceValues({choices})']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _create_scale_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#addscaleitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)
    min_label = kwargs.get('min_label', '')
    max_label = kwargs.get('max_label', '')
    min_value = kwargs.get('min', 0)
    max_value = kwargs.get('max', -1)

    lines = ['form.addScaleItem()',
             f'  .setTitle("{title}")',
             f'  .setBounds({min_value}, {max_value})',
             f'  .setLabels("{min_label}", "{max_label}")']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _create_date_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#adddateitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)

    lines = ['form.addDateItem()',
             f'  .setTitle("{title}")']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _create_time_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#addtimeitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)

    lines = ['form.addTimeItem()',
             f'  .setTitle("{title}")']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _create_date_time_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#adddatetimeitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)

    lines = ['form.addDateTimeItem()',
             f'  .setTitle("{title}")']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _create_duration_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#adddurationitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)

    lines = ['form.addDurationItem()',
             f'  .setTitle("{title}")']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _create_grid_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#addgriditem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)
    rows = kwargs.get('rows', [])
    columns = kwargs.get('columns', [])

    lines = ['form.addGridItem()',
             f'  .setTitle("{title}")',
             f'  .setRows({rows})',
             f'  .setColumns({columns})']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _create_checkbox_grid_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#addcheckboxgriditem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)
    rows = kwargs.get('rows', [])
    columns = kwargs.get('columns', [])

    lines = ['form.addCheckboxGridItem()',
             f'  .setTitle("{title}")',
             f'  .setRows({rows})',
             f'  .setColumns({columns})']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    if required:
        lines.append('  .setRequired(true)')

    lines[-1] += ';\n'

    return '\n' + _concatenate_lines(lines)


def _move_section_to_end_of_form(title: str) -> str:
    # https://developers.google.com/apps-script/reference/forms/form?hl=pt-br#moveitemto

    lines = [f'form.moveItem(form.getItemById(sections["{title}"].getId()), form.getItems().length - 1);\n']
    # lines = [f'form.moveItem(sections["{title}"], form.getItems().length - 1);\n']

    return '\n' + _concatenate_lines(lines)


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
    code = _begin_create_form()
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

    for line in markdown_file.open():
        # the order of function calls here matters
        line = line.strip()
        if len(line) == 0:
            continue

        match = column_row_checkbox_grid_regex.match(line)
        if match is not None:
            row = match.group(1).strip().lower() == 'rows'
            current_function = _create_checkbox_grid_item
            grid = True
            continue

        match = column_row_radio_button_grid_regex.match(line)
        if match is not None:
            row = match.group(1).strip().lower() == 'rows'
            current_function = _create_grid_item
            grid = True
            continue

        # when reaching a new title or section, create the previous item
        match = title_regex.match(line)
        if match is not None:
            if current_function is not None:
                if current_function == _create_form:
                    created_main_title = True

                code += current_function(**args)
                grid = False

                if current_function == _edit_section:
                    code += _move_section_to_end_of_form(args['title'])

                _reset_args(args)
                current_function = None

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
                if current_function == _create_form:
                    created_main_title = True

                code += current_function(**args)
                _reset_args(args)
                current_function = None
                grid = False

            else:
                created_first_item = True

            args['title'] = match.group(1)
            current_function = _edit_section
            continue

        match = main_title_regex.match(line)
        if match is not None:
            if created_main_title:
                raise Exception('Main title already created')

            args['title'] = match.group(1)
            current_function = _create_form
            continue

        match = confirmation_message_regex.match(line)
        if match is not None:
            confirmation_message = match.group(1)
            args['confirmation_message'] = confirmation_message
            continue

        match = paragraph_regex.match(line)
        if match is not None:
            current_function = _create_paragraph_text_item
            continue

        match = short_text_regex.match(line)
        if match is not None:
            current_function = _create_short_text_item
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

                    current_function = _create_checkbox_item

            else:
                if current_function == _create_form:
                    created_main_title = True
                    code += current_function(**args)
                    _reset_args(args)
                    current_function = None
                    grid = False

                code += _create_section(title=match.group(2))

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

                    current_function = _create_multiple_choice_item

            else:
                if current_function == _create_form:
                    created_main_title = True
                    code += current_function(**args)
                    _reset_args(args)
                    current_function = None
                    grid = False

                code += _create_section(title=match.group(1))

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
                    current_function = _create_list_item

            else:
                if current_function == _create_form:
                    created_main_title = True
                    code += current_function(**args)
                    _reset_args(args)
                    current_function = None
                    grid = False

                code += _create_section(title=match.group(1))

            continue

        match = scale_regex.match(line)
        if match is not None:
            args['min_label'] = match.group(1)
            args['min'] = match.group(2)
            args['max'] = match.group(3)
            args['max_label'] = match.group(4)
            current_function = _create_scale_item
            continue

        match = date_time_regex.match(line)
        if match is not None:
            current_function = _create_date_time_item
            continue

        match = date_regex.match(line)
        if match is not None:
            current_function = _create_date_item
            continue

        match = duration_regex.match(line)
        if match is not None:
            current_function = _create_duration_item
            continue

        match = time_regex.match(line)
        if match is not None:
            current_function = _create_time_item
            continue

        args['description'] = line

    # finished reading the file, create the last item
    if current_function is not None:
        code += current_function(**args)
        _reset_args(args)
        current_function = None

    code += _end_create_form()

    print(code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('markdown_file', type=str,
                        help='path to markdown file')
    args = parser.parse_args()

    markdown_file_path = Path(args.markdown_file)

    main(markdown_file_path)
