# Create your views here.
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.forms import ModelForm
from django.template import RequestContext

def show_stages(request):
	return render_to_response(
		"stages/stage.html",
		{})