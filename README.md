# [AAAI 2022] FCA: Learning a 3D Full-coverage Vehicle Camouflage for Multi-view Physical Adversarial Attack
# 三维多视角车辆反识别对抗迷彩生成框架

## fork目的
 1. 原来项目的主要问题：1）环境安装困难，尤其是渲染器的安装；2）没有使用指导；3）没有数据集制作指导；4）基本无人维护；
 2. 因此，这个fork主要解决这几个问题；问题1）和问题3）是非常困难的，然而，我这里基本打通了，所以，我尽量将整个过程清晰地分享给大家；有问题大家再互相交流。

## 环境安装
pip install -r requirements.txt

3D Renderer安装指导：
https://winterwindwang.github.io/2021/07/22/nerual_rendered_build.html

下载数据集，从百度网盘或google drive上下载：
百度网盘：（提取码：dual）
https://pan.baidu.com/s/1m2dACufqcRb-uL2JYGZxkA#list/path=%2F
Google Drive：
https://drive.google.com/drive/folders/1vspvRxnZ3shOV4kM5ELcO9-xztapBThS

## 代码使用指导
### 训练前，要注意参数设置
1. 要设置车辆模型存在位置：
       parser.add_argument('--obj_file', type=str, default='carassets/audi_et_te.obj', help='3d car model obj')
       parser.add_argument('--faces', type=str, default='carassets/exterior_face.txt', help='exterior_face file  (exterior_face, all_faces)')
2. 设置训练数据集的位置：
       parser.add_argument('--datapath', type=str, default='F:/PythonPro/DualAttentionAttack/data/', help='data path')
### 执行训练：python train_camouflage_yolov3.py
### 训练过程中，注意查看loss是否正常显示。训练过程中的中介结果存放在logs/epoch-x-。。。。。/文件夹下面，里面会有texture.png和test_total.png
texture.png是当前的车辆渲染结果，test_total.png是渲染车辆叠加环境的结果，可以查看这两张图片，查看生成结果是否存在异常。
### 训练结束后，生成的结果是：logs/epoch-x-。。。。。/texture.npy
将此npy文件复制： cp logs/epoch-x-。。。。。/texture.npy textures/texture_camouflage.npy
用于下面步骤中，生成纹理
### 使用训练结果测试和生成纹理：python generated_and_test.py
生成的结果，保存在savedImage/文件夹下
## 实际效果测试
将生成的纹理图片打印出来，粘贴到车体上；
使用yolo系列模型对车进行检测，查看纹理是否欺骗yolo，使其不能检测到车辆。

## 数据集制作指导
### 前置条件：
1. 编译安装carlaUE4，以便能够启动carlaUE4 Editor；这一步需要在windows上完成，因为carlaUE4 Editor启动后有图形界面。
2. 制作车辆模型，模型的格式是fbx，这个车辆既是被用来进行纹理生成的，生成的纹理将能够将车辆对于OD检测系统隐身；
3. 编辑此fbx模型，以便能够导入carlaUE4；包括设置车辆模型中，对车轮的旋转方向和移动等进行约束等；
4. 重新导出fbx模型，然后导入到carlaUE4中；包括创建车辆蓝图、修改车轮尺寸等等。
### 创建数据集
1. 在carla中制作vehicle_manual_control_with_customized_camera.py, 用于驱动车辆在carla中运行。
2. 采用自己导入的车辆模型，使其在carlaUE4中运行起来，并采集图片，生成携带相机和车辆全局位置（transform）的npy文件和图片文件。
3. 制作每张图片的mask.png，既：将图片中的车辆的RGB使用白色（255,255,255）替代，其他部分采用黑色（0，0，0）替代
4. 制作每张图片的label，yolo格式。
5. 将数据集分割成train, train_new, masks, label, test等
### 将车辆模型和数据集加入FCA代码中；
1. 将fbx格式车辆模型转换为obj模型，并导入到FCA中，执行训练可能报显存不足，那么就需要通过blender压缩obj文件。
2. 将数据集导入FCA代码中。
3. 修改代码配置，执行训练

