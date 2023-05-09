# Views imports
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PredictionForm1

# Prediction Imports
import os
import pickle
import numpy as np
import tensorflow as tf
from PIL import Image
from datetime import datetime, timezone


# Predictions here

QP_MODEL_DIR = '../../Predictions/'
QP_SCALAR_DIR = '../../Predictions/Model1/complements/'
QP_IMG_DIR = 'media/prediction_model1/'

model = tf.keras.models.load_model(QP_MODEL_DIR + 'final_model.h5')
stat_scaler = pickle.load(open(QP_SCALAR_DIR + 'stats_scaler.pickle', 'rb'))
like_scaler = pickle.load(open(QP_SCALAR_DIR + 'likes_scaler.pickle', 'rb'))
view_scaler = pickle.load(open(QP_SCALAR_DIR + 'views_scaler.pickle', 'rb'))

def quick_predict_script(stats, img_url):
    img = Image.open(img_url)
    img = img.resize((150, 150))
    thumb = np.array(img, dtype=np.float32)/255
    img_to_predict = np.expand_dims(thumb, axis=0)
    img.close()

    input_stat = np.expand_dims(stats, axis=0)
    input_stat = stat_scaler.transform(input_stat)

    ans = model.predict([img_to_predict, input_stat])
    view = view_scaler.inverse_transform(ans[0])
    like = like_scaler.inverse_transform(ans[1])
    return [view, like]








# Actual Views here

QUICK_PREDICT_COST = 1
CATEGORY_CHOICES = {
    1 : 'Gaming',
    2 : 'Development',
    3 : 'Cars'
}

def tools(request):
    return render(request, 'tools.html', {})

def quick_predict(request):
    if request.user.is_authenticated == False:                          # No user
        messages.error(request, "You need to login first!")
        return redirect("/accounts/login/")

    if request.method == 'GET':                                         # Simple GET
        context_dict = {'txt': 'Prediction Model 1'}
        form = PredictionForm1()
        context_dict['form'] = form

        return render(request, 'quick_predict.html', context_dict)

    
    elif request.method == 'POST':
        form = PredictionForm1(request.POST, request.FILES)
        if form.is_valid():
            
            if request.user.tokenBalance - QUICK_PREDICT_COST < 0:      # Token check!
                messages.error(request, "You are out of tokens!")
                return render(request, 'quick_predict.html', {})
            request.user.tokenBalance -= QUICK_PREDICT_COST             # Step 1
            request.user.totalPredictions += 1
            request.user.save()                                         # Step 2 - This is how you change user attributes!

            f_instance = form.save(commit=False)                        # Step 1
            f_instance.user = request.user                              # Step 2
            f_instance.save()                                           # Step 3 - This is how you set the user in the model!

            input_data = []
            input_data.append(['Category:', CATEGORY_CHOICES[f_instance.category]])
            input_data.append(["Channel publish:", str(f_instance.channel_pub_time)[:10]])
            input_data.append(["Video release:", str(f_instance.video_pub_time)[:10]])
            input_data.append(["Subscribers:", f_instance.subscribers])
            input_data.append(["Total Videos:", f_instance.videos])
            input_data.append(["Total Views:", f_instance.views])

            # category, seconds_since_published, subscribers, total_videos, total_views, publishing_date
            time_rn = datetime.now(timezone.utc)
            time_since_channel_published = (time_rn-f_instance.channel_pub_time)
            time_since_video_published = (time_rn-f_instance.video_pub_time)

            stats = [f_instance.category, time_since_channel_published.total_seconds(), f_instance.subscribers, f_instance.videos, f_instance.views, time_since_video_published.total_seconds()]
            p = quick_predict_script(stats, f_instance.thumb.url[1:])       # Slicing to remove first character '/'

            output_data = []
            output_data.append(["Predicted Views:", round(p[0][0][0])])
            output_data.append(["Predicted Views:", round(p[1][0][0])])

            context_dict = {'thumb_url': f_instance.thumb.url,
                            'input_data': input_data,
                            'output_data' :output_data}

            return render(request, 'results.html', context_dict)
