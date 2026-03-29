"""
测距脚本：读取 detection_result.json,计算距离
"""

import json
import os




#配置参数

# 检测结果文件(模型检测后导出的json文件路径)
JSON_PATH = '.json'
# 相机参数
FOCAL_LENGTH = 800  # 像素焦距(未定)
# 物体真实高度(等官方数据或是自己测)
OBJECT_HEIGHTS = {
    0: 0.05,    # coin
    1: 0.5,     # car
    2: 1.7,     # people
}
# 类别名称
CLASS_NAMES = {
    0: 'coin',
    1: 'car',
    2: 'people',
}




# 距离计算 

def calculate_distance(bbox_height, real_height, focal_length):
    """距离 = (真实高度 * 焦距) / 像素高度"""
    if bbox_height <= 0:
        return None
    return (real_height * focal_length) / bbox_height

# ==================== 主程序 ====================

def main():
    distances = []
    # 读取JSON文件
    if not os.path.exists(JSON_PATH):
        print(f"文件不存在: {JSON_PATH}")
        return distances
    #将json文件中的数据加载到data变量中
    with open(JSON_PATH, 'r') as f:
        data = json.load(f)
    
    # 遍历每张图片的检测结果
    for img_info in data:
        img_name = img_info['filename']
        print(f"\n图片: {img_name}")
        # 遍历每个检测框，计算距离
        for det in img_info['bbox']:
            x1, y1, x2, y2, score, cls_id = det[:6]
            bbox_height = y2 - y1
            real_height = OBJECT_HEIGHTS.get(cls_id, 1.7)
            
            distance = calculate_distance(bbox_height, real_height, FOCAL_LENGTH)
            class_name = CLASS_NAMES.get(cls_id, 'unknown')
            
            if distance:
                print(f"  {class_name}(ID:{cls_id}): {distance:.2f}米 (框高:{bbox_height}px, 置信度:{score:.2f})")
                distances.append(distance)
            else:
                print(f"  {class_name}: 无法计算距离")
    return distances

# 运行主程序
if __name__ == "__main__":
    main()
