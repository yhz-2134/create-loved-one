#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
照片分析工具
提取照片的EXIF信息、时间线和场景
"""

import argparse
import os
from datetime import datetime
from PIL import Image
import exifread


def get_exif_data(image_path):
    """提取照片的EXIF信息"""
    exif_data = {}
    
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
        
        # 提取时间
        if 'Image DateTime' in tags:
            exif_data['date_time'] = str(tags['Image DateTime'])
        
        # 提取GPS信息
        if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
            # 简单处理GPS坐标
            lat = tags['GPS GPSLatitude']
            lon = tags['GPS GPSLongitude']
            exif_data['gps'] = f"{lat}, {lon}"
        
        # 提取相机信息
        if 'Image Make' in tags:
            exif_data['camera_make'] = str(tags['Image Make'])
        if 'Image Model' in tags:
            exif_data['camera_model'] = str(tags['Image Model'])
            
    except Exception as e:
        exif_data['error'] = str(e)
    
    return exif_data


def analyze_photo(photo_path):
    """分析单张照片"""
    result = {
        'path': photo_path,
        'exif': get_exif_data(photo_path)
    }
    
    # 获取文件修改时间作为备选
    try:
        mtime = os.path.getmtime(photo_path)
        result['modified_time'] = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        pass
    
    return result


def analyze_directory(directory):
    """分析目录中的所有照片"""
    photos = []
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp')
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                photo_path = os.path.join(root, file)
                try:
                    photo_data = analyze_photo(photo_path)
                    photos.append(photo_data)
                except Exception as e:
                    print(f"分析 {photo_path} 失败: {e}")
    
    return photos


def generate_timeline(photos):
    """生成时间线"""
    timeline = []
    
    for photo in photos:
        # 优先使用EXIF时间，其次使用文件修改时间
        date_time = None
        if 'date_time' in photo['exif']:
            try:
                date_time = datetime.strptime(photo['exif']['date_time'], '%Y:%m:%d %H:%M:%S')
            except Exception:
                pass
        
        if not date_time and 'modified_time' in photo:
            try:
                date_time = datetime.strptime(photo['modified_time'], '%Y-%m-%d %H:%M:%S')
            except Exception:
                pass
        
        if date_time:
            timeline.append({
                'date': date_time.strftime('%Y-%m-%d'),
                'time': date_time.strftime('%H:%M:%S'),
                'path': photo['path'],
                'exif': photo['exif']
            })
    
    # 按时间排序
    timeline.sort(key=lambda x: x['date'] + ' ' + x['time'])
    
    return timeline


def main():
    parser = argparse.ArgumentParser(description='照片分析工具')
    parser.add_argument('--dir', required=True, help='照片目录路径')
    parser.add_argument('--output', required=True, help='输出文件路径')
    
    args = parser.parse_args()
    
    # 分析照片
    photos = analyze_directory(args.dir)
    timeline = generate_timeline(photos)
    
    # 生成输出
    output_lines = []
    output_lines.append(f"分析到 {len(photos)} 张照片")
    output_lines.append("\n时间线：")
    
    for item in timeline:
        output_lines.append(f"[{item['date']} {item['time']}] {os.path.basename(item['path'])}")
        if 'gps' in item['exif']:
            output_lines.append(f"  地点: {item['exif']['gps']}")
        if 'camera_model' in item['exif']:
            output_lines.append(f"  相机: {item['exif']['camera_model']}")
        output_lines.append("")
    
    # 写入输出文件
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f'分析完成，已保存到 {args.output}')


if __name__ == '__main__':
    main()
