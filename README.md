# 自动视频剪辑工具

这是一个自动将图片转换为视频的Python工具，支持图片缩放效果和背景音乐。

## 功能特点

- 自动读取指定目录下的图片文件
- 每张图片显示2秒
- 支持图片缩放效果（从100%到120%）
- 自动添加背景音乐
- 支持批量处理（每10张图片生成一个视频）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 确保已安装所有依赖
2. 运行程序：
```bash
python auto_video.py
```

## 输出

生成的视频文件将保存在 `output_videos` 目录下，文件名格式为 `output_video_1.mp4`、`output_video_2.mp4` 等。

## 注意事项

- 支持的图片格式：PNG、JPG、JPEG
- 图片将按文件名排序处理
- 确保有足够的磁盘空间存储生成的视频文件 