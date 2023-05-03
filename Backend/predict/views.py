from django.shortcuts import render

# Create your views here.

from .forms import PredictionForm1

CATEGORY_CHOICES = {
    1 : 'Gaming',
    2 : 'Development',
    3 : 'Cars'
}

def predict1(request):
    if request.method == 'GET':
        context_dict = {'txt': 'Prediction Model 1'}
        form = PredictionForm1()
        context_dict['form'] = form

        return render(request, 'predict1.html', context_dict)

    
    elif request.method == 'POST':
        form = PredictionForm1(request.POST, request.FILES)
        if form.is_valid():
            request.user.tokenBalance -= 5              # Step 1
            request.user.save()                         # Step 2 - This is how you change user attributes!

            f_instance = form.save(commit=False)        # Step 1
            f_instance.user = request.user              # Step 2
            f_instance.save()                           # Step 3 - This is how you set the user in the model!

            input_data = []
            input_data.append(['Category:', CATEGORY_CHOICES[f_instance.category]])
            input_data.append(["Channel publish:", str(f_instance.channel_pub_time)[:10]])
            input_data.append(["Video release:", str(f_instance.video_pub_time)[:10]])
            input_data.append(["Subscribers:", f_instance.subscribers])
            input_data.append(["Total Videos:", f_instance.videos])
            input_data.append(["Total Views:", f_instance.views])

            output_data = []
            output_data.append(["Predicted Views:", 100])
            output_data.append(["Predicted Views:", 50])

            context_dict = {'thumb_url': f_instance.thumb.url,
                            'input_data': input_data,
                            'output_data' :output_data}

            return render(request, 'results.html', context_dict)