from schemadict import schemadict
from aktion import schema_aktion

schema_sachverhalt = schemadict(
    {
        'beteiligter': {'type': str, 'required': True},
        'fahrzeug': {'type': str, 'required': True},
        'aktionen': {
            'type': list,
            'item_type': dict,
            'required': True,
            'item_schemadict': schema_aktion,
        },
    }
)
