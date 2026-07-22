from torchvision.models import resnet18
import torch.nn as nn
 
 
def build_model(num_classes=2):
    model = resnet18(weights=None)  # weights from our trained best_model.pth
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model
 