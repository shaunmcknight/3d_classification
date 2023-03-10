import os
import numpy as np

import torchvision.transforms as transforms
from torch.autograd import Variable

import torch.nn as nn
import torch.nn.functional as F
import torch

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import glob
import random
from torch.utils.data import Dataset
from PIL import Image


########################################################
# Methods for 3D DataLoader
#
# 1's = defect
# 0's = no defect
#
#
########################################################

class SyntheticDataset(Dataset):
    def __init__(self, root, transforms_=None, mode="train"):
        self.transform = transforms.Compose(transforms_)
        
        self.files_defect = np.load(glob.glob(os.path.join(root, "%s_defect" % mode) + "/*.*")[0])
        self.labels_defect = np.ones(np.shape(self.files_defect)[0])
        
        self.files_no_defect = np.load(glob.glob(os.path.join(root, "%s_no_defect" % mode) + "/*.*")[0])
        self.labels_no_defect = np.zeros(np.shape(self.files_no_defect)[0])
        
        self.combined_data = np.concatenate((self.files_defect, self.files_no_defect))
        self.labels = np.concatenate((self.labels_defect, self.labels_no_defect))
            
        print('~~~~ Synthetic dataloader INFO ~~~~~')
        print('Number defective points ', mode,' ~ ', len(self.files_defect), 
              'Max/Min ', np.amax(self.files_defect), np.amin(self.files_defect), 
              ' ~ Shape ', np.shape(self.files_defect[0]))
        print('Number defect free points ', mode,' ~ ', len(self.files_no_defect), 
              'Max/Min ', np.amax(self.files_no_defect), np.amin(self.files_no_defect), 
              ' ~ Shape ', np.shape(self.files_no_defect[0]))

    def __getitem__(self, index):
        data = self.combined_data[index]
        data = torch.from_numpy(np.pad(
            data, ((0,0), (0, 1024-data.shape[1]), (0,0)),
            mode='constant', constant_values=0)) # pad depth to 1024
        data = np.clip(data, 0, 1)
        data = data.unsqueeze(0)
        #print('shape ', data.shape)
        label = self.labels[index]
        if self.transform != None:
            data = self.transform(data)
        # print('Image shape ', np.shape(image))
        return data, label

    def __len__(self):
        return len(self.combined_data)


class ExperimentalDataset(Dataset):
    def __init__(self, root, transforms_=None, mode="test"):
        self.transform = transforms.Compose(transforms_)
        
        self.files_defect = np.load(glob.glob(os.path.join(root, "%s_defect" % mode) + "/*.*")[0])
        self.labels_defect = np.ones(np.shape(self.files_defect)[0])
        
        self.files_no_defect = np.load(glob.glob(os.path.join(root, "%s_no_defect" % mode) + "/*.*")[0])
        self.labels_no_defect = np.zeros(np.shape(self.files_no_defect)[0])
        
        self.combined_data = np.concatenate((self.files_defect, self.files_no_defect))
        self.labels = np.concatenate((self.labels_defect, self.labels_no_defect))
            
        print('~~~~ Synthetic dataloader INFO ~~~~~')
        print('Number defective points ', mode,' ~ ', len(self.files_defect),
              'Max/Min ', np.amax(self.files_defect), np.amin(self.files_defect), 
              ' ~ Shape ', np.shape(self.files_defect[0]))
        print('Number defect free points ', mode,' ~ ', len(self.files_no_defect),
              'Max/Min ', np.amax(self.files_no_defect), np.amin(self.files_no_defect), 
              ' ~ Shape ', np.shape(self.files_no_defect[0]))

    def __getitem__(self, index):
        data = self.combined_data[index]
        data = torch.from_numpy(np.pad(
            data, ((0,0), (0, 1024-data.shape[1]), (0,0)),
            mode='constant', constant_values=0)) # pad depth to 1024
        data = data.unsqueeze(0)
        label = self.labels[index]
        if self.transform != None:
            data = self.transform(data)
        # print('Image shape ', np.shape(image))
        return data, label

    def __len__(self):
        return len(self.combined_data)
