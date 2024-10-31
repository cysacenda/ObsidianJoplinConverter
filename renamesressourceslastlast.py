import os
import re
from difflib import get_close_matches
import filetype

# Définir les répertoires des ressources et des notes
resources_dir = r'G:\Mon Drive\_Obsidian\_resources'
notes_dir = r'G:\Mon Drive\_Obsidian'

# Charger tous les fichiers dans le dossier des ressources
def get_all_resources():
    return {filename for filename in os.listdir(resources_dir) if os.path.isfile(os.path.join(resources_dir, filename))}

# Fonction pour corriger les extensions et les noms de fichiers incomplets dans _resources
def correct_file_names_and_extensions():
    renamed_files = {}
    
    for filename in os.listdir(resources_dir):
        file_path = os.path.join(resources_dir, filename)
        
        # Vérification des fichiers avec une extension incomplète ou partiellement tronquée
        if filename.endswith(('.jp', '.j', '.pn', '(1', '(2', '(3', '.pdf', '.docx', '.pptx')):  # Ajouter ici d'autres extensions suspectes
            # Mapping d'extensions attendues en cas de troncature
            extension_mapping = {
                '.jp': '.jpg',
                '.j': '.jpg',
                '.pn': '.png',
                '.pdf': '.pdf',
                '.docx': '.docx',
                '.pptx': '.pptx'
            }
            ext = os.path.splitext(filename)[1]
            
            # Deviner l'extension attendue et renommer
            new_ext = extension_mapping.get(ext, '.jpg')  # Par défaut .jpg si inconnu
            new_filename = filename[:-len(ext)] + new_ext
            new_file_path = os.path.join(resources_dir, new_filename)
            os.rename(file_path, new_file_path)
            renamed_files[filename] = new_filename
            print(f"Renamed: {filename} -> {new_filename}")
        
        # Vérifier si un fichier n'a pas d'extension et essayer de deviner son type
        elif os.path.isfile(file_path) and not os.path.splitext(filename)[1]:
            kind = filetype.guess(file_path)
            if kind:
                # Ajouter l'extension détectée
                new_filename = f"{filename}.{kind.extension}"
                new_file_path = os.path.join(resources_dir, new_filename)
                os.rename(file_path, new_file_path)
                renamed_files[filename] = new_filename
                print(f"Renamed: {filename} -> {new_filename}")
            else:
                print(f"Impossible de déterminer l'extension pour {filename}")
                
    return renamed_files

# Fonction pour mettre à jour les liens dans les notes avec les nouveaux noms des ressources
def update_links_with_correct_resources(renamed_files):
    link_pattern = re.compile(r'\[(.*?)\]\(\.\./_resources/([^)]+)\)')

    for root, _, files in os.walk(notes_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                modified = False

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Rechercher et remplacer les liens vers les ressources dans le contenu
                def replace_link(match):
                    label = match.group(1)
                    referenced_filename = match.group(2)

                    # Vérifier si le fichier référencé a été renommé
                    if referenced_filename in renamed_files:
                        nonlocal modified
                        modified = True
                        corrected_filename = renamed_files[referenced_filename]
                        new_link = f"[{label}](../_resources/{corrected_filename})"
                        print(f"Dans {file_path}, le fichier référencé '{referenced_filename}' est remplacé par '{corrected_filename}'")
                        return new_link
                    else:
                        return match.group(0)

                # Remplacer les liens et mettre à jour le fichier si modifié
                updated_content = link_pattern.sub(replace_link, content)
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"Liens mis à jour dans le fichier : {file_path}")

# Exécuter les deux fonctions
renamed_files = correct_file_names_and_extensions()
if renamed_files:
    update_links_with_correct_resources(renamed_files)
else:
    print("Aucun fichier à corriger dans les ressources.")
