# COM3D2_Tools_901

901 的 COM3D2 工具，这次没有国际化

Vibe Coding include :D

## 先决条件

本仓库的所有 .py 文件都需要 Python3 来运行

请自行安装 [Python3](https://www.python.org/downloads/)

请尝试 Python 3.12 及以上版本


### COM3D2文件关键词替换GUI工具.py

通常用于制作差分

本脚本依赖于 [https://github.com/MeidoPromotionAssociation/MeidoSerialization](https://github.com/MeidoPromotionAssociation/MeidoSerialization) 请先下载

安装 [Python3](https://www.python.org/downloads/) 后，双击即可启动

如果不行就 `python .\COM3D2文件关键词替换GUI工具.py`

<br>

替换 MOD 文件内的关键词时，会将 MOD 文件先转换成 JSON 再进行替换，需要注意 MeidoSerialization 转换的 JSON 文件是紧凑格式，建议先打开一个确认格式。

假设我想要批量替换 mate 文件中的 `_MatcapValue` 的值，首先切换到格式转换功能，转换一个 `.mate` 为 `.mate.json` ，然后打开 `.mate.json` ，搜索 `_MatcapValue`

它可能长这样
```
{"TypeName":"f","PropName":"_MatcapValue","Number":0.5}
```

<br>

于是我们在替换里面就要写，查找关键词：
```
{"TypeName":"f","PropName":"_MatcapValue","Number":0.5}
```
替换为：
```
{"TypeName":"f","PropName":"_MatcapValue","Number":0.7}
```

如果你只写一个 0.5，那么其他 0.5 也会被替换的，这样能保证精确替换。

<br>

<img width="600" height="600" alt="图片" src="https://github.com/user-attachments/assets/e39a1aee-ccc0-4c6e-ac0a-efdd82290b9e" />

<img width="600" height="600" alt="图片" src="https://github.com/user-attachments/assets/f1a29729-4363-48f9-8c05-95c320b8e947" />

<img width="600" height="600" alt="图片" src="https://github.com/user-attachments/assets/b13baa2e-fd18-4848-bb39-9efd834f5737" />

<img width="600" height="600" alt="图片" src="https://github.com/user-attachments/assets/f2613251-d241-499f-a08d-e2d9a2f8fbb0" />


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
