# https://carla.readthedocs.io/en/0.9.14/tuto_G_retrieve_data/#rgb-camera
import carla
import time
import pygame
import numpy as np
import random
from PIL import Image


class VehicleAndCamera:
    def __init__(self, cam_position):
        self.cam_position = cam_position
        self.client = carla.Client('localhost', 2000)
        # print(client.get_available_maps())
        # world = client.load_world("Town01")
        self.world = self.client.get_world()
        self.world.set_weather(carla.WeatherParameters.ClearNoon)
        self.bp_lib = self.world.get_blueprint_library()
        self.ego_vehicle, ego_transform = self.spawn_vehicle()
        self.set_spectator(ego_transform)
        self.ego_cam = self.spawn_rgb_camera()

    def spawn_vehicle(self):
        ego_bp = self.world.get_blueprint_library().find('vehicle.tesla.model3')
        ego_bp.set_attribute('role_name', 'ego')
        ego_color = random.choice(ego_bp.get_attribute('color').recommended_values)
        ego_bp.set_attribute('color', ego_color)

        spawn_points = self.world.get_map().get_spawn_points()
        number_of_spawn_points = len(spawn_points)
        if 0 > number_of_spawn_points:
            print('\nCould not found any spawn points')
            raise SystemExit

        random.shuffle(spawn_points)
        ego_transform = spawn_points[0]
        print('\nEgo is spawned')
        return self.world.spawn_actor(ego_bp, ego_transform), ego_transform

    def set_spectator(self, ego_transform):
        spectator = self.world.get_spectator()
        world_snapshot = self.world.wait_for_tick()
        sp_transform = carla.Transform(ego_transform.location + carla.Location(z=30, x=-25),
                                       carla.Rotation(yaw=90, pitch=-90))
        # spectator.set_transform(ego_vehicle.get_transform())
        spectator.set_transform(sp_transform)

        control = carla.VehicleControl()
        control.throttle = 0.3
        self.ego_vehicle.apply_control(control)

    def spawn_rgb_camera(self):
        cam_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')
        cam_bp.set_attribute("image_size_x", str(1920))
        cam_bp.set_attribute("image_size_y", str(1080))
        # cam_bp.set_attribute("fov", str(90))
        cam_transform = carla.Transform(*self.cam_position)
        ego_cam = self.world.spawn_actor(cam_bp, cam_transform, attach_to=self.ego_vehicle,
                                         attachment_type=carla.AttachmentType.Rigid)
        # ego_cam.listen(lambda image: image.save_to_disk('output/%.6d.jpg' % image.frame, carla.ColorConverter.Raw))
        ego_cam.listen(lambda image: self.save_image_and_npz_new(image))
        return ego_cam

    def save_image_and_npz_new(self, image):
        pathstr = 'output/%.6d.png' % image.frame
        image.save_to_disk(pathstr, carla.ColorConverter.Raw)
        img = Image.open(pathstr)
        np_img = np.array(img)
        trans = self.ego_cam.get_transform()
        trans_cam = ((trans.location.x, trans.location.y, trans.location.z),
                     (trans.rotation.pitch, trans.rotation.yaw, trans.rotation.roll))
        print(trans_cam)
        trans = self.ego_vehicle.get_transform()
        trans_veh = ((trans.location.x, trans.location.y, trans.location.z),
                     (trans.rotation.pitch, trans.rotation.yaw, trans.rotation.roll))
        print(trans_veh)
        print("\n")
        pathstr = pathstr.split('.')[0] + ".npz"
        np.savez(pathstr, img=np_img, cam_trans=trans_cam, veh_trans=trans_veh)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ego_cam.destroy()
        self.ego_vehicle.destroy()


# 红绿灯摄像头，拍摄车尾，俯视角约为45度
cam_rear_06 = (carla.Location(-6, 0, 6), carla.Rotation(-45, 0, 0))
cam_rear_08 = (carla.Location(-8, 0, 6), carla.Rotation(-45, 0, 0))
cam_rear_10 = (carla.Location(-10, 0, 6), carla.Rotation(-45, 0, 0))
cam_rear_12 = (carla.Location(-12, 0, 6), carla.Rotation(-45, 0, 0))
cam_rear_14 = (carla.Location(-14, 0, 6), carla.Rotation(-45, 0, 0))
cam_rear_16 = (carla.Location(-16, 0, 6), carla.Rotation(-45, 0, 0))
cam_rear_18 = (carla.Location(-18, 0, 6), carla.Rotation(-45, 0, 0))
# 超速摄像头，拍摄车头，俯视角约为30度
cam_head_20 = (carla.Location(20, 0, 6), carla.Rotation(-45, 180, 0))
cam_head_18 = (carla.Location(18, 0, 6), carla.Rotation(-45, 180, 0))
cam_head_16 = (carla.Location(16, 0, 6), carla.Rotation(-45, 180, 0))
cam_head_14 = (carla.Location(14, 0, 6), carla.Rotation(-45, 180, 0))
cam_head_12 = (carla.Location(12, 0, 6), carla.Rotation(-45, 180, 0))
cam_head_10 = (carla.Location(10, 0, 6), carla.Rotation(-45, 180, 0))
cam_head_08 = (carla.Location(8, 0, 6), carla.Rotation(-45, 180, 0))
cam_head_06 = (carla.Location(6, 0, 6), carla.Rotation(-45, 180, 0))

cam_90 = (carla.Location(0, 0, 6), carla.Rotation(-90, 180, 0))  # 正上方拍摄，俯视角约为90度
cam_right = (carla.Location(0, 3, 1), carla.Rotation(0, 270, 0))  # 正右方拍摄，右侧正视摄像头
cam_left = (carla.Location(0, -3, 1), carla.Rotation(0, 90, 0))  # 正左侧拍摄，左侧正视摄像头
cam_back = (carla.Location(-4, 0, 1.2), carla.Rotation(0, 0, 0))  # 正后方拍摄，后侧正视摄像头


if __name__ == "__main__":
    with VehicleAndCamera(cam_head_08) as vc:
        time.sleep(3)
