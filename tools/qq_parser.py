#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ聊天记录解析工具
支持XML格式的QQ聊天记录导出
"""

import argparse
import xml.etree.ElementTree as ET
from datetime import datetime


def parse_qq_xml(xml_path, target_name, output_file):
    """解析QQ导出的XML聊天记录"""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        print(f'解析XML文件失败: {e}')
        return 0
    
    messages = []
    
    # QQ XML格式可能因版本而异，这里提供一个通用解析
    for msg_elem in root.findall('.//msg'):
        try:
            # 提取消息信息
            content = msg_elem.findtext('content')
            time_str = msg_elem.findtext('time')
            sender = msg_elem.findtext('sendername')
            
            if content and time_str and sender:
                # 转换时间戳
                try:
                    timestamp = int(time_str)
                    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    date = time_str
                
                if target_name in sender:
                    messages.append(f"[{date}] {sender}: {content}")
        except Exception:
            continue
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(messages))
    
    return len(messages)


def main():
    parser = argparse.ArgumentParser(description='QQ聊天记录解析工具')
    parser.add_argument('--file', required=True, help='QQ聊天记录XML文件路径')
    parser.add_argument('--target', required=True, help='目标联系人名称')
    parser.add_argument('--output', required=True, help='输出文件路径')
    
    args = parser.parse_args()
    
    try:
        count = parse_qq_xml(args.file, args.target, args.output)
        print(f'成功解析 {count} 条消息，已保存到 {args.output}')
    except Exception as e:
        print(f'解析失败：{e}')


if __name__ == '__main__':
    main()
