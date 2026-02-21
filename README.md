# SogouHelper - 搜狗输入法辅助工具

搜狗输入法辅助工具：
1. **将电脑端自定义短语批量转到安卓端**
2. **将通讯录内容批量导入常用语**，解决通讯录词库功能下架的问题

## 功能特性

### 1. PC到安卓自定义短语转换
- 支持多种PC端短语格式
- 自动转换为安卓端兼容的INI格式
- 保留所有短语和缩写映射

### 2. 通讯录导入常用语
- 支持VCF (vCard)格式
- 支持CSV格式
- 自动生成拼音缩写
- 将联系人姓名和电话号码转换为常用语

## 安装

本工具使用Python 3编写，无需额外依赖库。

```bash
# 克隆仓库
git clone https://github.com/BigThunder8/SogouHelper.git
cd SogouHelper

# 确保Python 3已安装
python3 --version
```

## 使用方法

### 1. PC端自定义短语转安卓端

```bash
python3 sogou_helper.py pc-to-android <输入文件> <输出文件>
```

**示例：**
```bash
python3 sogou_helper.py pc-to-android examples/pc_phrases.txt output_android.ini
```

**PC端支持的输入格式：**

```
# 格式1: abbreviation,N=phrase
email,1=example@email.com

# 格式2: abbreviation=phrase  
dz=地址

# 格式3: abbreviation phrase (空格分隔)
wx 微信
```

**安卓端输出格式：**

```ini
[Custom Phrase]
count=3
1=email,example@email.com
2=dz,地址
3=wx,微信
```

### 2. 通讯录导入常用语

```bash
python3 sogou_helper.py contacts-to-phrases <输入文件> <输出文件>
```

**示例：**

```bash
# 从VCF文件导入
python3 sogou_helper.py contacts-to-phrases examples/contacts.vcf output_contacts.ini

# 从CSV文件导入
python3 sogou_helper.py contacts-to-phrases examples/contacts.csv output_contacts.ini
```

**VCF格式示例：**

```
BEGIN:VCARD
VERSION:3.0
FN:张三
TEL;TYPE=CELL:13800138000
END:VCARD
```

**CSV格式示例：**

```csv
姓名,电话
张三,13800138000
李四,13900139000
```

**输出格式：**

```ini
[Custom Phrase]
count=2
1=zs,张三 13800138000
2=ls,李四 13900139000
```

## 导入到安卓搜狗输入法

1. 将生成的`.ini`文件传输到安卓设备
2. 打开搜狗输入法设置
3. 进入"词库管理" → "自定义短语"
4. 选择"导入"，选择生成的`.ini`文件
5. 确认导入

## 文件说明

- `sogou_helper.py` - 主程序入口
- `pc_to_android.py` - PC到安卓转换模块
- `contacts_to_phrases.py` - 通讯录到常用语转换模块
- `examples/` - 示例文件目录
  - `pc_phrases.txt` - PC端短语示例
  - `contacts.vcf` - VCF格式通讯录示例
  - `contacts.csv` - CSV格式通讯录示例

## 注意事项

1. 确保输入文件编码为UTF-8
2. 电话号码会自动清理空格、括号等特殊字符
3. CSV文件第一行为标题行（姓名,电话）
4. 生成的文件可以直接导入搜狗输入法安卓版

## 常见问题

**Q: 为什么需要这个工具？**  
A: 搜狗输入法安卓版取消了通讯录词库功能，此工具可以将通讯录转换为自定义短语，方便输入联系人信息。

**Q: 支持哪些联系人格式？**  
A: 支持标准的VCF (vCard)格式和CSV格式。

**Q: 生成的缩写是如何确定的？**  
A: 使用姓名的拼音首字母作为缩写（针对常见姓氏），如果无法生成则使用电话后4位。

**Q: 可以自定义缩写吗？**  
A: 可以在生成后手动编辑输出文件，修改缩写部分。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 作者

BigThunder8
