#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具测试脚本
验证所有工具是否能正常运行
"""

import os
import sys
import tempfile
import shutil

# 添加tools目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

def test_photo_analyzer():
    """测试照片分析工具"""
    print("\n=== 测试照片分析工具 ===")
    
    # 创建临时目录和测试文件
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建一个简单的测试照片（使用PIL创建）
        from PIL import Image
        test_image = Image.new('RGB', (100, 100), color='red')
        test_image_path = os.path.join(temp_dir, 'test.jpg')
        test_image.save(test_image_path)
        
        # 测试命令
        output_file = os.path.join(temp_dir, 'output.txt')
        cmd = f"python tools/photo_analyzer.py --dir {temp_dir} --output {output_file}"
        print(f"执行命令: {cmd}")
        
        try:
            os.system(cmd)
            if os.path.exists(output_file):
                print("OK 照片分析工具测试成功")
                with open(output_file, 'r', encoding='utf-8') as f:
                    print("输出预览:")
                    print(f.read()[:200] + "...")
            else:
                print("FAIL 照片分析工具测试失败")
        except Exception as e:
            print(f"FAIL 照片分析工具测试失败: {e}")

def test_skill_writer():
    """测试Skill写入工具"""
    print("\n=== 测试Skill写入工具 ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试文件
        meta_content = '''{
    "name": "测试亲人",
    "slug": "test-loved-one",
    "profile": {
        "relationship": "父亲",
        "birth_year": "1950",
        "passing_year": "2020",
        "occupation": "教师",
        "hobbies": "下棋、钓鱼",
        "personality": "温和"
    },
    "memory_sources": [],
    "corrections_count": 0
}'''
        
        memory_content = "# 记忆库\n\n## 共同经历\n- 一起钓鱼\n\n## 价值观\n- 诚实做人"
        persona_content = "# 人格\n\n## 说话风格\n- 温和，有耐心"
        
        # 写入测试文件
        meta_path = os.path.join(temp_dir, 'meta.json')
        memory_path = os.path.join(temp_dir, 'memory.md')
        persona_path = os.path.join(temp_dir, 'persona.md')
        
        with open(meta_path, 'w', encoding='utf-8') as f:
            f.write(meta_content)
        with open(memory_path, 'w', encoding='utf-8') as f:
            f.write(memory_content)
        with open(persona_path, 'w', encoding='utf-8') as f:
            f.write(persona_content)
        
        # 创建目标目录
        target_dir = os.path.join(temp_dir, '.claude', 'skills')
        os.makedirs(target_dir, exist_ok=True)
        
        # 测试创建Skill
        cmd = f"python tools/skill_writer.py --action create --slug test-loved-one --base-dir {target_dir} --meta {meta_path} --self {memory_path} --persona {persona_path}"
        print(f"执行命令: {cmd}")
        
        try:
            os.system(cmd)
            skill_dir = os.path.join(target_dir, 'test-loved-one')
            if os.path.exists(os.path.join(skill_dir, 'SKILL.md')):
                print("OK Skill写入工具测试成功")
            else:
                print("FAIL Skill写入工具测试失败")
        except Exception as e:
            print(f"FAIL Skill写入工具测试失败: {e}")

def test_version_manager():
    """测试版本管理工具"""
    print("\n=== 测试版本管理工具 ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试Skill目录
        skill_dir = os.path.join(temp_dir, 'test-loved-one')
        os.makedirs(skill_dir, exist_ok=True)
        
        # 创建必要文件
        meta_content = '''{
    "name": "测试亲人",
    "slug": "test-loved-one",
    "version": "v1",
    "updated_at": "2026-04-07T00:00:00"
}'''
        
        with open(os.path.join(skill_dir, 'meta.json'), 'w', encoding='utf-8') as f:
            f.write(meta_content)
        with open(os.path.join(skill_dir, 'memory.md'), 'w', encoding='utf-8') as f:
            f.write("# 记忆库")
        with open(os.path.join(skill_dir, 'persona.md'), 'w', encoding='utf-8') as f:
            f.write("# 人格")
        with open(os.path.join(skill_dir, 'SKILL.md'), 'w', encoding='utf-8') as f:
            f.write("# 测试Skill")
        
        # 测试备份
        cmd = f"python tools/version_manager.py --action backup --slug test-loved-one --base-dir {temp_dir}"
        print(f"执行命令: {cmd}")
        
        try:
            os.system(cmd)
            versions_dir = os.path.join(skill_dir, 'versions')
            if os.path.exists(versions_dir) and len(os.listdir(versions_dir)) > 0:
                print("OK 版本管理工具测试成功")
            else:
                print("FAIL 版本管理工具测试失败")
        except Exception as e:
            print(f"FAIL 版本管理工具测试失败: {e}")

def main():
    print("开始测试工具...")
    
    # 检查tools目录是否存在
    if not os.path.exists('tools'):
        print("错误: tools目录不存在")
        return
    
    # 测试各个工具
    test_photo_analyzer()
    test_skill_writer()
    test_version_manager()
    
    print("\n测试完成！")


if __name__ == '__main__':
    main()
