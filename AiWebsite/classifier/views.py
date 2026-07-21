import torch
from torchvision import transforms
from PIL import Image as PILImage
from django.apps import apps
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from .forms import ImageForm
from .models import PredictionResult, ResultStatus
 
CLASS_NAMES = ['AI-Generated', 'Real']  
 
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                          std=[0.229, 0.224, 0.225])
])
 
 
class ClassifyImageView(FormView):
    template_name = "classifier/classify.html"
    form_class = ImageForm
    success_url = reverse_lazy("classifier:history")
 
    def form_valid(self, form):
        instance = form.save()
        ResultStatus.objects.create(result=instance, status='pending')
 
        config = apps.get_app_config('classifier')
        device = config.device
 
        try:
            img = PILImage.open(self.request.FILES['image']).convert('RGB')
 
            # --- AI vs Real classification ---
            img_tensor = transform(img).unsqueeze(0).to(device)
            with torch.no_grad():
                outputs = config.model(img_tensor)
                probs = torch.softmax(outputs, dim=1)
                confidence, pred_idx = torch.max(probs, 1)
 
            label = CLASS_NAMES[pred_idx.item()]
            confidence_val = confidence.item()
 
            # --- Captioning (BLIP) ---
            caption_inputs = config.caption_processor(images=img, return_tensors="pt").to(device)
            generated_ids = config.caption_model.generate(
                pixel_values=caption_inputs.pixel_values,
                max_length=50,
                num_beams=5,
                repetition_penalty=1.5,
                no_repeat_ngram_size=3,
                early_stopping=True
            )
            caption = config.caption_processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
 
            instance.label = label
            instance.confidence = confidence_val
            instance.save()
 
            final_status = 'finished_ai' if label == 'AI-Generated' else 'finished_real'
            ResultStatus.objects.create(result=instance, status=final_status, caption=caption)
 
        except Exception:
            ResultStatus.objects.create(result=instance, status='failed')
 
        return super(ClassifyImageView, self).form_valid(form)
 
    def form_invalid(self, form):
        return super(ClassifyImageView, self).form_invalid(form)
 
 
class PredictionHistoryView(ListView):
    model = PredictionResult
    template_name = "classifier/history.html"
    context_object_name = "results"
    ordering = ['-created_at']
 
    def get_queryset(self):
        return PredictionResult.objects.order_by('-created_at')