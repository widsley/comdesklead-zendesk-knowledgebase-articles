#!/usr/bin/env python3
import os
import re
import json
import shutil

FOLDER_MAP = {
    'はじめてガイド/ユーザーガイド':      'guide/user',
    'はじめてガイド/推奨環境ガイド':      'guide/env',
    'はじめてガイド/管理者ガイド':        'guide/admin',
    'トラブルシューティング/エラー':      'troubleshoot/error',
    'トラブルシューティング/サポートチームへのお問い合わせ方法': 'troubleshoot/support',
    'ハードウェアについて/弊社貸出端末について':  'hardware/device',
    'ハードウェアについて/端末に関する各種ご依頼': 'hardware/request',
    'リリースノート・お知らせ/Comdesk_Lead_Release_Notes': 'release/notes',
    'リリースノート・お知らせ/Widsley_News': 'release/news',
    '機能一覧/基本ガイド':               'features/basic',
    '機能一覧/活用ガイド':               'features/advanced',
    '製品・プランについて/Comdesk_Leadのご契約について': 'plan/contract',
}

SUMMARY_STRUCTURE = [
    ('はじめてガイド', [
        ('ユーザーガイド',   'guide/user'),
        ('推奨環境ガイド',   'guide/env'),
        ('管理者ガイド',     'guide/admin'),
    ]),
    ('機能一覧', [
        ('基本ガイド',       'features/basic'),
        ('活用ガイド',       'features/advanced'),
    ]),
    ('トラブルシューティング', [
        ('エラー',           'troubleshoot/error'),
        ('サポートへのお問い合わせ', 'troubleshoot/support'),
    ]),
    ('ハードウェアについて', [
        ('貸出端末について',  'hardware/device'),
        ('各種ご依頼',       'hardware/request'),
    ]),
    ('リリースノート・お知らせ', [
        ('リリースノート',   'release/notes'),
        ('Widsley News',     'release/news'),
    ]),
    ('製品・プランについて', [
        ('ご契約について',   'plan/contract'),
    ]),
]

NAVIGATION_STRUCTURE = SUMMARY_STRUCTURE

def get_article_id(filename):
    match = re.match(r'^(\d+)', filename)
    return match.group(1) if match else None

def get_title_from_md(filepath):
    try:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
        m = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
        if m:
            return m.group(1).strip().strip('"\'')
        m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return None

def rename_files():
    id_to_title = {}
    id_to_folder = {}
    moved_count = 0

    for src_folder, dst_folder in FOLDER_MAP.items():
        if not os.path.exists(src_folder):
            print(f'SKIP (not found): {src_folder}')
            continue

        os.makedirs(dst_folder, exist_ok=True)

        for filename in sorted(os.listdir(src_folder)):
            if not filename.endswith('.md'):
                continue
            article_id = get_article_id(filename)
            if not article_id:
                print(f'  SKIP (no ID): {filename}')
                continue

            src_file = os.path.join(src_folder, filename)
            new_filename = article_id + '.md'
            dst_file = os.path.join(dst_folder, new_filename)

            title = get_title_from_md(src_file)
            if title:
                id_to_title[article_id] = title
            id_to_folder[article_id] = dst_folder

            shutil.move(src_file, dst_file)
            moved_count += 1

    print(f'Moved {moved_count} files')

    # 空になった日本語フォルダを削除
    removed_tops = set()
    for src_folder in FOLDER_MAP:
        top = src_folder.split('/')[0]
        if top not in removed_tops and os.path.exists(top):
            shutil.rmtree(top, ignore_errors=True)
            removed_tops.add(top)
            print(f'Removed folder: {top}')

    # ローマ字の空フォルダも削除
    for folder in ['hajimetegaido', 'hdoweanitsuite', 'ji-neng-yi-lan',
                    'purannitsuite', 'rirsuntoorase', 'toraburushtingu']:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
            print(f'Removed romanized folder: {folder}')

    return id_to_title, id_to_folder

