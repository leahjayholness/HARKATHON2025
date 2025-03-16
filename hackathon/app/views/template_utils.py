from flask import render_template

def render_with_context(template_name, **context):
    """
    Wrapper around Flask's render_template to add common context variables.
    """
    default_context = {"app_name": "My Flask App"}
    default_context.update(context)
    return render_template(template_name, **default_context)