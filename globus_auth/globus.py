from django.shortcuts import render

def globus_view(request):
    uuid = None
    access_token = None
    refresh_token = None

    # Verify the user is authenticated
    if request.user.is_authenticated:
        uuid = request.user.social_auth.get(provider='globus').uid
        social = request.user.social_auth
        access_token = social.get(provider='globus').extra_data['access_token']
        refresh_token = social.get(provider='globus').extra_data['refresh_token']

    return render(request,
                  'globus/globus.html',
                  {'uuid': uuid,
                  'access_token': access_token,
                  'refresh_token': refresh_token})