import os
import re
from datetime import datetime

# Définir le répertoire des fichiers .md
root_dir = r'G:\Mon Drive\_Obsidian\Archives'

# Expressions régulières pour détecter et modifier les informations dans les métadonnées
latitude_pattern = re.compile(r'^\s*latitude:\s*[\d\.\-]+\s*$', re.MULTILINE)
longitude_pattern = re.compile(r'^\s*longitude:\s*[\d\.\-]+\s*$', re.MULTILINE)
altitude_pattern = re.compile(r'^\s*altitude:\s*[\d\.\-]+\s*$', re.MULTILINE)
author_pattern = re.compile(r'^\s*author:\s*.*$', re.MULTILINE)
tag_pattern = re.compile(r'^\s*-\s*\'?>?\s*([^\']+?)\'?\s*$', re.MULTILINE)
date_pattern = re.compile(r'^(updated|created):\s*(\d{4}-\d{2}-\d{2})\s(\d{2}:\d{2}:\d{2})Z$', re.MULTILINE)

# Fonction pour convertir la date au nouveau format
def convert_date_format(match):
    prop = match.group(1)
    date_str = f"{match.group(2)} {match.group(3)}"
    # Convertir la date au format souhaité
    new_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S")
    return f"{prop}: {new_date}"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier s'il y a une section de métadonnées et la traiter uniquement
    if content.startswith('---'):
        # Séparer les métadonnées du contenu principal
        parts = content.split('---', 2)
        metadata = parts[1]
        body = parts[2] if len(parts) > 2 else ""

        # Supprimer les informations inutiles dans les métadonnées
        metadata = latitude_pattern.sub('', metadata)
        metadata = longitude_pattern.sub('', metadata)
        metadata = altitude_pattern.sub('', metadata)
        metadata = author_pattern.sub('', metadata)

        # Modifier les tags dans les métadonnées
        def replace_tag(match):
            # Retirer les espaces et les caractères spéciaux du tag
            tag = re.sub(r'[^a-zA-Z0-9]', '', match.group(1).strip())
            if tag.startswith('>'):
                tag = '0' + tag[1:]
            return f"- {tag}"  # Retourner le tag formaté sans quotes

        metadata = tag_pattern.sub(replace_tag, metadata)

        # Convertir le format de date pour les champs updated et created
        metadata = date_pattern.sub(convert_date_format, metadata)

        # Ajouter un retour à la ligne à la fin des métadonnées pour s'assurer qu'il y a un espace avant `---` final
        if not metadata.endswith('\n'):
            metadata += '\n'

        # Reconstruire le contenu avec métadonnées nettoyées et ajouter un retour à la ligne après le dernier ---
        new_content = f"---{metadata}---\n\n{body}"

        # Supprimer les lignes vides résiduelles dans les métadonnées
        new_content = re.sub(r'\n\s*\n', '\n', new_content)

        # Enregistrer les modifications si le contenu a changé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Processed: {file_path}')

# Parcourir tous les fichiers .md dans le répertoire spécifié
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.join(subdir, file)
            process_file(file_path)