from schemadict import schemadict

schema_aktion = schemadict(
    {
        "id": {"type": int, "required": True},
        "beschreibung": {"type": str, "required": True},
        "artikel_id": {
            "type": str,
            "required": False,
        },
        "hat_artikel_verstossen": {"type": bool, "required": False},
    }
)
