from django import template
register=template.Library()

def to_lower(str):
    return str.lower()

register.filter('to_lower',to_lower)

def do_current_time(parser, token):
    try:       
        # split_contents() knows not to split quoted strings.       
        tag_name, format_string = token.split_contents()   
    except ValueError:       
        msg = '%r tag requires a single argument' % token.contents[0]       
    raise template.TemplateSyntaxError(msg)   
    return CurrentTimeNode(format_string[1:-1])