import os
import re
from difflib import get_close_matches
import urllib.parse

# Définir les répertoires des ressources et des notes
resources_dir = r'G:\Mon Drive\_Obsidian\_resources'
notes_dir = r'G:\Mon Drive\_Obsidian'

# Charger tous les fichiers dans le dossier des ressources
def get_all_resources():
    return {filename for filename in os.listdir(resources_dir) if os.path.isfile(os.path.join(resources_dir, filename))}

# Trouver le meilleur match pour un nom de fichier tronqué
def find_best_match(truncated_name, resources):
    # Chercher une correspondance exacte sur les premiers caractères dans les ressources
    potential_matches = [resource for resource in resources if resource.startswith(truncated_name)]
    if potential_matches:
        return potential_matches[0]
    
    # Utiliser une correspondance partielle avec `get_close_matches` si aucune correspondance exacte n'est trouvée
    close_matches = get_close_matches(truncated_name, resources, n=1, cutoff=0.6)
    return close_matches[0] if close_matches else None

# Fonction pour mettre à jour les liens dans les notes avec le nom correct des ressources
def update_links_with_correct_resources():
    resources = get_all_resources()
    link_pattern = re.compile(r'\[(.*?)\]\(\.\./_resources/([^)]+)\)')

    for root, _, files in os.walk(notes_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                modified = False

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Rechercher les liens vers des ressources dans le contenu
                def replace_link(match):
                    label = match.group(1)
                    referenced_filename = match.group(2)

                    # Décoder les caractères spéciaux dans le nom de fichier pour correspondance, sans modifier le lien d'origine
                    decoded_filename = urllib.parse.unquote(referenced_filename)
                    
                    # Chercher le meilleur match pour le nom décodé
                    best_match = find_best_match(decoded_filename, resources)
                    if best_match:
                        nonlocal modified
                        modified = True
                        new_link = f"[{label}](../_resources/{best_match})"
                        print(f"Dans {file_path}, le fichier référencé '{referenced_filename}' est remplacé par '{best_match}'")
                        return new_link
                    else:
                        print(f"Pas de correspondance trouvée pour '{referenced_filename}' dans {file_path}")
                        return match.group(0)

                # Remplacer les liens et mettre à jour le fichier si modifié
                updated_content = link_pattern.sub(replace_link, content)
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"Liens mis à jour dans le fichier : {file_path}")

# Exécuter la fonction pour mettre à jour les liens avec le bon nom de fichier
update_links_with_correct_resources()