def create_readme_files():
    folder_names = {
        'guide':             'はじめてガイド',
        'guide/user':        'ユーザーガイド',
        'guide/env':         '推奨環境ガイド',
        'guide/admin':       '管理者ガイド',
        'features':          '機能一覧',
        'features/basic':    '基本ガイド',
        'features/advanced': '活用ガイド',
        'troubleshoot':          'トラブルシューティング',
        'troubleshoot/error':    'エラー',
        'troubleshoot/support':  'サポートへのお問い合わせ',
        'hardware':          'ハードウェアについて',
        'hardware/device':   '貸出端末について',
        'hardware/request':  '各種ご依頼',
        'release':           'リリースノート・お知らせ',
        'release/notes':     'リリースノート',
        'release/news':      'Widsley News',
        'plan':              '製品・プランについて',
        'plan/contract':     'ご契約について',
    }
    for folder, name in folder_names.items():
        os.makedirs(folder, exist_ok=True)
        readme_path = os.path.join(folder, 'README.md')
        if not os.path.exists(readme_path):
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f'# {name}\n')

def generate_summary(id_to_title):
    lines = ['# Table of contents', '']
    lines.append('* [Comdeskご利用ガイド](README.md)')
    for top_name, subgroups in SUMMARY_STRUCTURE:
        lines.append(f'* [{top_name}]({subgroups[0][1]}/README.md)')
        for sub_name, folder in subgroups:
            lines.append(f'  * [{sub_name}]({folder}/README.md)')
            if not os.path.exists(folder):
                continue
            files = sorted(
                [f for f in os.listdir(folder) if f.endswith('.md') and f != 'README.md'],
                key=lambda x: int(x.replace('.md', '')) if x.replace('.md', '').isdigit() else 0
            )
            for filename in files:
                article_id = filename.replace('.md', '')
                title = id_to_title.get(article_id, article_id)
                path = f'{folder}/{filename}'
                lines.append(f'    * [{title}]({path})')
    lines.append('')
    with open('SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('SUMMARY.md generated!')

def generate_docs_json():
    navigation_groups = []
    for top_name, subgroups in NAVIGATION_STRUCTURE:
        sub_pages = []
        for sub_name, folder in subgroups:
            if not os.path.exists(folder):
                continue
            files = sorted(
                [f for f in os.listdir(folder) if f.endswith('.md') and f != 'README.md'],
                key=lambda x: int(x.replace('.md', '')) if x.replace('.md', '').isdigit() else 0
            )
            pages = [f'{folder}/{f.replace(".md", "")}' for f in files]
            if pages:
                sub_pages.append({'group': sub_name, 'pages': pages})
        if sub_pages:
            navigation_groups.append({'group': top_name, 'pages': sub_pages})

    docs_json = {
        '$schema': 'https://mintlify.com/schema.json',
        'name': 'Comdesk ヘルプ',
        'locale': 'ja',
        'theme': 'mint',
        'colors': {'primary': '#00BCD4'},
        'navigation': {'groups': navigation_groups}
    }
    with open('docs.json', 'w', encoding='utf-8') as f:
        json.dump(docs_json, f, ensure_ascii=False, indent=2)
    print('docs.json generated!')

def update_mintignore():
    with open('.mintignore', 'w', encoding='utf-8') as f:
        f.write('.gitbook/\nSUMMARY.md\nREADME.md\ntest.md\n')
    print('.mintignore updated!')

if __name__ == '__main__':
    # リポジトリルートに移動
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    os.chdir(repo_root)
    print(f'Working directory: {os.getcwd()}')
    print('=== Step 1: Renaming files ===')
    id_to_title, id_to_folder = rename_files()
    print('\n=== Step 2: Creating README files ===')
    create_readme_files()
    print('\n=== Step 3: Generating SUMMARY.md ===')
    generate_summary(id_to_title)
    print('\n=== Step 4: Generating docs.json ===')
    generate_docs_json()
    print('\n=== Step 5: Updating .mintignore ===')
    update_mintignore()
    print('\n=== Done! ===')
