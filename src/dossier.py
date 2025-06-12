#for single compound search 
#doc
#txt file

def generate_dossier(name, ids_dict, synonyms):
    lines = [
        f"🧪 Compound Dossier",
        f"{'=' * 30}",
        f"Name: {name}",
        f"Synonyms: {synonyms or 'Unavailable'}\n",
        f"📛 Identifiers:"
    ]
    for db, val in ids_dict.items():
        lines.append(f" - {db}: {val or 'Unavailable'}")

    lines.append("\n🔎 Source: Comp_Srch CLI")
    lines.append("=" * 30)
    return "\n".join(lines)
