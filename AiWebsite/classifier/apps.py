import os
import torch
from django.apps import AppConfig
from django.conf import settings
 
 
class ClassifierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'classifier'
 
    model = None
    device = None
    caption_processor = None
    caption_model = None
 
    def ready(self):
        from .dl_model.architecture import build_model
        from transformers import BlipProcessor, BlipForConditionalGeneration
 
        ClassifierConfig.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
 
        # AI-vs-Real classification model (ResNet18-based)
        model = build_model(num_classes=2)
        model_path = os.path.join(settings.BASE_DIR, 'classifier', 'dl_model', 'best_model.pth')
        model.load_state_dict(torch.load(model_path, map_location=ClassifierConfig.device))
        model.to(ClassifierConfig.device)
        model.eval()
        ClassifierConfig.model = model
 
        # BLIP captioning model
        ClassifierConfig.caption_processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        caption_model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        caption_model.to(ClassifierConfig.device)
        caption_model.eval()
        ClassifierConfig.caption_model = caption_model
 