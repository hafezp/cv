
from django.http 					import JsonResponse, HttpResponse
from django.core 					import serializers
from django.shortcuts               import get_object_or_404, render
from django.views.generic           import DetailView, View

from .models                        import Testimonial, Post
from .forms							import ContactForm



# Create your views here.



class PostDetailView(DetailView):
    model = Post
    template_name = "single.html"  
    def get_object(self):
        id=self.kwargs.get('id')
        return get_object_or_404(Post.objects.all(), id=id)


def is_ajax(request):
	return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class ContactFormView(View):

	form_class = ContactForm


	def get(self, request, *args, **kwargs):
		form = self.form_class
		context = {
		'testimonials':Testimonial.objects.all(),
		'posts':Post.objects.all(),
		'form':form
		}
		
		return render(request, 'index.html', context)


	def post(self, request, *args, **kwargs):
		if is_ajax(request=request):
			form = self.form_class(self.request.POST)
			if form.is_valid():
				instance = form.save()
				ser_instance = serializers.serialize('json', [ instance, ])
				# send to client side.
				return JsonResponse({"instance": ser_instance}, status=200)
			else:
				return JsonResponse({"error": form.errors}, status=400)

		return JsonResponse({"error": ""}, status=400)



def custom_page_not_found_view(request, exception):
   

    return render(request, 'cv/404.html')


def custom_permission_denied_view(request, exception):
   

    return render(request, 'cv/403.html')


def custom_bad_request_view(request, exception):
   

    return render(request, 'cv/400.html')


class My500View(View):
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse('err 500')