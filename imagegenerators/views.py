from django.shortcuts import render
from django.conf import settings
import openai
# Create your views here.
def generate_image(request):

    q = request.GET.get('q')
    response = openai.Image.create(
        prompt = str(q),
        n=6,
        size="1024x1024",
        user=str(request.user)
    )
    image_url = response['data']
    created = response['created']
    print("response", response)
    context = {
        "title": "image generator",
        "response": image_url,
        "created": created
    }
    return render(request, 'image_generator.html', context)