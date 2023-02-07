
from .models import IpAddress  


import socket
import asyncio

class SaveIpAddressMiddleware: 

    
	def __init__(self, get_response):

		self.get_response = get_response
		# One-time configuration and initialization.

	def __call__(self, request):
		# Code to be executed for each request before
		# the view (and later middleware) are called.

		

		# ips = IpAddress.objects.all()

		ip_with_socket = socket.gethostbyname(socket.gethostname())
		ip_with_request = request.META.get('REMOTE_ADDR')

		# socket_ip_exist =  ips.filter(ip_address=ip_with_socket).exists() 
		# request_ip_exist = ips.filter(ip_address=ip_with_request).exists() 


		# if not socket_ip_exist and request.user.is_anonymous:
		# 	ip_address = IpAddress(ip_address=ip_with_socket, pub_date=datetime.datetime.now())
		# 	ip_address.save()
		if request.user.is_anonymous:
			asyncio.run(IpAddress.objects.aget_or_create(ip_address=ip_with_socket))
			asyncio.run(IpAddress.objects.aget_or_create(ip_address=ip_with_request))


		# if not request_ip_exist and request.user.is_anonymous:
		# 	ip_address = IpAddress(ip_address=ip_with_request, pub_date=datetime.datetime.now())
		# 	ip_address.save()




		response = self.get_response(request)

		# Code to be executed for each request/response after
		# the view is called.


		return response



