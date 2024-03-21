import logging
import re
from typing import Any


_logger = logging.getLogger(__name__)

_main_title_regex = re.compile(r'^#[\s]*(.*)$')
_confirmation_message_regex = re.compile(r'^_(.*)_$')
_section_regex = re.compile(r'^##[\s]*(.*)$')
_title_regex = re.compile(r'^###[\s]*(.*)$')
_combobox_regex = re.compile(r'^-[\s]*(.*)$')
_radio_button_regex = re.compile(r'^\*[\s]*(.*)$')
_checkbox_regex = re.compile(r'^([-*][\s]*)?\[[\s]*\] (.*)$')
_navigation_regex = re.compile(r'^(.*) \[(.*)\]$')
_paragraph_regex = re.compile(r'^[\s]*```(.|\s)*```[\s]*$')
_short_text_regex = re.compile(r'^`(.*)`$')
_required_regex = re.compile(r'^\*\*(.*)\*\*$')
_scale_regex = re.compile(r'^(.*) (\d)+ --- (\d)+ (.*)$')
_date_regex = re.compile(r'^dd|[\d]{2}/mm|[\d]{2}/yyyy|[\d]{4}$')
_time_regex = re.compile(r'^hh|[\d]{2}:mm|[\d]{2}$')
_date_time_regex = re.compile(r'^dd|[\d]{2}/mm|[\d]{2}/yyyy|[\d]{4} hh|[\d]{2}:mm|[\d]{2}$')
_duration_regex = re.compile(r'^hh|[\d]{2}:mm|[\d]{2}:ss|[\d]{2}$')
_column_row_radio_button_grid_regex = re.compile(r'^####[\s]*(.*)$')
_column_row_checkbox_grid_regex = re.compile(r'^####[\s]*\[[\s]*\] (.*)$')


def begin_create_form():
    _logger.debug('Creating form')
    return 'function createForm() {\n'


def end_create_form():
    _logger.debug('Form created')
    return '}'


def _concatenate_lines(lines: list[str] | tuple[str], identation_level: int = 1, identation: str = 2 * ' '):
    return '\n'.join([f'{identation * identation_level}{line}' for line in lines])


