#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本管理工具
用于备份和回滚Skill版本
"""

import argparse
import json
import os
import shutil
from datetime import datetime


def backup_skill(slug, base_dir):
    """备份Skill版本"""
    skill_dir = os.path.join(base_dir, slug)
    if not os.path.exists(skill_dir):
        print(f'Skill {slug} 不存在')
        return False
    
    # 创建版本备份目录
    backup_dir = os.path.join(skill_dir, 'versions')
    os.makedirs(backup_dir, exist_ok=True)
    
    # 生成版本号
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    version = f'v{timestamp}'
    
    # 备份文件
    backup_version_dir = os.path.join(backup_dir, version)
    os.makedirs(backup_version_dir, exist_ok=True)
    
    # 复制文件
    for file in ['memory.md', 'persona.md', 'meta.json', 'SKILL.md']:
        src = os.path.join(skill_dir, file)
        if os.path.exists(src):
            dst = os.path.join(backup_version_dir, file)
            shutil.copy2(src, dst)
    
    # 更新meta.json中的版本信息
    meta_path = os.path.join(skill_dir, 'meta.json')
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        
        meta['version'] = version
        meta['updated_at'] = datetime.now().isoformat()
        
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f'成功备份到版本 {version}')
    return True


def rollback_skill(slug, version, base_dir):
    """回滚Skill版本"""
    skill_dir = os.path.join(base_dir, slug)
    if not os.path.exists(skill_dir):
        print(f'Skill {slug} 不存在')
        return False
    
    # 检查版本是否存在
    backup_version_dir = os.path.join(skill_dir, 'versions', version)
    if not os.path.exists(backup_version_dir):
        print(f'版本 {version} 不存在')
        return False
    
    # 恢复文件
    for file in ['memory.md', 'persona.md', 'meta.json', 'SKILL.md']:
        src = os.path.join(backup_version_dir, file)
        if os.path.exists(src):
            dst = os.path.join(skill_dir, file)
            shutil.copy2(src, dst)
    
    # 更新meta.json中的版本信息
    meta_path = os.path.join(skill_dir, 'meta.json')
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        
        meta['version'] = version
        meta['updated_at'] = datetime.now().isoformat()
        
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f'成功回滚到版本 {version}')
    return True


def list_versions(slug, base_dir):
    """列出所有版本"""
    skill_dir = os.path.join(base_dir, slug)
    if not os.path.exists(skill_dir):
        print(f'Skill {slug} 不存在')
        return
    
    backup_dir = os.path.join(skill_dir, 'versions')
    if not os.path.exists(backup_dir):
        print('暂无备份版本')
        return
    
    versions = []
    for item in os.listdir(backup_dir):
        item_path = os.path.join(backup_dir, item)
        if os.path.isdir(item_path):
            versions.append(item)
    
    if versions:
        print('可用版本：')
        for version in sorted(versions, reverse=True):
            print(f'  - {version}')
    else:
        print('暂无备份版本')


def main():
    parser = argparse.ArgumentParser(description='版本管理工具')
    parser.add_argument('--action', required=True, help='操作：backup/rollback/list')
    parser.add_argument('--slug', required=True, help='Skill的slug')
    parser.add_argument('--base-dir', default='./.claude/skills', help='Skill基础目录')
    parser.add_argument('--version', help='版本号，用于回滚')
    
    args = parser.parse_args()
    
    if args.action == 'backup':
        backup_skill(args.slug, args.base_dir)
    elif args.action == 'rollback':
        if not args.version:
            print('回滚操作需要指定版本号')
        else:
            rollback_skill(args.slug, args.version, args.base_dir)
    elif args.action == 'list':
        list_versions(args.slug, args.base_dir)
    else:
        print('不支持的操作')


if __name__ == '__main__':
    main()
