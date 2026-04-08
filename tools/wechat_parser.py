#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信聊天记录解析工具
支持多种导出格式：WeChatMsg、留痕、PyWxDump
"""

import argparse
import json
import os
import sqlite3
from datetime import datetime


def parse_wechatmsg(db_path, target_name, output_file):
    """解析WeChatMsg导出的数据库"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询消息记录
    cursor.execute('''
        SELECT msg.content, msg.createTime, msg.type, 
               contact.nickname, contact.remark 
        FROM msg 
        JOIN contact ON msg.talker = contact.username 
        WHERE (contact.nickname = ? OR contact.remark = ?) 
        ORDER BY msg.createTime
    ''', (target_name, target_name))
    
    messages = []
    for row in cursor.fetchall():
        content, create_time, msg_type, nickname, remark = row
        
        # 转换时间戳
        try:
            timestamp = int(create_time)
            if len(str(timestamp)) == 10:
                timestamp *= 1000
            date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        except:
            date = "未知时间"
        
        # 过滤消息类型
        if msg_type == 1:  # 文本消息
            messages.append(f"[{date}] {nickname or remark}: {content}")
    
    conn.close()
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(messages))
    
    return len(messages)


def parse_liuhen(html_path, target_name, output_file):
    """解析留痕导出的HTML文件"""
    import re
    from bs4 import BeautifulSoup
    
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    messages = []
    # 留痕的HTML结构可能因版本而异，这里提供一个通用解析
    for msg in soup.find_all(class_=re.compile(r'msg|message')):
        try:
            # 提取时间、发送者、内容
            time_elem = msg.find(class_=re.compile(r'time|date'))
            sender_elem = msg.find(class_=re.compile(r'sender|name'))
            content_elem = msg.find(class_=re.compile(r'content|text'))
            
            if time_elem and sender_elem and content_elem:
                time_str = time_elem.text.strip()
                sender = sender_elem.text.strip()
                content = content_elem.text.strip()
                
                if target_name in sender:
                    messages.append(f"[{time_str}] {sender}: {content}")
        except Exception:
            continue
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(messages))
    
    return len(messages)


def parse_pywxdump(json_path, target_name, output_file):
    """解析PyWxDump导出的JSON文件"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    messages = []
    for msg in data:
        try:
            if 'content' in msg and 'createTime' in msg and 'sender' in msg:
                if target_name in msg['sender']:
                    # 转换时间
                    timestamp = msg['createTime']
                    if isinstance(timestamp, str):
                        timestamp = int(timestamp)
                    date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    messages.append(f"[{date}] {msg['sender']}: {msg['content']}")
        except Exception:
            continue
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(messages))
    
    return len(messages)


def detect_format(file_path):
    """自动检测文件格式"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.db':
        return 'wechatmsg'
    elif ext == '.html':
        return 'liuhen'
    elif ext == '.json':
        return 'pywxdump'
    else:
        return None


def main():
    parser = argparse.ArgumentParser(description='微信聊天记录解析工具')
    parser.add_argument('--file', required=True, help='聊天记录文件路径')
    parser.add_argument('--target', required=True, help='目标联系人名称')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--format', default='auto', help='文件格式：wechatmsg/liuhen/pywxdump/auto')
    
    args = parser.parse_args()
    
    # 自动检测格式
    if args.format == 'auto':
        args.format = detect_format(args.file)
        if not args.format:
            print('无法自动检测文件格式，请手动指定')
            return
    
    # 解析文件
    try:
        if args.format == 'wechatmsg':
            count = parse_wechatmsg(args.file, args.target, args.output)
        elif args.format == 'liuhen':
            count = parse_liuhen(args.file, args.target, args.output)
        elif args.format == 'pywxdump':
            count = parse_pywxdump(args.file, args.target, args.output)
        else:
            print('不支持的文件格式')
            return
        
        print(f'成功解析 {count} 条消息，已保存到 {args.output}')
    except Exception as e:
        print(f'解析失败：{e}')


if __name__ == '__main__':
    main()
