import os
import shutil

main_path = "E:/my_data_from_carla/my_carla_dataset_with_global_position/cam_right_1719970583/"
# names_path中有全部的训练图片
# mask_path存放每张训练图片的mask图片
# label_path中存放每张训练图片的label文件
names_path = main_path + "train_new"
mask_path = main_path + 'masks'
label_path = main_path + 'train_label_new'


# 复制mask.png，并将其名称设置为names_path中的图片的名称，直到每个names_path中的图片，都有一个同名的mask图片
def copy_mask():
    origin = main_path + "mask.png"
    names = os.listdir(names_path)
    if not os.path.exists(mask_path):
        os.mkdir(mask_path)
    print(names)
    for name in names:
        dest = mask_path + "/" + name
        shutil.copy(origin, dest)


def copy_label():
    origin = main_path + "label.txt"
    names = os.listdir(names_path)
    print(names)
    if not os.path.exists(label_path):
        os.mkdir(label_path)
    for name in names:
        dest = label_path + "/" + name.split('.')[0] + ".txt"
        shutil.copy(origin, dest)


if __name__ == "__main__":
    copy_mask()
    copy_label()
