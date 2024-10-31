import os
import re
import urllib.parse

# Définir les répertoires des ressources et des notes
resources_dir = r'G:\Mon Drive\_Obsidian\_resources'
notes_dir = r'G:\Mon Drive\_Obsidian'

# Charger tous les fichiers dans le dossier des ressources
def get_all_resources():
    return {filename for filename in os.listdir(resources_dir) if os.path.isfile(os.path.join(resources_dir, filename))}

# Fonction pour vérifier les liens vers les ressources dans les notes
def find_missing_resources_links():
    all_resources = get_all_resources()
    missing_links = []

    # Expression régulière pour détecter les liens vers les ressources
    link_pattern = re.compile(r'\[(.*?)\]\(\.\./_resources/([^)]+)\)')

    for root, _, files in os.walk(notes_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Rechercher tous les liens vers les ressources
                for match in link_pattern.findall(content):
                    label, referenced_filename = match
                    # Décoder les caractères spéciaux dans le nom de fichier (ex : %20 -> espace)
                    decoded_filename = urllib.parse.unquote(referenced_filename)
                    
                    # Vérifier si le fichier décodé existe dans les ressources
                    if decoded_filename not in all_resources:
                        missing_links.append((file_path, referenced_filename))

    # Afficher les liens vers des ressources manquantes
    if missing_links:
        print("Liens internes vers des ressources manquantes dans les notes :")
        for note, resource in missing_links:
            print(f"Dans {note}, le fichier référencé '{resource}' est manquant.")
    else:
        print("Toutes les ressources référencées dans les notes existent dans le dossier _resources.")

# Exécuter la fonction pour trouver et afficher les liens vers des ressources manquantes
find_missing_resources_links()