## Overview
This is the official implementation and case study of the Full-coverage Vehicle Camouflage(FCA) method proposed in our AAAI 2022 paper [FCA: Learning a 3D Full-coverage Vehicle Camouflage for Multi-view Physical Adversarial Attack](https://arxiv.org/abs/2109.07193). 

## Abstract
Physical adversarial attacks in object detection have attracted increasing attention. However, most previous works focus on hiding the objects from the detector by generating an individual adversarial patch, which only covers the planar part of the vehicle’s surface and fails to attack the detector in physical scenarios for multi-view, long-distance and partially occluded objects. To bridge the gap between digital attacks and physical attacks, we exploit the full 3D vehicle surface to propose a robust Full-coverage Camouflage Attack (FCA) to fool detectors. Specifically, we first try rendering the nonplanar camouflage texture over the full vehicle surface. To mimic the real-world environment conditions, we then introduce a transformation function to transfer the rendered camouflaged vehicle into a photo realistic scenario. Finally, we design an efficient loss function to optimize the camouflage texture. Experiments show that the full-coverage camouflage attack can not only outperform state-of-the-art methods under various test cases but also generalize to different environments, vehicles, and object detectors. 

## Framework
![image-20211209204327675](https://gitee.com/freeneuro/PigBed/raw/master/img/image-20211209204327675.png)

## Cases of Digital Attack

### Multi-view Attack: Carmear distance is 3

<table frame=void cellspacing="0" cellpadding="0">
    <tr>
      <td></td>
      <td>Elevation 0</td>
      <td>Elevation 30</td>
      <td>Elevation 50</td>
    </tr>
  <tr>
    <td>Original</td>
    <td><center> <img src = 'assets/distance_3_elevation_0_ori_pred.gif?raw=true'/></center></td>
        <td><center> <img src = 'assets/distance_3_elevation_30_ori_pred.gif?raw=true'/></center></td>
    <td><center> <img src = 'assets/distance_3_elevation_50_ori_pred.gif?raw=true'/></center></td>
  </tr>
    <tr>
    <td>FCA</td>
    <td><center><img src = 'assets/distance_3_elevation_0_adv_pred.gif?raw=true'/></center></td>
    <td><center><img src = 'assets/distance_3_elevation_30_adv_pred.gif?raw=true'/></center></td>    
    <td><center><img src = 'assets/distance_3_elevation_50_adv_pred.gif?raw=true'/></center></td>
  </tr>
</table>


### Multi-view Attack: Carmear distance is 5  

<table border=0>
    <tr>
      <td></td>
      <td>Elevation 20</td>
      <td>Elevation 40</td>
      <td>Elevation 50</td>
    </tr>
   <tr>
      <td>Original</td>
    <td><center> <img src = 'assets/distance_5_elevation_20_ori_pred.gif?raw=true'/></center></td>
     <td><center> <img src = 'assets/distance_5_elevation_40_ori_pred.gif?raw=true'/></center></td>
    <td><center> <img src = 'assets/distance_5_elevation_50_ori_pred.gif?raw=true'/></center></td>
  </tr>
    <tr>
     <td>FCA</td>
    <td><center><img src = 'assets/distance_5_elevation_20_adv_pred.gif?raw=true'/></center></td>
    <td><center><img src = 'assets/distance_5_elevation_40_adv_pred.gif?raw=true'/></center></td> 
    <td><center><img src = 'assets/distance_5_elevation_50_adv_pred.gif?raw=true'/></center></td>
  </tr>
</table>


### Multi-view Attack: Carmear distance is 10

<table>
    <tr>
      <td></td>
      <td>Elevation 30</td>
      <td>Elevation 40</td>
      <td>Elevation 50</td>
    </tr>
    <tr>
      <td>Original</td>
    <td><center> <img src = 'assets/distance_10_elevation_30_ori_pred.gif?raw=true'/></center></td>
    <td><center> <img src = 'https://github.com/idrl-lab//Full-coverage-camouflage-adversarial-attack/blob/gh-pages/assets/distance_10_elevation_40_ori_pred.gif?raw=true'/></center></td>
    <td><center> <img src = 'assets/distance_10_elevation_50_ori_pred.gif?raw=true'/></center></td>
  </tr>
    <tr>
    <td>FCA</td>
    <td><center><img src = 'assets/distance_10_elevation_30_adv_pred.gif?raw=true'/></center></td>
    <td><center><img src = 'https://github.com/idrl-lab/Full-coverage-camouflage-adversarial-attack/blob/gh-pages/assets/distance_10_elevation_40_adv_pred.gif?raw=true'/></center></td>
    <td><center><img src = 'assets/distance_10_elevation_50_adv_pred.gif?raw=true'/></center></td>
  </tr>
</table>

### Multi-view Attack: different distance, elevation and azimuth

<table>
  <tr>
   <td>Original</td>
  <td><center> <img src = 'assets/camera_distance_5_elevation_10_57_ori.png?raw=true' width="100" /></center></td>
    <td><center><img src = 'assets/camera_distance_5_elevation_30_66_ori.png?raw=true' width="100" /> </center></td>
      <td><center><img src = 'assets/camera_distance_10_elevation_0_135_ori.png?raw=true' width="100" /> </center></td>
    <td><center> <img src = 'assets/camera_distance_10_elevation_20_177_ori.png?raw=true' width="100" /> </center></td>
      <td><center>  <img src = 'assets/camera_distance_15_elevation_20_330_ori.png?raw=true' width="100" /> </center></td>
    <td><center><img src = 'assets/camera_distance_15_elevation_50_327_ori.png?raw=true' width="100" /></center></td>
  </tr>
  <tr>
    <td>FCA</td>
  <td><center> <img src = 'assets/camera_distance_5_elevation_10_57_adv.png?raw=true' width="100" /></center></td>
    <td><center><img src = 'assets/camera_distance_5_elevation_30_66_adv.png?raw=true' width="100" /> </center></td>
      <td><center><img src = 'assets/camera_distance_10_elevation_0_135_adv.png?raw=true' width="100"/> </center></td>
    <td><center> <img src = 'assets/camera_distance_10_elevation_20_177_adv.png?raw=true' width="100" /> </center></td>
      <td><center>  <img src = 'assets/camera_distance_15_elevation_20_330_adv.png?raw=true' width="100" /> </center></td>
    <td><center><img src = 'assets/camera_distance_15_elevation_50_327_adv.png?raw=true' width="100"/></center></td>
  </tr>
</table>

### Partial occlusion 

<table>
  <tr>
  <td>Original</td>
  <td><center> <img src = 'assets/camera_distance_1.5_elevation_0_6_ori.png?raw=true'  width="100"/></center></td>
    <td><center><img src = 'assets/camera_distance_1.5_elevation_0_42_ori.png?raw=true' width="100" /> </center></td>
      <td><center><img src = 'assets/camera_distance_1.5_elevation_0_54_ori.png?raw=true' width="100" /> </center></td>
    <td><center> <img src = 'assets/camera_distance_1.5_elevation_0_126_ori.png?raw=true' width="100" /> </center></td>
      <td><center>  <img src = 'assets/camera_distance_1.5_elevation_10_330_ori.png?raw=true' width="100" /> </center></td>
    <td><center><img src = 'assets/camera_distance_1.5_elevation_20_78_ori.png?raw=true' width="100" /></center></td>
  </tr>
  <tr>
    <td>FCA</td>
    <td><center> <img src = 'assets/camera_distance_1.5_elevation_0_6_adv.png?raw=true' width="100" /></center></td>
    <td><center><img src = 'assets/camera_distance_1.5_elevation_0_42_adv.png?raw=true' width="100" /> </center></td>
      <td><center><img src = 'assets/camera_distance_1.5_elevation_0_54_adv.png?raw=true' width="100" /> </center></td>
    <td><center> <img src = 'assets/camera_distance_1.5_elevation_0_126_adv.png?raw=true' width="100" /> </center></td>
      <td><center>  <img src = 'assets/camera_distance_1.5_elevation_10_330_adv.png?raw=true' width="100" /> </center></td>
    <td><center><img src = 'assets/camera_distance_1.5_elevation_20_78_adv.png?raw=true' width="100" /></center></td>
  </tr>
</table>


## Cases of Phyical Attack

### Case in the simulator environment

<iframe src="//player.bilibili.com/player.html?aid=937368019&bvid=BV1dT4y1U75b&cid=550826852&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>

### Case in the real world

<iframe src="//player.bilibili.com/player.html?aid=852356546&bvid=BV1RL4y1T723&cid=550828041&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>
