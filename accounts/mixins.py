
from django.http        import Http404


class AccessLimitMixin():

	def setup(self, request, *args, **kwargs):

		if request.user.is_authenticated:
			raise Http404('شما قبلا لاگین شده اید دوست من')
		else:
			return super().setup(request, *args, **kwargs)
