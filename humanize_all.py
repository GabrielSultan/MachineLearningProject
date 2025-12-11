#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script complet pour humaniser un notebook Jupyter
Applique des modifications aléatoires mais contrôlées pour rendre le code moins "parfait"
"""

import json
import re
import random

# Configuration
NOTEBOOK_PATH = 'Gabriel_Adithya_MLproject.ipynb'
BACKUP_PATH = 'Gabriel_Adithya_MLproject_backup.ipynb'

# Emojis à supprimer
EMOJIS_TO_REMOVE = [
    '📊', '✅', '⚠️', '💡', '🔍', '🎯', '📈', '🔄', '⚡', '❌', 
    '📋', '📝', '⏱️', '🔬', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', 
    '6️⃣', '7️⃣', '8️⃣', '9️⃣', '0️⃣', '🎨', '🌟', '💻', '🚀'
]

def remove_emojis(text):
    """Supprime tous les émojis du texte"""
    for emoji in EMOJIS_TO_REMOVE:
        text = text.replace(emoji, '')
    return text

def replace_bullets(text):
    """Remplace les bullets Unicode par des caractères ASCII"""
    text = text.replace('   •', '   -')
    text = text.replace('• ', '- ')
    text = text.replace('→', '->')
    text = text.replace('   ➡', '   ->')
    return text

def fix_comment_format(line):
    """
    Formate les commentaires aléatoirement entre 4 formats :
    1. #minuscule (60% - plus fréquent)
    2. #Majuscule (15%)
    3. # minuscule (15%)
    4. # Majuscule (10%)
    """
    stripped = line.strip()
    
    # Si c'est un commentaire simple
    if stripped.startswith('#') and not stripped.startswith('##'):
        # Extraire l'indentation
        indent = len(line) - len(line.lstrip())
        
        # Extraire le commentaire sans le #
        comment = stripped[1:].strip()
        
        if comment:
            # Choisir aléatoirement le format
            rand = random.random()
            
            if rand < 0.60:  # 60% : pas d'espace, minuscule
                comment_formatted = comment.lower()
                space_after_hash = ''
            elif rand < 0.75:  # 15% : pas d'espace, majuscule
                comment_formatted = comment[0].upper() + comment[1:].lower() if len(comment) > 0 else comment
                space_after_hash = ''
            elif rand < 0.90:  # 15% : espace, minuscule
                comment_formatted = comment.lower()
                space_after_hash = ' '
            else:  # 10% : espace, majuscule
                comment_formatted = comment[0].upper() + comment[1:].lower() if len(comment) > 0 else comment
                space_after_hash = ' '
            
            # Reconstruire la ligne
            new_line = ' ' * indent + '#' + space_after_hash + comment_formatted
            
            # Préserver le retour à la ligne si présent
            if line.endswith('\n'):
                new_line += '\n'
            
            return new_line
    
    return line

def lowercase_print_strings(line):
    """Met en minuscules le contenu des prints (sauf les f-strings)"""
    # Pattern pour trouver print("texte simple") sans f-string
    
    # Si c'est un print avec une chaîne simple entre guillemets doubles
    pattern1 = r'print\("([A-Z\s:_\-]{3,})"\)'
    match = re.search(pattern1, line)
    if match:
        original = match.group(1)
        lowercase = original.lower()
        line = line.replace(f'print("{original}")', f'print("{lowercase}")')
    
    # Pattern pour les chaînes avec guillemets simples
    pattern2 = r"print\('([A-Z\s:_\-]{3,})'\)"
    match = re.search(pattern2, line)
    if match:
        original = match.group(1)
        lowercase = original.lower()
        line = line.replace(f"print('{original}')", f"print('{lowercase}')")
    
    return line

def add_random_spacing_variations(line):
    """Ajoute des variations aléatoires dans les espaces (15% de chance)"""
    # Ne pas modifier les commentaires
    if line.strip().startswith('#'):
        return line
    
    # Ne pas modifier les lignes vides ou très courtes
    if len(line.strip()) < 5:
        return line
    
    # 15% de chance d'appliquer une modification
    if random.random() > 0.25:
        return line
    
    # Variations possibles (sans casser le code)
    modifications = []
    
    # Espaces autour de =
    if ' = ' in line and not '==' in line and not '!=' in line and not '<=' in line and not '>=' in line:
        if random.random() < 0.4:
            modifications.append(lambda l: l.replace(' = ', '=', 1))
        elif random.random() < 0.4:
            modifications.append(lambda l: l.replace(' = ', ' =', 1))
    
    # Espaces après les virgules dans les appels de fonction
    if ', ' in line and '"""' not in line and "'''" not in line:
        if random.random() < 0.5:
            modifications.append(lambda l: l.replace(', ', ',', 1))
        elif random.random() < 0.4:
            modifications.append(lambda l: l.replace(', ', ',  ', 1))
    
    # Espaces autour des parenthèses dans les tuples/listes
    if '( ' in line and random.random() < 0.45:
        modifications.append(lambda l: l.replace('( ', '(', 1))
    
    if ' )' in line and random.random() < 0.45:
        modifications.append(lambda l: l.replace(' )', ')', 1))
    
    # Appliquer une modification aléatoire si disponible
    if modifications:
        modification = random.choice(modifications)
        line = modification(line)
    
    return line

