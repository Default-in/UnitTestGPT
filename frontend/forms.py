from django import forms

from frontend.constants import PYTHON, JAVASCRIPT, JAVA, PHP, RUST, GO


class CodeInputForm(forms.Form):
    action = forms.ChoiceField(label='Action',
                               choices=[
                                   ('translate', 'Translate'),
                                   ('unit test', 'Unit Test')
                               ], required=True)
    initial_language = forms.ChoiceField(label='Select langauge the code is written in',
                                         choices=[
                                             ('python', PYTHON),
                                             ('Javascript', JAVASCRIPT),
                                             ('Java', JAVA),
                                             ('PHP', PHP),
                                             ('Rust', RUST),
                                             ('Go', GO)
                                         ],
                                         required=True)
    input_code = forms.CharField(label='Enter Code', widget=forms.Textarea(attrs={'rows': 50, 'cols': 50}),
                                 required=True)
    target_language = forms.ChoiceField(label='Select langauge to translate to',
                                        choices=[
                                            ('python', PYTHON),
                                            ('Javascript', JAVASCRIPT),
                                            ('Java', JAVA),
                                            ('PHP', PHP),
                                            ('Rust', RUST),
                                            ('Go', GO)
                                        ])
    # the following field will depend on the initial language, choices will be populated based on the initial language
