from schemadict import schemadict

schema_aktion = schemadict(
    {
        'id': {'type': int, 'required': True},
        'beschreibung': {'type': str, 'required': True},
    }
)
