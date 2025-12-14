def normalizar_telefono(telefono: str) -> str:
    if not telefono:
        return ""

    solo_digitos = "".join(c for c in telefono if c.isdigit())

    if len(solo_digitos) >= 9:
        return solo_digitos[-9:]

    return solo_digitos
