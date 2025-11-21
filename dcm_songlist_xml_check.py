#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Function: 检查指定文件夹内的 .xml 文件格式是否正确，是否为 songList 格式，以及引用的文件是否存在
# Author: Claude Sonnet 4.5 & 90135
# Creation date: 2025-11-21
# Version: 2025-11-21
# License: Bsd-3

import os
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import List, Tuple, Set

class XMLChecker:
    def __init__(self, folder_path: str, check_files: bool = True):
        self.folder_path = Path(folder_path)
        self.song_folder = self.folder_path.parent / "song"
        self.check_files = check_files
        self.errors = []
        self.warnings = []
        
    def check_all_xml_files(self) -> bool:
        """检查文件夹内所有 XML 文件"""
        xml_files = list(self.folder_path.glob("*.xml"))
        
        if not xml_files:
            print(f"❌ 在 {self.folder_path} 中没有找到 XML 文件")
            return False
        
        print(f"找到 {len(xml_files)} 个 XML 文件\n")
        
        all_valid = True
        for xml_file in xml_files:
            print(f"{'='*60}")
            print(f"检查文件: {xml_file.name}")
            print(f"{'='*60}")
            
            if not self.check_xml_file(xml_file):
                all_valid = False
            
            print()
        
        return all_valid
    
    def check_xml_file(self, xml_path: Path) -> bool:
        """检查单个 XML 文件"""
        self.errors = []
        self.warnings = []
        
        # 1. 检查 XML 格式
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            print("✓ XML 格式正确")
        except ET.ParseError as e:
            self.errors.append(f"XML 解析错误: {e}")
            self._print_results()
            return False
        except Exception as e:
            self.errors.append(f"读取文件错误: {e}")
            self._print_results()
            return False
        
        # 2. 检查根元素
        if root.tag not in ["SongList", "DanceList"]:
            self.errors.append(f"根元素应为 'SongList' 或 'DanceList'，当前为 '{root.tag}'")
        
        # 3. 检查每个 song/dance 元素
        songs = root.findall("song") + root.findall("dance")
        
        if not songs:
            self.warnings.append("未找到 song 或 dance 元素")
        else:
            print(f"✓ 找到 {len(songs)} 个 song/dance 元素")
        
        for idx, song in enumerate(songs, 1):
            label = song.get("label", f"未命名-{idx}")
            print(f"\n检查 [{label}]:")
            self._check_song_element(song, label)
        
        # 输出结果
        self._print_results()
        
        return len(self.errors) == 0
    
    def _check_song_element(self, song_elem: ET.Element, label: str):
        """检查 song 元素及其引用的文件"""
        # 获取 folder 路径
        folder_elem = song_elem.find("folder")
        if folder_elem is None or not folder_elem.text:
            self.errors.append(f"  [{label}] 缺少 folder 元素或值为空")
            return
        
        folder_path = self.song_folder / folder_elem.text
        
        # 如果不检查文件，只验证 folder 元素存在即可
        if not self.check_files:
            print(f"  ✓ folder: {folder_elem.text}")
            return
        
        # 需要检查的文件元素列表
        file_elements = [
            "bgm", "bgmParallel", "customMotion", "motion", "customMorph",
            "stageObject", "changePrimitive", "changeBg", "changeFade",
            "changeItem", "changeDress", "changeUndress", "changeMaidMenu",
            "changeMaidVoice", "changeMaidPrefab", "changePrefab",
            "changeParticle", "changeLight", "changeText", "changeMessage",
            "changeModel", "changePng", "changeImageEffects", "changeShapeKey",
            "changeDressBone", "changeLookAt", "changeDressGrip", "movePng",
            "moveModel", "mobCrowd", "changeSe", "bukkake"
        ]
        
        checked_files = set()
        
        # 检查顶层文件元素
        for elem_name in file_elements:
            elem = song_elem.find(elem_name)
            if elem is not None and elem.text:
                self._check_file_exists(folder_path, elem.text, elem_name, label, checked_files)
        
        # 检查 maid 元素
        for maid_idx, maid in enumerate(song_elem.findall("maid")):
            slot_no = maid.get("slotNo", str(maid_idx))
            self._check_maid_element(maid, folder_path, label, slot_no, checked_files)
        
        # 检查 man 元素
        for man_idx, man in enumerate(song_elem.findall("man")):
            slot_no = man.get("slotNo", str(man_idx))
            self._check_man_element(man, folder_path, label, slot_no, checked_files)
    
    def _check_maid_element(self, maid_elem: ET.Element, folder_path: Path, 
                           label: str, slot_no: str, checked_files: Set[str]):
        """检查 maid 元素中引用的文件"""
        maid_file_elements = [
            "customAnimation", "morph", "wneMorph", "wneLip", "face", 
            "faceOfficial", "mouth", "pose", "bone", "move", "lyrics",
            "mabataki", "eyes", "voice", "piston", "bindBone"
        ]
        
        for elem_name in maid_file_elements:
            elem = maid_elem.find(elem_name)
            if elem is not None and elem.text:
                self._check_file_exists(folder_path, elem.text, 
                                      f"maid[{slot_no}]/{elem_name}", 
                                      label, checked_files)
    
    def _check_man_element(self, man_elem: ET.Element, folder_path: Path,
                          label: str, slot_no: str, checked_files: Set[str]):
        """检查 man 元素中引用的文件"""
        man_file_elements = ["pose", "move", "bindBone", "chinkoCtrl"]
        
        for elem_name in man_file_elements:
            elem = man_elem.find(elem_name)
            if elem is not None and elem.text:
                self._check_file_exists(folder_path, elem.text,
                                      f"man[{slot_no}]/{elem_name}",
                                      label, checked_files)
    
    def _check_file_exists(self, base_path: Path, filename: str, 
                          elem_name: str, label: str, checked_files: Set[str]):
        """检查文件是否存在"""
        if not filename:
            return
        
        file_path = base_path / filename
        file_key = str(file_path)
        
        # 避免重复检查
        if file_key in checked_files:
            return
        checked_files.add(file_key)
        
        if not file_path.exists():
            self.errors.append(f"  [{label}] {elem_name}: 文件不存在 - {file_path}")
        else:
            print(f"  ✓ {elem_name}: {filename}")
    
    def _print_results(self):
        """打印检查结果"""
        print("\n" + "="*60)
        
        if self.warnings:
            print("⚠️  警告:")
            for warning in self.warnings:
                print(f"  {warning}")
            print()
        
        if self.errors:
            print("❌ 错误:")
            for error in self.errors:
                print(f"  {error}")
            print("\n检查结果: 失败")
        else:
            print("✅ 检查结果: 通过")
        
        print("="*60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='检查 XML 文件格式和引用文件是否存在',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 只检查 XML 格式
  python xml_checker.py ./config
  
  # 检查 XML 格式并验证文件存在
  python xml_checker.py ./config --check-files
  
  # 或使用短选项
  python xml_checker.py ./config -c
        '''
    )
    
    parser.add_argument('folder', help='包含 XML 文件的文件夹路径')
    parser.add_argument('-c', '--check-files', action='store_true',
                       help='检查引用的文件是否存在（默认不检查）')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.folder):
        print(f"❌ 文件夹不存在: {args.folder}")
        sys.exit(1)
    
    if not os.path.isdir(args.folder):
        print(f"❌ 路径不是文件夹: {args.folder}")
        sys.exit(1)
    
    print(f"检查模式: {'验证 XML 格式 + 文件存在' if args.check_files else '仅验证 XML 格式'}")
    print()
    
    checker = XMLChecker(args.folder, check_files=args.check_files)
    success = checker.check_all_xml_files()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()