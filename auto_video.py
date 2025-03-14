import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, VideoFileClip
from PIL import Image
import numpy as np
from pathlib import Path

def resize_image(img_path, target_size=(1920, 1080)):
    """调整图片尺寸，保持宽高比"""
    # 使用PIL打开图片并转换为RGB模式
    img = Image.open(img_path).convert('RGB')
    
    # 计算缩放比例
    w, h = img.size
    scale = min(target_size[0]/w, target_size[1]/h)
    new_size = (int(w*scale), int(h*scale))
    
    # 调整图片大小
    img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # 创建黑色背景
    background = Image.new('RGB', target_size, (0, 0, 0))
    
    # 计算居中位置
    x_offset = (target_size[0] - new_size[0]) // 2
    y_offset = (target_size[1] - new_size[1]) // 2
    
    # 将调整后的图片放在背景中央
    background.paste(img, (x_offset, y_offset))
    
    # 转换为numpy数组并确保类型正确
    return np.array(background).astype(np.uint8)

def create_zoom_effect(clip, zoom_factor=1.1):
    """创建缩放效果"""
    def zoom(t):
        # 使用更平滑的缩放曲线
        progress = t / clip.duration
        zoom_ratio = 1 + (zoom_factor - 1) * progress
        return zoom_ratio
    
    return clip.resize(zoom)

def process_images_to_video(image_dir, audio_path, output_dir, batch_size=10):
    """处理图片并生成视频"""
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有图片文件
    image_files = sorted([f for f in os.listdir(image_dir) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    if not image_files:
        print(f"警告：在目录 {image_dir} 中没有找到图片文件！")
        return
    
    # 按批次处理图片
    for i in range(0, len(image_files), batch_size):
        batch_files = image_files[i:i + batch_size]
        clips = []
        
        for img_file in batch_files:
            img_path = os.path.join(image_dir, img_file)
            print(f"处理图片：{img_path}")
            
            try:
                # 调整图片尺寸
                img = resize_image(img_path)
                
                # 创建图片片段，确保持续2秒
                clip = ImageClip(img, duration=2)
                
                # 添加缩放效果
                clip = create_zoom_effect(clip)
                
                clips.append(clip)
            except Exception as e:
                print(f"处理图片 {img_path} 时出错: {str(e)}")
                continue
        
        if not clips:
            print("没有成功处理的图片，跳过此批次")
            continue
        
        try:
            # 连接所有片段
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # 添加音频
            audio = AudioFileClip(audio_path)
            # 剪切音频以匹配视频长度
            audio = audio.subclip(0, final_clip.duration)
            final_clip = final_clip.set_audio(audio)
            
            # 生成输出文件名
            output_file = os.path.join(output_dir, f'output_video_{i//batch_size + 1}.mp4')
            print(f"生成视频：{output_file}")
            
            # 导出视频，使用高质量设置
            final_clip.write_videofile(
                output_file,
                fps=30,
                codec='libx264',
                audio_codec='aac',
                bitrate='8000k',
                audio_bitrate='192k',
                threads=4,
                preset='medium',
                ffmpeg_params=[
                    '-pix_fmt', 'yuv420p',  # 确保视频兼容性
                    '-profile:v', 'high',    # 使用高质量配置文件
                    '-level', '4.0'          # 设置兼容性级别
                ]
            )
            
            # 验证生成的视频
            print(f"验证视频时长...")
            generated_video = VideoFileClip(output_file)
            print(f"视频时长: {generated_video.duration} 秒")
            generated_video.close()
            
        except Exception as e:
            print(f"生成视频时出错: {str(e)}")
            continue
        finally:
            # 清理资源
            try:
                final_clip.close()
                audio.close()
                for clip in clips:
                    clip.close()
            except:
                pass

if __name__ == "__main__":
    # 设置路径
    image_dir = "input_images"  # 图片输入目录
    audio_path = "background_music.m4a"  # 背景音乐文件
    output_dir = "output_videos"  # 输出视频目录
    
    # 检查文件和目录是否存在
    if not os.path.exists(image_dir):
        print(f"错误：输入图片目录 {image_dir} 不存在！")
        exit(1)
    
    if not os.path.exists(audio_path):
        print(f"错误：背景音乐文件 {audio_path} 不存在！")
        exit(1)
    
    # 处理视频
    process_images_to_video(image_dir, audio_path, output_dir) 