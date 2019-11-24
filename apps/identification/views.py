from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from keras.applications.resnet50 import ResNet50
from PIL import Image
import numpy as np
import io
import json
import ssl


def prepare_image(image, target):
    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image


@login_required(login_url='/accounts/login/')
def predict(request):
    return render(request, 'predict.html')


@csrf_exempt
def predict_request(request):

    data = {"success": False}

    # solve error “SSL: CERTIFICATE_VERIFY_FAILED”
    ssl._create_default_https_context = ssl._create_unverified_context

    top = request.POST.get("top")

    # ensure an image was properly uploaded to our endpoint
    if request.method == 'POST':

        if request.FILES.get("image"):
            # read the image in PIL format
            if top:
                top = int(top)
            else:
                top = 6

            image = request.FILES["image"].read()
            image = Image.open(io.BytesIO(image))
            model = ResNet50(weights='imagenet')

            img = prepare_image(image, target=(224, 224))
            preds = model.predict(img)
            results = imagenet_utils.decode_predictions(preds, top=top)
            data["predictions"] = []

            # loop over the results and add them to the list of
            # returned predictions
            for (imagenetID, label, prob) in results[0]:
                r = {"label": label, "probability": float(prob)}
                data["predictions"].append(r)

            # indicate that the request was a success
            data["success"] = True

    return HttpResponse(json.dumps(data), content_type='application/json')


