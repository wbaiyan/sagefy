from models.card import Card
from modules.validations import is_required, is_string, is_url, \
    has_max_length, is_list, is_integer


class EmbedCard(Card):
    schema = dict(Card.schema.copy(), **{
        'url': {
            'validate': (is_required, is_string, is_url),
        },
        'rubric': {
            'validate': (is_required, is_list, (has_max_length, 5)),
            'embed_many': {
                'body': {
                    'validate': (is_required, is_string,),
                },
                'value': {
                    'validate': (is_required, is_integer,),
                    'default': 1,
                },
                'body_none': {  # Incomplete  (0%)
                    'validate': (is_required, is_string,),
                },
                'body_half': {  # Needs Work  (50%)
                    'validate': (is_required, is_string,),
                },
                'body_full': {  # Good  (100%)
                    'validate': (is_required, is_string,),
                },
            },
        },
    })

    def __init__(self, fields=None):
        """
        Create a new embed card instance.
        """

        super().__init__(fields)
        self['kind'] = 'embed'

    def validate_response(self, response):
        """
        TODO-3 Ensure the given response body is valid,
        given the card information.
        """

        return []
