#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社交媒体内容解析工具
支持解析微博、微信朋友圈等内容
"""

import argparse
import json
import os
from datetime import datetime


def parse_weibo(json_path, target_name, output_file):
    """解析微博内容"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    posts = []
    for post in data:
        try:
            if 'user' in post and 'screen_name' in post['user']:
                if target_name in post['user']['screen_name']:
                    # 提取发布时间
                    if 'created_at' in post:
                        created_at = post['created_at']
                    else:
                        created_at = "未知时间"
                    
                    # 提取内容
                    if 'text' in post:
                        content = post['text']
                    else:
                        content = ""
                    
                    posts.append(f"[{created_at}] {post['user']['screen_name']}: {content}")
        except Exception:
            continue
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(posts))
    
    return len(posts)


def parse_wechat_moments(json_path, target_name, output_file):
    """解析微信朋友圈内容"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    posts = []
    for post in data:
        try:
            if 'sender' in post:
                if target_name in post['sender']:
                    # 提取发布时间
                    if 'time' in post:
                        timestamp = post['time']
                        if isinstance(timestamp, str):
                            timestamp = int(timestamp)
                        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        date = "未知时间"
                    
                    # 提取内容
                    if 'content' in post:
                        content = post['content']
                    else:
                        content = ""
                    
                    posts.append(f"[{date}] {post['sender']}: {content}")
        except Exception:
            continue
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(posts))
    
    return len(posts)


def main():
    parser = argparse.ArgumentParser(description='社交媒体内容解析工具')
    parser.add_argument('--file', required=True, help='社交媒体内容文件路径')
    parser.add_argument('--target', required=True, help='目标用户名称')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--platform', default='weibo', help='平台：weibo/wechat')
    
    args = parser.parse_args()
    
    try:
        if args.platform == 'weibo':
            count = parse_weibo(args.file, args.target, args.output)
        elif args.platform == 'wechat':
            count = parse_wechat_moments(args.file, args.target, args.output)
        else:
            print('不支持的平台')
            return
        
        print(f'成功解析 {count} 条内容，已保存到 {args.output}')
    except Exception as e:
        print(f'解析失败：{e}')


if __name__ == '__main__':
    main()
