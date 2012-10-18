from django.shortcuts import render_to_response

def welcome(request):
    c = {
        'names': [
            'creisman',
            'jlowdermilk',
            'natmote',
            'cmoice',
        ]
    }

    return render_to_response('welcome.html', c)
