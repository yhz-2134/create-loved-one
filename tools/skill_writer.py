#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill写入工具
用于创建、更新和管理Skill文件
"""

import argparse
import json
import os
from datetime import datetime


def create_skill(slug, base_dir, meta_path, memory_path, persona_path):
    """创建新的Skill"""
    # 读取元数据
    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    
    # 读取memory和persona内容
    with open(memory_path, 'r', encoding='utf-8') as f:
        memory_content = f.read()
    
    with open(persona_path, 'r', encoding='utf-8') as f:
        persona_content = f.read()
    
    # 创建Skill目录
    skill_dir = os.path.join(base_dir, slug)
    os.makedirs(skill_dir, exist_ok=True)
    
    # 写入文件
    # meta.json
    meta['created_at'] = datetime.now().isoformat()
    meta['updated_at'] = datetime.now().isoformat()
    with open(os.path.join(skill_dir, 'meta.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    # memory.md
    with open(os.path.join(skill_dir, 'memory.md'), 'w', encoding='utf-8') as f:
        f.write(memory_content)
    
    # persona.md
    with open(os.path.join(skill_dir, 'persona.md'), 'w', encoding='utf-8') as f:
        f.write(persona_content)
    
    # 生成SKILL.md
    combine_skill(slug, base_dir)
    
    print(f'成功创建Skill: {slug}')
    return True


def combine_skill(slug, base_dir):
    """合并生成SKILL.md"""
    skill_dir = os.path.join(base_dir, slug)
    if not os.path.exists(skill_dir):
        print(f'Skill {slug} 不存在')
        return False
    
    # 读取meta.json
    meta_path = os.path.join(skill_dir, 'meta.json')
    if not os.path.exists(meta_path):
        print('meta.json 不存在')
        return False
    
    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    
    # 读取memory.md和persona.md
    memory_path = os.path.join(skill_dir, 'memory.md')
    persona_path = os.path.join(skill_dir, 'persona.md')
    
    if not os.path.exists(memory_path) or not os.path.exists(persona_path):
        print('memory.md 或 persona.md 不存在')
        return False
    
    with open(memory_path, 'r', encoding='utf-8') as f:
        memory_content = f.read()
    
    with open(persona_path, 'r', encoding='utf-8') as f:
        persona_content = f.read()
    
    # 生成SKILL.md内容
    skill_content = f"""
---
name: {meta.get('name', slug)}
description: "与{meta.get('name', '亲人')}的数字记忆与情感连接"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit
---

# {meta.get('name', '亲人')}.skill

## 记忆库

{memory_content}

## 人格

{persona_content}

## 运行逻辑

1. 收到消息后，先从人格层判断回应风格
2. 从记忆库中提取相关背景和情感连接
3. 用亲人的方式生成回应

## 管理

- 说"我有新的回忆"或"追加记忆"来更新
- 说"亲人不会这样说"或"应该是"来纠正
- 使用`/update-loved-one {slug}`命令更新
- 使用`/rollback-loved-one {slug} version`命令回滚

""".strip()
    
    # 写入SKILL.md
    with open(os.path.join(skill_dir, 'SKILL.md'), 'w', encoding='utf-8') as f:
        f.write(skill_content)
    
    print(f'成功生成SKILL.md: {slug}')
    return True


def list_skills(base_dir):
    """列出所有Skill"""
    if not os.path.exists(base_dir):
        print('Skill目录不存在')
        return
    
    skills = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, 'SKILL.md')):
            # 读取meta.json获取信息
            meta_path = os.path.join(item_path, 'meta.json')
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                    skills.append({
                        'slug': item,
                        'name': meta.get('name', item),
                        'created_at': meta.get('created_at', '未知'),
                        'version': meta.get('version', 'v1')
                    })
                except Exception:
                    skills.append({
                        'slug': item,
                        'name': item,
                        'created_at': '未知',
                        'version': 'v1'
                    })
            else:
                skills.append({
                    'slug': item,
                    'name': item,
                    'created_at': '未知',
                    'version': 'v1'
                })
    
    if skills:
        print('已创建的亲人Skill:')
        for skill in skills:
            print(f"  - {skill['name']} (/{skill['slug']}) - 创建时间: {skill['created_at']} - 版本: {skill['version']}")
    else:
        print('暂无创建的亲人Skill')


def main():
    parser = argparse.ArgumentParser(description='Skill写入工具')
    parser.add_argument('--action', required=True, help='操作：create/combine/list')
    parser.add_argument('--slug', help='Skill的slug')
    parser.add_argument('--base-dir', default='./.claude/skills', help='Skill基础目录')
    parser.add_argument('--meta', help='元数据文件路径')
    parser.add_argument('--self', dest='memory', help='memory.md文件路径')
    parser.add_argument('--persona', help='persona.md文件路径')
    
    args = parser.parse_args()
    
    if args.action == 'create':
        if not args.slug or not args.meta or not args.memory or not args.persona:
            print('创建操作需要指定slug、meta、memory和persona文件路径')
        else:
            create_skill(args.slug, args.base_dir, args.meta, args.memory, args.persona)
    elif args.action == 'combine':
        if not args.slug:
            print('合并操作需要指定slug')
        else:
            combine_skill(args.slug, args.base_dir)
    elif args.action == 'list':
        list_skills(args.base_dir)
    else:
        print('不支持的操作')


if __name__ == '__main__':
    main()
