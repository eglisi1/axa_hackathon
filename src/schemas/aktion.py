from schemadict import schemadict

schema_aktion = schemadict(
    {
        "id": {"type": int, "required": True},
        "beschreibung": {"type": str, "required": True},
        "artikel": {
            "type": list,
            "item_type": dict,
            "required": True
        }
        "hat_artikel_verstossen": {"type": bool, "required": False}
    }
)
