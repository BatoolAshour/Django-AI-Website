import os
import torch
from django.apps import AppConfig
from django.conf import settings

class ClassifierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'classifier'
    model = None
    device = None

    def ready(self):
        from .dl_model.architecture import SimpleCNN

        ClassifierConfig.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = SimpleCNN(num_classes=2)

        model_path = os.path.join(settings.BASE_DIR, 'classifier', 'dl_model', 'best_model.pth')
        model.load_state_dict(torch.load(model_path, map_location=ClassifierConfig.device))
        model.to(ClassifierConfig.device)
        model.eval()

        ClassifierConfig.model = model