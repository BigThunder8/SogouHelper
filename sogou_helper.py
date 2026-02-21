#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜狗输入法辅助工具 (Sogou Input Method Helper Tool)
功能：
1. 将电脑端自定义短语批量转到安卓端
2. 将通讯录内容批量导入常用语
"""

import argparse
import sys
import os
from pc_to_android import convert_pc_to_android
from contacts_to_phrases import convert_contacts_to_phrases


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='搜狗输入法辅助工具 - Sogou Input Method Helper Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例 (Usage Examples):
  
  1. 转换PC自定义短语到安卓端:
     python sogou_helper.py pc-to-android input.txt output.ini
  
  2. 导入通讯录到常用语:
     python sogou_helper.py contacts-to-phrases contacts.vcf output.ini
     python sogou_helper.py contacts-to-phrases contacts.csv output.ini
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # PC到安卓转换命令
    pc_parser = subparsers.add_parser(
        'pc-to-android',
        help='将电脑端自定义短语转换为安卓端格式'
    )
    pc_parser.add_argument('input', help='输入文件路径 (PC自定义短语文件)')
    pc_parser.add_argument('output', help='输出文件路径 (安卓格式)')
    
    # 通讯录到短语转换命令
    contacts_parser = subparsers.add_parser(
        'contacts-to-phrases',
        help='将通讯录导入为常用语'
    )
    contacts_parser.add_argument('input', help='输入文件路径 (VCF或CSV格式)')
    contacts_parser.add_argument('output', help='输出文件路径 (常用语格式)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'pc-to-android':
            print(f'正在转换PC自定义短语: {args.input} -> {args.output}')
            convert_pc_to_android(args.input, args.output)
            print('转换成功！')
            
        elif args.command == 'contacts-to-phrases':
            print(f'正在导入通讯录: {args.input} -> {args.output}')
            convert_contacts_to_phrases(args.input, args.output)
            print('导入成功！')
            
        return 0
        
    except FileNotFoundError as e:
        print(f'错误: 文件未找到 - {e}', file=sys.stderr)
        return 1
    except Exception as e:
        print(f'错误: {e}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
