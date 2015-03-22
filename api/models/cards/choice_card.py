from models.card import Card
from modules.validations import is_required, is_string, is_list, \
    is_one_of, is_boolean, is_integer
from modules.content import get as c


def has_correct_options(options):
    """
    Ensure the list of options has at least one correct option.
    """

    has_correct = False

    for option in options:
        if option.get('correct') is True:
            has_correct = True

    if not has_correct:
        return c('card', 'error_need_correct')


class ChoiceCard(Card):
    schema = dict(Card.schema.copy(), **{
        'body': {  # Question field
            'validate': (is_required, is_string,),
        },
        'options': {  # Available answers
            'validate': (is_required, is_list,),
            'embed_many': {
                'value': {
                    'validate': (is_required, is_string,),
                },
                'correct': {
                    'validate': (is_required, is_boolean,),
                    'access': ('view',),
                },
                'feedback': {
                    'validate': (is_required, is_string,),
                    'access': ('view',),
                },
            }
        },
        'order': {
            'validate': (is_string, (is_one_of, 'random', 'set')),
            'default': 'random',
            'access': ('view',),
        },
        'max_options_to_show': {
            'validate': (is_integer,),
            'default': 4,
            'access': ('view',),
        }
    })

    def __init__(self, fields=None):
        """
        Create a new choice card instance.
        """

        super().__init__(fields)
        self['kind'] = 'choice'

    # TODO@ validate has_correct_options

    # TODO@ When listing options to learner,
    #       make sure there is at least one correct option

    def validate_response(self, body):
        """
        TODO@ Ensure the given response body is valid,
        given the card information.
        """

        return []

    def score_response(self, response):
        """
        TODO@ Score the given response.
        Returns the score and feedback.
        """

        return 1, ''
