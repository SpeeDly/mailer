from django.utils.module_loading import import_string

from mailer import settings


def get_connections():
    '''
     evaluationg the imported strings from the settings file
     describing the available email engines
    '''
    services = []
    for engine in settings.EMAIL_ENGINES:
        services.append(import_string(engine))
    return services

def parse_to_html(message):
    ''' Convert email-from style tags in html '''
    tags_convention = [
        ["[strong]", "<strong>"],
        ["[/strong]", "</strong>"],
        ["[i]", "<i>"],
        ["[/i]", "</i>"],
        ["[u]", "<u>"],
        ["[/u]", "</u>"],
        ["[font ", "<font "],
        ["[/font]", "</font>"],
    ]

    for rules in tags_convention:
        message = message.replace(rules[0], rules[1])

    message = message.replace("']", "'>")
    return message

def get_object_or_None(klass, *args, **kwargs):
    ''' return object if it exist, otherwise - None '''
    try:
        return klass._default_manager.get(*args, **kwargs)
    except klass.DoesNotExist:
        return None
