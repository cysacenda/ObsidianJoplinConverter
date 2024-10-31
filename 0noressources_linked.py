import os
import re

# Définir les répertoires des ressources et des notes
resources_dir = r'G:\Mon Drive\_Obsidian\_resources'
notes_dir = r'G:\Mon Drive\_Obsidian'

# Fonction pour récupérer tous les fichiers dans le dossier des ressources
def get_all_resources():
    resources = set()
    for filename in os.listdir(resources_dir):
        file_path = os.path.join(resources_dir, filename)
        if os.path.isfile(file_path):
            resources.add(filename)
    return resources

# Fonction pour lister tous les liens vers les ressources dans les notes
def find_missing_resources_links():
    all_resources = get_all_resources()
    missing_links = []

    link_pattern = re.compile(r'\[(.*?)\]\(\.\./_resources/([^)]+)\)')

    for root, _, files in os.walk(notes_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Rechercher tous les liens vers les ressources et vérifier leur existence
                for match in link_pattern.findall(content):
                    resource_filename = match[1]  # Le nom du fichier référencé dans le lien
                    if resource_filename not in all_resources:
                        missing_links.append((file_path, resource_filename))

    # Afficher les liens manquants
    if missing_links:
        print("Liens internes vers des ressources manquantes dans les notes :")
        for note, resource in missing_links:
            print(f"Dans {note}, le fichier référencé '{resource}' est manquant.")
    else:
        print("Toutes les ressources référencées dans les notes existent dans le dossier _resources.")

# Exécuter la fonction pour trouver et afficher les liens vers des ressources manquantes
find_missing_resources_links()
