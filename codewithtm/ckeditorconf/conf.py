# django-ckeditor settings

CKEDITOR_UPLOAD_PATH = 'uploads/'
# CKEDITOR_CONFIGS = {
#     'default': {
#         'width': 850,
#         'height': 350,
#         'filebrowserWindowWidth': 975,
#         'filebrowserWindowHeight': 550,
#     },
#     'small': {
#         'width': 850,
#         'height': 200,
#         'filebrowserWindowWidth': 975,
#         'filebrowserWindowHeight': 550,
#     },
# }

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'Custom',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        'filebrowserWindowHeight': 725,
        'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'codesnippet',
            # 'youtube',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
        'codeSnippet_theme': 'pojoaque',
    },

    'small': {
        'width': 850,
        'height': 200,
        'filebrowserWindowWidth': 975,
        'filebrowserWindowHeight': 550,
    },

    # config.codeSnippet_theme = 'pojoaque';

  #    'codewithtm': {
  #   'width': '100%',
  #   'height': 600,
  #   'toolbar': 'Custom',
  #   'extraPlugins': ','.join([
  #     'codesnippet',
  #     # 'youtube'
  #   ]),
  #   'toolbar_Custom': [
  #     [
  #       'Bold',
  #       'Italic',
  #       'Underline'
  #     ],
  #     [
  #       'Font',
  #       'FontSize',
  #       'TextColor',
  #       'BGColor'
  #     ],
  #     [
  #       'NumberedList',
  #       'BulletedList',
  #       '-',
  #       'Outdent',
  #       'Indent',
  #       '-',
  #       'JustifyLeft',
  #       'JustifyCenter',
  #       'JustifyRight',
  #       'JustifyBlock'
  #     ],
  #     [
  #       'Link',
  #       'Unlink'
  #     ],
  #     [
  #       'RemoveFormat',
  #       'Source',
  #       'CodeSnippet',
  #       'Image',
  #       'Youtube'
  #     ]
  #   ],
    
  # },
}




# CKEDITOR_CONFIGS={
 
  
# }