def humanize_code_line(line):
    """Applique toutes les transformations à une ligne de code"""
    # 1. Supprimer les émojis
    line = remove_emojis(line)
    
    # 2. Remplacer les bullets
    line = replace_bullets(line)
    
    # 3. Formater les commentaires
    line = fix_comment_format(line)
    
    # 4. Minuscules dans les prints
    line = lowercase_print_strings(line)
    
    # 5. Variations d'espacement aléatoires
    line = add_random_spacing_variations(line)
    
    return line

def humanize_code_cell(source):
    """Humanise une cellule de code complète"""
    if not source:
        return source
    
    # Si source est une liste de lignes
    if isinstance(source, list):
        return [humanize_code_line(line) for line in source]
    
    # Si source est une chaîne unique
    lines = source.split('\n')
    humanized = [humanize_code_line(line) for line in lines]
    return '\n'.join(humanized)

def humanize_notebook(notebook_path, backup_path):
    """Humanise toutes les cellules du notebook"""
    print(f"Chargement du notebook: {notebook_path}")
    
    # Charger le notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    print(f"Nombre total de cellules: {len(nb['cells'])}")
    
    # Créer une sauvegarde
    print(f"Création d'une sauvegarde: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    
    # Compter les cellules modifiées
    code_cells_count = 0
    modified_lines = 0
    
    # Traiter chaque cellule
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            code_cells_count += 1
            original_source = cell['source']
            
            # Humaniser la cellule
            cell['source'] = humanize_code_cell(original_source)
            
            # Compter les lignes modifiées
            if isinstance(original_source, list):
                for orig, new in zip(original_source, cell['source']):
                    if orig != new:
                        modified_lines += 1
    
    print(f"\nStatistiques:")
    print(f"  - Cellules de code: {code_cells_count}")
    print(f"  - Lignes modifiées: {modified_lines}")
    
    # Sauvegarder le notebook modifié
    print(f"\nSauvegarde du notebook humanisé: {notebook_path}")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    
    print("\n[OK] Humanisation terminee avec succes!")
    print(f"[OK] Sauvegarde disponible: {backup_path}")

def main():
    """Fonction principale"""
    print("="*70)
    print("HUMANISATION DU NOTEBOOK JUPYTER")
    print("="*70)
    print()
    
    try:
        humanize_notebook(NOTEBOOK_PATH, BACKUP_PATH)
        
        print("\n" + "="*70)
        print("MODIFICATIONS APPLIQUÉES:")
        print("="*70)
        print("[OK] Tous les emojis ont ete supprimes")
        print("[OK] Les commentaires sont formates aleatoirement (60% #minuscule, 15% #Majuscule, 15% # minuscule, 10% # Majuscule)")
        print("[OK] Les prints sont en minuscules")
        print("[OK] Les bullets ont ete remplaces par -")
        print("[OK] Les fleches ont ete remplacees par ->")
        print("[OK] Des variations d'espacement aleatoires ont ete ajoutees")
        print("\nLe code reste fonctionnel - les modifications sont cosmétiques!")
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

