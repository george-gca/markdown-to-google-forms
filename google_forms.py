import logging


_logger = logging.getLogger(__name__)


def begin_create_form():
    _logger.debug('Creating form')
    return 'function createForm() {\n'


def end_create_form():
    _logger.debug('Form created')
    return '}'


def _concatenate_lines(lines: list[str] | tuple[str], identation_level: int = 1, identation: str = 2 * ' '):
    return '\n'.join([f'{identation * identation_level}{line}' for line in lines])


def create_form(**kwargs) -> str:
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


def create_section(**kwargs) -> str:
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


def create_title_and_description_item(**kwargs) -> str:
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


def create_short_text_item(**kwargs) -> str:
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


def create_paragraph_text_item(**kwargs) -> str:
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


def create_multiple_choice_item(**kwargs) -> str:
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


def create_checkbox_item(**kwargs) -> str:
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


def create_list_item(**kwargs) -> str:
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


def create_scale_item(**kwargs) -> str:
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


def create_date_item(**kwargs) -> str:
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


def create_time_item(**kwargs) -> str:
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


def create_date_time_item(**kwargs) -> str:
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


def create_duration_item(**kwargs) -> str:
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


def create_grid_item(**kwargs) -> str:
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


def create_checkbox_grid_item(**kwargs) -> str:
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


def move_section_to_end_of_form(title: str) -> str:
    # https://developers.google.com/apps-script/reference/forms/form#moveitemto

    lines = [f'form.moveItem(form.getItemById(sections["{title}"].getId()), form.getItems().length - 1);\n']
    # lines = [f'form.moveItem(sections["{title}"], form.getItems().length - 1);\n']

    _logger.debug(f'Moving section to end of form: {title}')

    return '\n' + _concatenate_lines(lines)
