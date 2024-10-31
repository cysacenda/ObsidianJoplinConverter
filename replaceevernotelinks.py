import os
import re

# Définir le répertoire des notes
notes_dir = r'G:\Mon Drive\_Obsidian'

# Expression régulière pour détecter les liens Evernote et extraire le titre
evernote_pattern = re.compile(r'\[(.*?)\]\(evernote://[^\)]+\)')

# Fonction pour trouver tous les fichiers de notes avec leurs titres
def get_all_note_titles():
    note_titles = {}
    for root, _, files in os.walk(notes_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Extraire le titre (première ligne commençant par `# `)
                    content = f.read()
                    title_match = re.search(r'^# (.+)', content, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1).strip()
                        note_titles[title.lower()] = file_path
    return note_titles

# Fonction pour identifier les liens Evernote dans les notes et les remplacer si possible
def replace_evernote_links():
    # Obtenir tous les titres et chemins des notes
    note_titles = get_all_note_titles()
    notes_with_evernote_links = []

    for root, _, files in os.walk(notes_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                modified = False

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Rechercher et traiter chaque lien Evernote dans le contenu
                def replace_link(match):
                    nonlocal modified
                    title = match.group(1).strip()
                    title_key = title.lower()
                    
                    # Chercher une correspondance pour le titre dans les autres notes
                    if title_key in note_titles:
                        modified = True
                        target_path = note_titles[title_key]
                        # Calculer le lien interne relatif
                        relative_path = os.path.relpath(target_path, start=os.path.dirname(file_path))
                        relative_path = relative_path.replace('\\', '/')
                        new_link = f"[{title}]({relative_path})"
                        print(f"Remplacement dans {file_path}: '{match.group(0)}' -> '{new_link}'")
                        return new_link
                    else:
                        notes_with_evernote_links.append((file_path, title))
                        return match.group(0)

                # Remplacer les liens et sauvegarder les modifications si besoin
                updated_content = evernote_pattern.sub(replace_link, content)
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"Liens Evernote remplacés dans le fichier : {file_path}")

    # Résumé des liens Evernote non remplacés
    if notes_with_evernote_links:
        print("\nLiens Evernote non remplacés (aucune correspondance trouvée) :")
        for note, title in notes_with_evernote_links:
            print(f" - Dans {note} : '{title}'")
    else:
        print("Tous les liens Evernote ont été remplacés par des liens internes.")

# Exécuter la fonction pour remplacer les liens Evernote
replace_evernote_links()
