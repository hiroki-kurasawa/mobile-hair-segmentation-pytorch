import torch
from model.model import MobileHairNet
import os
from glob import glob
import matplotlib.pyplot as plt
from torchvision.utils import save_image


class Tester:
    def __init__(self, config, dataloader):
        self.batch_size = config.batch_size
        self.config = config
        self.model_path = config.checkpoint_dir
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.data_loader = dataloader
        self.num_classes = config.num_classes
        self.build_model()
        self.num_test = config.num_test
        self.test_dir = config.sample_image_dir

    def build_model(self):
        self.net = MobileHairNet()
        self.net.to(self.device)
        self.load_model()

    def load_model(self):
        print("[*] Load checkpoint in ", str(self.model_path))
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)

        if not os.listdir(self.model_path):
            print("[!] No checkpoint in ", str(self.model_path))
            return

        model = glob(os.path.join(self.model_path, "MobileHairNet*.pth"))
        model.sort()

        self.net.load_state_dict(torch.load(model[-1], map_location=self.device))
        print("[*] Load Model from %s: " % str(self.model_path), str(model[-1]))

    def test(self):

        for step, (image, mask) in enumerate(self.data_loader):
            image = image.to(self.device)
            mask = mask.to(self.device)
            pred = self.net(image)

            result = torch.cat((image, mask, pred), 3)


            print('[*] Saved sample images')
        result_file = os.path.join(self.test_dir, "test.png")
        plt.savefig(dir_name)


