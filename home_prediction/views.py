from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import numpy as np
import tensorflow as tf
from keras.preprocessing import image
import json
from products.models import Product
from info.models import Plant_Info
from django.contrib.auth.decorators import login_required
from users.views import is_admin
from .models import Prediction
from django.conf import settings


img_height, img_width = 256, 256

with open('./models/class_names.json', 'r') as f:
    labelInfo = f.read()

labelInfo = json.loads(labelInfo)

model = tf.keras.models.load_model('./models/plant_care_model.h5')


def index(request):
    if is_admin(request.user):
        return render(request, 'users/admin_dashboard.html')
    else:
        return render(request, 'index.html')


def predictImage(request):
    processing = False
    if request.method == 'POST':

        if request.user.is_authenticated:
            
            try:
                processing = True
                fileObj = request.FILES['filePath']
                fs = FileSystemStorage()
                filePathNames = fs.save(fileObj.name, fileObj)
                filePathName = './media/' + filePathNames

                testimage = filePathName

                img = image.load_img(testimage, target_size=(img_height, img_width))
                x = image.img_to_array(img)

                x = x / 255
                x = x.reshape(1, img_height, img_width, 3)
                predictions = model.predict(x)

                predictedLabel = labelInfo[str(np.argmax(predictions[0]))]
                label = ' '.join(predictedLabel)

                description, cause, solution = results(predictedLabel)
                confidence = round(100 * (np.max(predictions[0])), 2)

                recommended_products = recommend_products(predictedLabel)

                recommended_product_names = [product.product_name for product in recommended_products]

                Prediction.objects.create(user=request.user, image_path=filePathNames, predicted_label=label, confidence=confidence, recommended_products=recommended_product_names)            

                context = {
                    'filePathName': filePathName, 
                    'label': label,
                    'description': description,
                    'cause': cause, 
                    'solution': solution,
                    'confidence':confidence, 
                    "recommended_products":recommended_products,
                    'processing': processing
                    }

                return render(request, 'index.html', context)
            except Exception as e:
                return redirect('homepage')

        else:
            return redirect('login')
    else:
        return redirect('homepage')


def recommend_products(predicted_label):
    if isinstance(predicted_label, list):
        predicted_label = ' '.join(predicted_label)
    
    products = predicted_label
    products = Product.objects.filter(product_for__icontains=products)
    
    return products


def results(predictedLabel):
    try:
        plant = Plant_Info.objects.filter(plant_name=predictedLabel[0]).first()
        if plant:
            description = plant.plant_description
            cause = plant.cause
            solution = plant.solution
            return description, cause, solution
        else:
            return 'No information available for this plant'
    except Plant_Info.DoesNotExist:
        return 'Sorry'

@login_required
def prediction_history(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-timestamp')
    for prediction in predictions:
        prediction.image_path = request.build_absolute_uri(settings.MEDIA_URL + prediction.image_path)
    return render(request, 'prediction/prediction_history.html', {'predictions': predictions})