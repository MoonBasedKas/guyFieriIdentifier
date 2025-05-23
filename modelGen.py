#!/usr/bin/env python3
"""
Trains Maiq the Identifier to Identify faces like no other.
"""
import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import torch.optim as optim
import sys
import maiqNet
import faceData
import os 


"""
Color information to improve readability.
"""
class color:
    RED = '\033[31m'
    BLACK = "\033[0;30m"
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BROWN = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    LIGHT_GRAY = '\033[0;37m'
    DARK_GRAY = '\033[1;30m'
    LIGHT_RED = '\033[1;31m'
    LIGHT_GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    LIGHT_BLUE = '\033[1;34m'
    LIGHT_PURPLE = '\033[1;35m'
    LIGHT_CYAN = '\033[1;36m'
    LIGHT_WHITE = '\033[1;37m'
    RESET = '\033[0m'


"""
Performs the training of one epoch for the AI.
"""
def train_epoch():
    # Begin learning
    maiqNet.train(True)
    runningLoss = 0.0
    runningAccuracy = 0.0
    batches = 0
    col = color.RED

    # Iterate over the trained data
    print("-")
    for batch, data  in enumerate(trainloader):
        inputs, labels = data[0].to(device), data[1].to(device)

        # Reset the gradents
        optimizer.zero_grad()
        outputs = maiqNet(inputs) # Gets our shape, size, shape(2)
        # The highest value of this will be the most likely, it'll be the index of it.
        # Gets us the labels of the images where it matches
        correct = torch.sum(labels == torch.argmax(outputs, dim=1)).item()
        runningAccuracy += correct / batch_size

        # This is kind of magic but for back propagation
        loss = criterion(outputs, labels)
        runningLoss += loss.item()
        loss.backward()
        optimizer.step()
        batches += 1
        if batch % 100 == 3:
            avgLossAcrossBatches = runningLoss/batches
            avgAcrossBatches = (runningAccuracy/batches)*100
            print("Batch", batch)
            print("Loss:", avgLossAcrossBatches)
            if avgAcrossBatches < 20:
                col = color.RED
            elif avgAcrossBatches < 40:
                col = color.YELLOW
            elif avgAcrossBatches < 60:
                col = color.LIGHT_PURPLE
            elif avgAcrossBatches < 80:
                col = color.BLUE
            elif avgAcrossBatches < 100:
                col = color.GREEN
            else:
                col = color.LIGHT_RED
            
            print(col + "Accuracy:",avgAcrossBatches, color.RESET)
            runningAccuracy = 0
            runningLoss = 0
            batches = 0

    print("-")


"""
Tests the accuracy of the AI.
"""
def validate_epoch():
    # Disable training
    maiqNet.train(False)
    runningLoss = 0.0
    runningAccuracy = 0.0
    col = None
    print(color.LIGHT_BLUE + "Eval:" + color.RESET)
    # Iterate over the test data
    for batch, data  in enumerate(testloader):
        inputs, labels = data[0].to(device), data[1].to(device)

        with torch.no_grad():
            outputs = maiqNet(inputs)
            correct = torch.sum(labels == torch.argmax(outputs, dim=1)).item()

        # The highest value of this will be the most likely, it'll be the index of it.
        # Gets us the labels of the images where it matches
            correct = torch.sum(labels == torch.argmax(outputs, dim=1)).item()
            runningAccuracy += correct / batch_size

        # This is kind of magic but for back propagation
            loss = criterion(outputs, labels)
            runningLoss += loss.item()


    # I'm not sure if this is meant to be indented left or right.
    # Because the model seems to max out at 20 when indendented.
    avgLossAcrossBatches = runningLoss/len(testloader)
    avgAcrossBatches = (runningAccuracy/len(testloader))*100
    
    print("Batch", batch)
    print("Loss:", avgLossAcrossBatches)
    if avgAcrossBatches < 20:
        col = color.RED
    elif avgAcrossBatches < 40:
        col = color.YELLOW
    elif avgAcrossBatches < 60:
        col = color.PURPLE
    elif avgAcrossBatches < 80:
        col = color.LIGHT_PURPLE
    else:
        col = color.GREEN
    print(col + "Accuracy:",avgAcrossBatches, color.RESET)
    runningAccuracy = 0
    runningLoss = 0



# Very slow
device = 'cpu'

def main():
    

    pass

# The magic model
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((128,128)),
    transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))],
     )

# transform = transforms.ToTensor()

batch_size = 8

# This gets the data set?
labelPath = "." + os.sep + "labels.csv"
imagePath = "." + os.sep + "data"
trainset = faceData.CustomImageDataset(labelPath, imagePath, transform=transform)
lim = len(trainset) * .15
lim = round(lim)
tlen = len(trainset) - lim
trainset, testset = torch.utils.data.random_split(trainset, [tlen, lim])
# This loads it into torch to train?
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True)
# num_workers=2


# Tests the accuracy
# testset = torchvision.datasets.CIFAR10(root='./data', train=False,
#                                        download=True, transform=transform)

# testset = faceData.CustomImageDataset(f".{os.sep}data{os.sep}train.csv", f".{os.sep}data{os.sep}training", transform=transform)

testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False)



# classes = ('Unknown', 'Maiq')


# Colored images have 3 channels
def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()


# get some random training images
dataiter = iter(trainloader)
images, labels = next(dataiter)
# Gets me my shape fo
# print(images.shape) # NOTE: Use when need to find new size.



maiqNet = maiqNet.neuralNet()


criterion = nn.CrossEntropyLoss()
# Erik said this adam guy is like magic, lr: learning rate
optimizer = optim.Adam(maiqNet.parameters(), lr=0.001)
# NOTE: parameter stuff.
# for i, data in enumerate(trainloader, 0):
#         # get the inputs; data is a list of [inputs, labels]
#         inputs, labels = data
#         print(inputs.shape)
#         print(net(inputs).shape)
# Our params
z = 0
for x in maiqNet.parameters():
     z += len(torch.flatten(x))
print("Params", z)

# Epic training loop
epic = 10
for epoch in range(epic):
    print("-----")
    print(color.BLUE + "epoch:", epoch + 1, color.RESET)

    train_epoch()
    validate_epoch()
    print("-----")



PATH = './maiqTheIdentifier.pth'
torch.save(maiqNet.state_dict(), PATH)
