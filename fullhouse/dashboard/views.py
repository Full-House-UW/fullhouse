from django.shortcuts import render_to_response

def welcome(request):
    c = {
        'names': [
            'creisman',
            'jlowdermilk',
        ]
    }

    return render_to_response('welcome.html', c)
