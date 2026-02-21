#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通讯录转换为常用语
"""

import os
import re
import csv


def parse_vcf_file(input_file):
    """
    解析VCF格式的通讯录文件
    
    Args:
        input_file: VCF文件路径
        
    Returns:
        list: 联系人列表，每个元素为(name, phone)元组
    """
    contacts = []
    current_name = None
    current_phones = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 解析姓名
            if line.startswith('FN:'):
                current_name = line[3:].strip()
            elif line.startswith('N:'):
                # N:姓;名;中间名;前缀;后缀
                parts = line[2:].split(';')
                if not current_name and len(parts) >= 2:
                    # 组合姓名：姓+名
                    current_name = ''.join([p for p in parts[:2] if p])
            
            # 解析电话
            elif line.startswith('TEL'):
                # TEL;TYPE=CELL:电话号码 或 TEL:电话号码
                phone_match = re.search(r':(.+)$', line)
                if phone_match:
                    phone = phone_match.group(1).strip()
                    # 清理电话号码中的空格和特殊字符
                    phone = re.sub(r'[\s\-\(\)]', '', phone)
                    if phone:
                        current_phones.append(phone)
            
            # vCard结束标记
            elif line.startswith('END:VCARD'):
                if current_name and current_phones:
                    for phone in current_phones:
                        contacts.append((current_name, phone))
                current_name = None
                current_phones = []
    
    return contacts


def parse_csv_file(input_file):
    """
    解析CSV格式的通讯录文件
    
    预期格式:
    Name,Phone
    张三,13800138000
    或者:
    姓名,电话
    张三,13800138000
    
    Args:
        input_file: CSV文件路径
        
    Returns:
        list: 联系人列表，每个元素为(name, phone)元组
    """
    contacts = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        # 尝试自动检测CSV方言
        sample = f.read(1024)
        f.seek(0)
        
        try:
            dialect = csv.Sniffer().sniff(sample)
        except (csv.Error, Exception):
            dialect = csv.excel
        
        reader = csv.reader(f, dialect)
        
        # 跳过标题行
        headers = next(reader, None)
        
        for row in reader:
            if len(row) >= 2:
                name = row[0].strip()
                phone = row[1].strip()
                # 清理电话号码
                phone = re.sub(r'[\s\-\(\)]', '', phone)
                if name and phone:
                    contacts.append((name, phone))
    
    return contacts


def get_pinyin_abbr(text):
    """
    获取文本的拼音首字母缩写
    
    优先使用pypinyin库（如果可用），否则使用内置映射
    
    Args:
        text: 输入文本
        
    Returns:
        str: 拼音首字母缩写
    """
    # 尝试使用pypinyin库
    try:
        from pypinyin import lazy_pinyin, Style
        pinyin_list = lazy_pinyin(text, style=Style.FIRST_LETTER)
        return ''.join(pinyin_list)
    except ImportError:
        pass
    
    # 使用内置的常用汉字映射
    pinyin_map = {
        '张': 'z', '王': 'w', '李': 'l', '刘': 'l', '陈': 'c',
        '杨': 'y', '黄': 'h', '赵': 'z', '周': 'z', '吴': 'w',
        '徐': 'x', '孙': 's', '马': 'm', '朱': 'z', '胡': 'h',
        '郭': 'g', '何': 'h', '林': 'l', '高': 'g', '罗': 'l',
        '三': 's', '四': 's', '五': 'w', '六': 'l', '七': 'q',
        '八': 'b', '九': 'j', '十': 's', '小': 'x', '大': 'd',
        '明': 'm', '红': 'h', '军': 'j', '强': 'q', '伟': 'w',
        '芳': 'f', '丽': 'l', '娟': 'j', '敏': 'm', '静': 'j',
        '华': 'h', '秀': 'x', '英': 'y', '兰': 'l', '霞': 'x'
    }
    
    abbr = ''
    for char in text:
        if char in pinyin_map:
            abbr += pinyin_map[char]
        elif char.isalpha():
            abbr += char.lower()
    
    return abbr


def generate_phrases_format(contacts):
    """
    生成常用语格式
    
    格式说明:
    - 使用姓名的拼音首字母作为缩写
    - 短语内容为: 姓名 电话号码
    
    Args:
        contacts: 联系人列表
        
    Returns:
        list: 短语列表，每个元素为(abbreviation, phrase)元组
    """
    phrases = []
    
    for name, phone in contacts:
        # 生成缩写：使用拼音首字母
        abbr = get_pinyin_abbr(name)
        
        # 如果没有生成缩写，使用电话后4位
        if not abbr:
            abbr = 'tel' + phone[-4:] if len(phone) >= 4 else 'tel'
        
        # 短语内容：姓名 电话
        phrase = f'{name} {phone}'
        phrases.append((abbr, phrase))
    
    return phrases


def generate_android_format(phrases):
    """
    生成安卓端格式的常用语
    
    格式与自定义短语相同
    
    Args:
        phrases: 短语列表
        
    Returns:
        str: 安卓端格式的文本
    """
    lines = ['[Custom Phrase]']
    lines.append(f'count={len(phrases)}')
    
    for i, (abbr, phrase) in enumerate(phrases, 1):
        lines.append(f'{i}={abbr},{phrase}')
    
    return '\n'.join(lines) + '\n'


def convert_contacts_to_phrases(input_file, output_file):
    """
    将通讯录转换为常用语
    
    Args:
        input_file: 通讯录文件路径 (VCF或CSV)
        output_file: 输出文件路径
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f'输入文件不存在: {input_file}')
    
    # 根据文件扩展名选择解析器
    ext = os.path.splitext(input_file)[1].lower()
    
    if ext == '.vcf':
        contacts = parse_vcf_file(input_file)
    elif ext == '.csv':
        contacts = parse_csv_file(input_file)
    else:
        # 尝试自动检测
        try:
            contacts = parse_vcf_file(input_file)
        except (ValueError, UnicodeDecodeError, Exception) as vcf_error:
            try:
                contacts = parse_csv_file(input_file)
            except (ValueError, UnicodeDecodeError, Exception) as csv_error:
                raise ValueError(f'无法识别的文件格式，请使用.vcf或.csv文件。VCF错误: {vcf_error}, CSV错误: {csv_error}')
    
    if not contacts:
        raise ValueError('没有找到有效的联系人数据')
    
    # 生成短语
    phrases = generate_phrases_format(contacts)
    
    # 生成安卓端格式
    android_content = generate_android_format(phrases)
    
    # 写入输出文件
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(android_content)
    
    print(f'已导入 {len(contacts)} 个联系人')
