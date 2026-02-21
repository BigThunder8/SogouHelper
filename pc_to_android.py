#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PC端自定义短语转换为安卓端格式
"""

import os
import re


def parse_pc_phrases(input_file):
    """
    解析PC端自定义短语文件
    
    PC端格式示例:
    abbreviation,1=full phrase
    或者简单的格式:
    abbreviation=full phrase
    
    Args:
        input_file: PC端短语文件路径
        
    Returns:
        list: 短语列表，每个元素为(abbreviation, phrase)元组
    """
    phrases = []
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f'输入文件不存在: {input_file}')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # 跳过空行和注释
            if not line or line.startswith('#') or line.startswith(';'):
                continue
            
            # 尝试匹配 "abbreviation,N=phrase" 格式
            match = re.match(r'^([^,=]+),\d+=(.+)$', line)
            if match:
                abbr, phrase = match.groups()
                phrases.append((abbr.strip(), phrase.strip()))
                continue
            
            # 尝试匹配 "abbreviation=phrase" 格式
            if '=' in line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    abbr, phrase = parts
                    phrases.append((abbr.strip(), phrase.strip()))
                    continue
            
            # 尝试匹配 "abbreviation phrase" 格式 (空格或制表符分隔)
            parts = re.split(r'\s+', line, 1)
            if len(parts) == 2:
                phrases.append((parts[0].strip(), parts[1].strip()))
    
    return phrases


def generate_android_format(phrases):
    """
    生成安卓端格式的自定义短语
    
    安卓端格式 (INI格式):
    [Custom Phrase]
    count=N
    1=abbreviation,phrase
    2=abbreviation,phrase
    ...
    
    Args:
        phrases: 短语列表
        
    Returns:
        str: 安卓端格式的文本
    """
    lines = ['[Custom Phrase]']
    lines.append(f'count={len(phrases)}')
    
    for i, (abbr, phrase) in enumerate(phrases, 1):
        # 安卓端格式: N=abbreviation,phrase
        lines.append(f'{i}={abbr},{phrase}')
    
    return '\n'.join(lines) + '\n'


def convert_pc_to_android(input_file, output_file):
    """
    将PC端自定义短语转换为安卓端格式
    
    Args:
        input_file: PC端短语文件路径
        output_file: 输出文件路径
    """
    # 解析PC端短语
    phrases = parse_pc_phrases(input_file)
    
    if not phrases:
        raise ValueError('没有找到有效的短语数据')
    
    # 生成安卓端格式
    android_content = generate_android_format(phrases)
    
    # 写入输出文件
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(android_content)
    
    print(f'已转换 {len(phrases)} 条短语')
