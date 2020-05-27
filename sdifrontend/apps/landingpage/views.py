from django.views.generic import TemplateView
from django.shortcuts import render

class IndexView(TemplateView):
   template_name = 'index.html'
   uuid = None
   access_token = None
   refresh_token = None
   
   def get(self, request, *args, **kwargs):
      if request.user.is_authenticated:
         self.uuid = request.user.social_auth.get(provider='globus').uid
         social = request.user.social_auth
         self.access_token = social.get(provider='globus').extra_data['access_token']
         self.refresh_token = social.get(provider='globus').extra_data['refresh_token']

      return render(request, self.template_name, {'uuid': self.uuid,
                  'access_token': self.access_token,
                  'refresh_token': self.refresh_token})