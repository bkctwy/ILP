# ILP

## **请移步[使用C++编写的新版本](https://github.com/bkctwy/ILP-Cpp)**

## 关于ILP
本项目名称来源于动漫作品「魔法禁书目录」中的「禁书目录」（Index-Librorum-Prohibitorum）的缩写。意指本程序的功能是获取「禁书」。

「ILP」可以有多个含义，包括：

~~(ILP无确切的含义，选择一个你喜欢的就好)~~

- Internet Literature Puller（互联网文学抓取器）
- Ingenious Literature Picker（巧妙文学选择器）
- Internet Literature Profiler（互联网文学剖析器）

## 介绍

此项目支持多个小说网站内容爬取，包括：
- [x] [番茄免费小说](https://fanqienovel.com "番茄免费小说")
    - [x] 标题
    - [x] 正文
    - [x] 作者
    - [ ] 封面
- [ ] [起点中文网](https://qidian.com "起点中文网")
    - [x] 标题
    - [ ] 正文
    - [x] 作者
    - [x] 封面
- [x] [飞卢小说](https://faloo.com "飞卢小说")
    - [x] 标题
    - [x] 正文
    - [x] 作者
    - [ ] 封面
- [ ] 更多...

## 特性
- 使用协程
- 断点续传
- 进度显示
- 缓存目录到数据库
- 保存为多章节文件

## TODO
- [ ] 支持选择爬取范围
- [ ] 支持单文件输出
- [ ] 支持缓存目录到Excel文件
- [ ] 支持缓存目录到Redis
- [x] ~~支持跨平台（当前未测试在Mac OS系统上是否可运行）~~

## 使用

### 从源代码运行

#### 运行
1. 克隆本项目`git clone https://github.com/bkctwy/ILP`
2. 切换到项目目录`cd ILP`
3. 安装依赖`pip install -r requirements.txt`
4. 运行`python ILP.py --help`获取帮助信息


### ~~使用二进制文件（Windows And Linux）~~
**暂不提供二进制文件，请从源代码运行。**

#### Windows
1. 从Github Actions页面下载压缩包（ILP-windows-latest-{commit-id}）
2. 解压
3. 运行`ILP-windows-latest-{commit-id}.exe --help`获取帮助

#### Linux
1. 从Github Actions页面下载压缩包（ILP-ubuntu-latest-{commit-id}）
2. 解压
3. 运行`ILP-ubuntu-latest-{commit-id} --help`获取帮助

## 配置
```json
{
    "PATHS": {                             // 路径配置
        "DATA_PATH": "./data",             // 总数据目录
        "NOVELS_PATH": "novels",           // 小说数据目录
        "LOGS_PATH": "logs",               // 日志目录
        "POSTERS_PATH": "posters",         // 封面图片目录
        "DB_PATH": "cache.db"              // 数据库文件路径
    },
    "MAX_WORKERS": 7,                      // 最大协程数(最好不要大于10)
    "SLEEP_TIME": 5,                       // 请求间隔(最好不要小于3)
}
```

## 注意事项
- 请不要滥用本程序，且用且珍惜
- 用户使用本程序造成的一切后果请自行承担
- 通过本程序爬取的小说需遵守相应网站的版权声明
- 本程序仅供学习交流使用，请勿用于商业用途
- 本项目是本人第一个真正意义上的Python项目，可能存在许多问题，还请批评指正
