from django.views.generic import TemplateView
from SqlLabApp.models import User
class HelpView(TemplateView):
    template_name = 'SqlLabApp/helpguide.html'

    def get(self, request, *args, **kwargs):
        full_name = User.objects.get(email=request.user.email).full_name
        return self.render_to_response(
            self.get_context_data(
                full_name=full_name,
            )
        )