#!/usr/bin/env python3
"""
Mintlify表示修正スクリプト
1. .mintignore から .gitbook/ を削除（画像修正）
2. 全mdファイルのフロントマター直後の # 見出し行を削除（タイトル二重修正）

リポジトリルートで実行すること
"""
import os
import re

# リポジトリルートに移動
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(repo_root)
print(f'Working directory: {os.getcwd()}')

# ============================================================
# Step 1: .mintignore から .gitbook/ を削除
# ============================================================
with open('.mintignore', 'r', encoding='utf-8') as f:
    mintignore = f.read()

fixed_mintignore = '\n'.join(
    line for line in mintignore.splitlines()
    if line.strip() != '.gitbook/'
) + '\n'

with open('.mintignore', 'w', encoding='utf-8') as f:
    f.write(fixed_mintignore)

print('.mintignore から .gitbook/ を削除しました')

# ============================================================
# Step 2: 全mdファイルの # タイトル行を削除
# （フロントマターに title: がある場合のみ）
# ============================================================

def remove_h1_if_title_in_frontmatter(content):
    if not content.startswith('---'):
        return content, False

    end = content.find('\n---', 3)
    if end == -1:
        return content, False

    frontmatter = content[:end + 4]
    body = content[end + 4:]

    if not re.search(r'^title:', frontmatter, re.MULTILINE):
        return content, False

    body_fixed = re.sub(r'^\n+# .+\n?', '\n', body)

    if body_fixed == body:
        return content, False

    return frontmatter + body_fixed, True

fixed_count = 0
for dirpath, _, filenames in os.walk('.'):
    if any(skip in dirpath for skip in ['.git', 'node_modules']):
        continue
    for filename in filenames:
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(dirpath, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            fixed, changed = remove_h1_if_title_in_frontmatter(content)
            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed)
                fixed_count += 1
        except Exception as e:
            print(f'  SKIP {filepath}: {e}')

print(f'タイトル二重修正: {fixed_count} ファイルを修正しました')
