"""
Code to use the saved models for testing
"""

import numpy as np
import pdb
import os
from tqdm import tqdm

from matplotlib import pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader

import torchvision
from torchvision.datasets import FashionMNIST
from torchvision import transforms

from utils import AverageMeter
from sklearn.metrics import confusion_matrix

def test(model, testloader):
    """ Training the model using the given dataloader for 1 epoch.

    Input: Model, Dataset, optimizer,
    """

    model.eval()
    avg_loss = AverageMeter("average-loss")

    y_gt = []
    y_pred_label = []

    for batch_idx, (img, y_true) in enumerate(testloader):
        img = Variable(img)
        y_true = Variable(y_true)
        out = model(img)
        y_pred = F.softmax(out, dim=1)
        y_pred_label_tmp = torch.argmax(y_pred, dim=1)

        loss = F.cross_entropy(out, y_true)
        avg_loss.update(loss, img.shape[0])

        # Add the labels
        y_gt += list(y_true.numpy())
        y_pred_label += list(y_pred_label_tmp.numpy())

    return avg_loss.avg, y_gt, y_pred_label


if __name__ == "__main__":

    trans_img = transforms.Compose([transforms.ToTensor()])
    dataset = FashionMNIST("./data/", train=False, transform=trans_img, download=True)
    testloader = DataLoader(dataset, batch_size=1024, shuffle=False)

    from train_multi_layer import MLP
    model_MLP = MLP()
    model_MLP = torch.load("./models/MLP.pth")

    from cnn_train import Network
    model_conv_net = Network()
    model_conv_net = torch.load("./models/convNet.pth")

    loss, gt, pred = test(model_MLP, testloader)
    
    # mlp_confusion_matrix = confusion_matrix(np.array(gt),np.array(pred))
    # np.savetxt("mlp_confusion_matrix.csv", mlp_confusion_matrix, delimiter=",")

    with open("multi-layer-net.txt", 'w') as f:
        f.write("Loss on Test Data : {}\n".format(loss))
        f.write("Accuracy on Test Data : {}\n".format(np.mean(np.array(gt) == np.array(pred))))
        f.write("gt_label,pred_label \n")
        for idx in range(len(gt)):
            f.write("{},{}\n".format(gt[idx], pred[idx]))

    loss, gt, pred = test(model_conv_net, testloader)

    # cnn_confusion_matrix = confusion_matrix(np.array(gt),np.array(pred))
    # np.savetxt("cnn_confusion_matrix.csv", cnn_confusion_matrix, delimiter=",")    

    with open("convolution-neural-net.txt", 'w') as f:
        f.write("Loss on Test Data : {}\n".format(loss))
        f.write("Accuracy on Test Data : {}\n".format(np.mean(np.array(gt) == np.array(pred))))
        f.write("gt_label,pred_label \n")
        for idx in range(len(gt)):
            f.write("{},{}\n".format(gt[idx], pred[idx]))

    
