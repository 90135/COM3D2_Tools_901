# COM3D2_Tools_901

901 的 COM3D2 工具，这次没有国际化

Vibe Coding include :D

## 先决条件

本仓库的所有 .py 文件都需要 Python3 来运行

请自行安装 [Python3](https://www.python.org/downloads/)



### COM3D2文件关键词替换GUI工具.py

通常用于制作差分

本脚本依赖于 [https://github.com/MeidoPromotionAssociation/MeidoSerialization](https://github.com/MeidoPromotionAssociation/MeidoSerialization) 请先下载

安装 [Python3](https://www.python.org/downloads/) 后，双击即可启动

如果不行就 `python .\COM3D2文件关键词替换GUI工具.py`


![图片](https://github.com/user-attachments/assets/d49c5992-1c39-4603-8ea4-e6c9e0294fe5)

![图片](https://github.com/user-attachments/assets/b15ce3cd-060f-4950-93d0-19dea0008fff)



### dcm_songlist_xml_check.py

检查 DanceCameraMotion 插件的 songList 是否正确

DCM 某个版本开始要是 songList 里面混进了非 songList 格式的文件就会打不开歌曲模式

此脚本用于检查有没有不正确的文件在里面的

顺便还能检查 songList 内引用的文件存在不存在

```
# 只检查 XML 格式（默认）
python dcm_songlist_xml_check.py "X:\maid\COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\songList"

# 检查 XML 格式并验证引用的文件是否存在
python dcm_songlist_xml_check.py"X:\maid\COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\songList" --check-files

# 或使用短选项
python dcm_songlist_xml_check.py "X:\maid\COM3D2\Sybaris\UnityInjector\Config\DanceCameraMotion\songList" -c

# 查看帮助
python dcm_songlist_xml_check.py --help
```



## 也可以看看我的其他仓库

- [COM3D2 简明 MOD 教程中文](https://github.com/90135/COM3D2_Simple_MOD_Guide_Chinese)
- [COM3D2 MOD 编辑器](https://github.com/90135/COM3D2_MOD_EDITOR)
- [COM3D2 插件中文翻译](https://github.com/90135/COM3D2_Plugin_Translate_Chinese)
- [90135 的 COM3D2 中文指北](https://github.com/90135/COM3D2_GUIDE_CHINESE)
- [90135 的 COM3D2 脚本收藏集](https://github.com/90135/COM3D2_Scripts_901)
- [90135 的 COM3D2 工具](https://github.com/90135/COM3D2_Tools_901)
