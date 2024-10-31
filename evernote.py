import os
import re

# Définir le répertoire des notes
notes_dir = r'G:\Mon Drive\_Obsidian'

# Expression régulière pour détecter les liens Evernote
evernote_pattern = re.compile(r'evernote:///view/\S+')

# Fonction pour identifier toutes les notes contenant des liens Evernote
def find_evernote_links():
    notes_with_evernote_links = []

    for root, _, files in os.walk(notes_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Rechercher les liens Evernote dans le contenu
                    if evernote_pattern.search(content):
                        notes_with_evernote_links.append(file_path)
                        print(f"Lien Evernote trouvé dans : {file_path}")

    # Résumé
    if notes_with_evernote_links:
        print("\nRésumé :")
        for note in notes_with_evernote_links:
            print(f" - {note}")
    else:
        print("Aucun lien Evernote trouvé dans les notes.")

# Exécuter la fonction pour identifier les liens Evernote
find_evernote_links()