def _create_form(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form
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
    # https://developers.google.com/apps-script/reference/forms/form#addpagebreakitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')

    lines = ['var section = form.addPageBreakItem()',
             f'  .setTitle("{title}");\n',
             f'sections["{title}"] = section;\n']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    _logger.debug(f'Creating section: {title} - {description}')

    return '\n' + _concatenate_lines(lines)


def edit_section(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#addpagebreakitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')

    lines = [f'sections["{title}"]',
             f'  .setTitle("{title}")']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    lines[-1] += ';\n'

    _logger.debug(f'Editing section: {title} - {description}')

    return '\n' + _concatenate_lines(lines)


def _create_title_and_description_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#addsectionheaderitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')

    lines = ['form.addSectionHeaderItem()',
             f'  .setTitle("{title}")']

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    lines[-1] += ';\n'

    _logger.debug(f'Creating title and description item: {title} - {description}')

    return '\n' + _concatenate_lines(lines)


def _create_short_text_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#addtextitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)

    lines = ['form.addTextItem()',
             f'  .setTitle("{title}")']

    if required:
        lines.append('  .setRequired(true)')

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    lines[-1] += ';\n'

    _logger.debug(f'Creating short text item: {title}{" (required)" if required else ""} - {description}')

    return '\n' + _concatenate_lines(lines)


def _create_paragraph_text_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#addparagraphtextitem
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    required = kwargs.get('required', False)

    lines = ['form.addParagraphTextItem()',
             f'  .setTitle("{title}")']

    if required:
        lines.append('  .setRequired(true)')

    if len(description) > 0:
        lines.append(f'  .setHelpText("{description}")')

    lines[-1] += ';\n'

    _logger.debug(f'Creating paragraph text item: {title}{" (required)" if required else ""} - {description}')

    return '\n' + _concatenate_lines(lines)


def _create_multiple_choice_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#addmultiplechoiceitem
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

    _logger.debug(f'Creating multiple choice item: {title}{" (required)" if required else ""} - {description}\nchoices: {choices}')

    return '\n' + _concatenate_lines(lines)


def _create_checkbox_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#addcheckboxitem
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

    _logger.debug(f'Creating checkbox item: {title}{" (required)" if required else ""} - {description}\nchoices: {choices}')

    return '\n' + _concatenate_lines(lines)


def _create_list_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#addlistitem
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

    _logger.debug(f'Creating list item: {title}{" (required)" if required else ""} - {description}\nchoices: {choices}')

    return '\n' + _concatenate_lines(lines)


def _create_scale_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#addscaleitem
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

    _logger.debug(f'Creating scale item: {title}{" (required)" if required else ""} - {description}\nmin ({min_label}): {min_value} - max ({max_label}): {max_value}')

    return '\n' + _concatenate_lines(lines)


def _create_date_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#adddateitem
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

    _logger.debug(f'Creating date item: {title}{" (required)" if required else ""} - {description}')

    return '\n' + _concatenate_lines(lines)


def _create_time_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#addtimeitem
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

    _logger.debug(f'Creating time item: {title}{" (required)" if required else ""} - {description}')

    return '\n' + _concatenate_lines(lines)


def _create_date_time_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#adddatetimeitem
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

    _logger.debug(f'Creating date time item: {title}{" (required)" if required else ""} - {description}')

    return '\n' + _concatenate_lines(lines)


def _create_duration_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#adddurationitem
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

    _logger.debug(f'Creating duration item: {title}{" (required)" if required else ""} - {description}')

    return '\n' + _concatenate_lines(lines)


def _create_grid_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#addgriditem
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

    _logger.debug(f'Creating grid item: {title}{" (required)" if required else ""} - {description}\nrows: {rows}\ncolumns: {columns}')

    return '\n' + _concatenate_lines(lines)


def _create_checkbox_grid_item(**kwargs) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#addcheckboxgriditem
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

    _logger.debug(f'Creating checkbox grid item: {title}{" (required)" if required else ""} - {description}\nrows: {rows}\ncolumns: {columns}')

    return '\n' + _concatenate_lines(lines)


def _move_section_to_end_of_form(title: str) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#moveitemto

    lines = [f'form.moveItem(form.getItemById(sections["{title}"].getId()), form.getItems().length - 1);\n']
    # lines = [f'form.moveItem(sections["{title}"], form.getItems().length - 1);\n']

    _logger.debug(f'Moving section to end of form: {title}')

    return '\n' + _concatenate_lines(lines)


def _reset_args(args: dict[str, Any]) -> None:
    args['title'] = ''
    args['description'] = ''
    args['required'] = False
    args['choices'] = []
    args['rows'] = []
    args['columns'] = []


def create_google_apps_script(markdown_file: str) -> None:
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

    for i, line in enumerate(markdown_file.strip().split('\n')):
        _logger.debug(f'Processing line {i}: {line}')
        # the order of function calls here matters
        line = line.strip()
        if len(line) == 0:
            continue

        match = _column_row_checkbox_grid_regex.match(line)
        if match is not None:
            row = match.group(1).strip().lower() == 'rows'
            current_function = _create_checkbox_grid_item
            grid = True
            continue

        match = _column_row_radio_button_grid_regex.match(line)
        if match is not None:
            row = match.group(1).strip().lower() == 'rows'
            current_function = _create_grid_item
            grid = True
            continue

        # when reaching a new title or section, create the previous item
        match = _title_regex.match(line)
        if match is not None:
            if current_function is not None:
                if current_function == _create_form:
                    created_main_title = True

                code += current_function(**args)
                grid = False

                if current_function == edit_section:
                    code += _move_section_to_end_of_form(args['title'])

                _reset_args(args)
                current_function = None

            elif created_first_item:
                code += _create_title_and_description_item(**args)
                grid = False
                _reset_args(args)

            else:
                created_first_item = True

            line = match.group(1)
            match = _required_regex.match(line)
            if match is not None:
                args['required'] = True
                args['title'] = match.group(1)

            else:
                args['title'] = line
            continue

        match = _section_regex.match(line)
        if match is not None:
            if current_function is not None:
                if current_function == _create_form:
                    created_main_title = True

                code += current_function(**args)
                grid = False
                _reset_args(args)
                current_function = None

            elif created_first_item:
                code += _create_title_and_description_item(**args)
                grid = False
                _reset_args(args)

            else:
                created_first_item = True

            args['title'] = match.group(1)
            current_function = edit_section
            continue

        match = _main_title_regex.match(line)
        if match is not None:
            if created_main_title:
                raise Exception('Main title already created')

            args['title'] = match.group(1)
            current_function = _create_form
            continue

        match = _confirmation_message_regex.match(line)
        if match is not None:
            confirmation_message = match.group(1)
            args['confirmation_message'] = confirmation_message
            continue

        match = _paragraph_regex.match(line)
        if match is not None:
            current_function = _create_paragraph_text_item
            continue

        match = _short_text_regex.match(line)
        if match is not None:
            current_function = _create_short_text_item
            continue

        match = _checkbox_regex.match(line)
        if match is not None:
            if created_first_item:
                if grid:
                    if row:
                        args['rows'].append(match.group(2))
                    else:
                        args['columns'].append(match.group(2))

                else:
                    option = match.group(2)
                    match = _navigation_regex.match(option)
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

        match = _radio_button_regex.match(line)
        if match is not None:
            if created_first_item:
                if grid:
                    if row:
                        args['rows'].append(match.group(1))
                    else:
                        args['columns'].append(match.group(1))

                else:
                    option = match.group(1)
                    match = _navigation_regex.match(option)
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

        match = _combobox_regex.match(line)
        if match is not None:
            if created_first_item:
                if grid:
                    if row:
                        args['rows'].append(match.group(1))
                    else:
                        args['columns'].append(match.group(1))

                else:
                    option = match.group(1)
                    match = _navigation_regex.match(option)
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

        match = _scale_regex.match(line)
        if match is not None:
            args['min_label'] = match.group(1)
            args['min'] = match.group(2)
            args['max'] = match.group(3)
            args['max_label'] = match.group(4)
            current_function = _create_scale_item
            continue

        match = _date_time_regex.match(line)
        if match is not None:
            current_function = _create_date_time_item
            continue

        match = _date_regex.match(line)
        if match is not None:
            current_function = _create_date_item
            continue

        match = _duration_regex.match(line)
        if match is not None:
            current_function = _create_duration_item
            continue

        match = _time_regex.match(line)
        if match is not None:
            current_function = _create_time_item
            continue

        args['description'] = line

    # finished reading the file, create the last item
    if current_function is not None:
        code += current_function(**args)
        _reset_args(args)
        current_function = None

    code += end_create_form()

    return code