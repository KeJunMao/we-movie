def generate_title_html(title):
    '''
    生成一段title的html
    '''
    html = f'<h3 style="font-size: 17px; font-weight: bold; margin-left: 8px; color: #48b378;text-align: center;margin-top: 1em;margin-bottom: 10px;">{title}</h3>'
    return html


def generate_p_html(text, style=''):
    '''
    生成一段p的html
    '''
    html = f'<p style="{style}font-size: 16px; padding-bottom: 8px; margin: 0; padding-top: 1em; color: rgb(74,74,74); line-height: 1.75em;">{text}</p>'
    return html


def generate_indent_p_html(text):
    return generate_p_html(text, 'text-indent: 2em;')


def generate_image_html(image, title):
    html = f'<img src="{image}" alt="{title}">'
    return generate_p_html(html, 'text-align: center;')


def generate_info_html(info):
    html = f'<p style="font-size: 12px; text-align: center;padding-bottom: 8px;margin: 0;"><i>{info}</i></p>'
    return html


def generate_blockquote_html(text):
    html = f'<blockquote class="multiquote-1" data-tool="mdnice编辑器" style="border: none; font-size: 0.9em; overflow: auto; overflow-scrolling: touch; background: rgba(0, 0, 0, 0.05); color: #6a737d; padding-top: 10px; padding-bottom: 10px; padding-left: 20px; padding-right: 10px; margin-bottom: 20px; margin-top: 20px; padding: 15px 20px; line-height: 27px; background-color: #FBF9FD; border-left: 3px solid #35b378; display: block;">{text}</blockquote>'
    return html
