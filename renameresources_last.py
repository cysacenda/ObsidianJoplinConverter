import os
import re
import filetype

# Définir les répertoires des ressources et des notes
resources_dir = r'G:\Mon Drive\_Obsidian\_resources'
notes_dir = r'G:\Mon Drive\_Obsidian'

# Fonction pour corriger les extensions des fichiers dans _resources
def correct_file_extensions():
    renamed_files = {}
    
    for filename in os.listdir(resources_dir):
        file_path = os.path.join(resources_dir, filename)
        
        # Vérifier si le fichier n'a pas la bonne extension
        if os.path.isfile(file_path) and not os.path.splitext(filename)[1]:
            kind = filetype.guess(file_path)
            if kind:
                # Ajouter l'extension correcte
                new_filename = f"{filename}.{kind.extension}"
                new_file_path = os.path.join(resources_dir, new_filename)
                os.rename(file_path, new_file_path)
                renamed_files[filename] = new_filename
                print(f"Renamed: {filename} -> {new_filename}")
            else:
                print(f"Impossible de déterminer l'extension pour {filename}")
                
        elif filename.endswith(('.jp', '.j', '.pn')):  # Ajouter des vérifications spécifiques pour les extensions tronquées
            # Deviner l'extension attendue et renommer
            extension_mapping = {
                '.jp': '.jpg',
                '.j': '.jpg',
                '.pn': '.png'
            }
            ext = os.path.splitext(filename)[1]
            if ext in extension_mapping:
                new_filename = filename[:-len(ext)] + extension_mapping[ext]
                new_file_path = os.path.join(resources_dir, new_filename)
                os.rename(file_path, new_file_path)
                renamed_files[filename] = new_filename
                print(f"Renamed: {filename} -> {new_filename}")
                
    return renamed_files

# Fonction pour mettre à jour les liens dans les notes avec le nom correct des ressources
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
renamed_files = correct_file_extensions()
if renamed_files:
    update_links_with_correct_resources(renamed_files)
else:
    print("Aucun fichier à corriger dans les ressources.")
