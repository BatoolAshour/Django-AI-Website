import torch
from torchvision import transforms
from PIL import Image as PILImage
from django.apps import apps
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from .forms import ImageForm
from .models import PredictionResult
 
CLASS_NAMES = ['AI-Generated', 'Real']  # index 0, 1 — matches training
 
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                          std=[0.229, 0.224, 0.225])
])
 
 
# def classify_image(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded = UploadedImage.objects.create(image=request.FILES['image'])
#             img = PILImage.open(uploaded.image.path).convert('RGB')
#             img_tensor = transform(img).unsqueeze(0)
#             config = apps.get_app_config('classifier')
#             model, device = config.model, config.device
#             img_tensor = img_tensor.to(device)
#             with torch.no_grad():
#                 outputs = model(img_tensor)
#                 probs = torch.softmax(outputs, dim=1)
#                 confidence, pred_idx = torch.max(probs, 1)
#             label = CLASS_NAMES[pred_idx.item()]
#             confidence_val = confidence.item()
#             PredictionResult.objects.create(image=uploaded, label=label, confidence=confidence_val)
#             return redirect('history')
#     else:
#         form = ImageForm()
#     return render(request, 'classifier/classify.html', {'form': form})
#
# def prediction_history(request):
#     results = PredictionResult.objects.select_related('image').order_by('-created_at')
#     return render(request, 'classifier/history.html', {'results': results})
 
 
class ClassifyImageView(FormView):
    template_name = "classifier/classify.html"
    form_class = ImageForm
    success_url = reverse_lazy("classifier:history")
 
    def form_valid(self, form):
        instance = form.save(commit=False)
 
        img = PILImage.open(self.request.FILES['image']).convert('RGB')
        img_tensor = transform(img).unsqueeze(0)
 
        config = apps.get_app_config('classifier')
        model, device = config.model, config.device
        img_tensor = img_tensor.to(device)
 
        with torch.no_grad():
            outputs = model(img_tensor)
            probs = torch.softmax(outputs, dim=1)
            confidence, pred_idx = torch.max(probs, 1)
 
        label = CLASS_NAMES[pred_idx.item()]
        confidence_val = confidence.item()
 
        instance.label = label
        instance.confidence = confidence_val
        instance.save()
 
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