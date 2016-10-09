from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer
from django.http import HttpResponse
import re
from django.db.models import Q

class MovieList(APIView):

	# def get(self,request):
	# 	t = 'name'
	# 	p = 'sultan'
	# 	# print Movie.objects.get(name=p)
	# 	# print dict(request.query_params)
	# 	# query_params_list = []
	# 	# # dct = dict(request.query_params)
	# 	# for key,value in request.query_params.items():
	# 	# 	q = key + '=' + '"'+''.join(value)+'"'
	# 	# 	# print key, value
	# 	# 	query_params_list.append(q)
	# 	# que = ','.join(query_params_list)
	# 	# # t = "director='Ali Abbas Zafar',name='sultan'"
	# 	# print que
	# 	movies = Movie.objects.all()
	# 	serializer = MovieSerializer(movies,many=True)
	# 	return Response(serializer.data)

		# serializer = MovieSerializer(request,many=True)
		# return HttpResponse(request)

	def post(self):
		pass

	def get(self,request):
		queryset = Movie.objects.all()

		keys = request.query_params.keys()

		keys = ','.join(keys)
		pattern = r'popularity99[^,?]*|imdb_score[^,?]*'
		regex = re.compile(pattern)
		q = re.findall(regex,keys)
		name = self.request.query_params.get('name')
		director = self.request.query_params.get('director')
		imdb = self.request.query_params.get('imdb_score')
		popularity = self.request.query_params.get('popularity99')
		genre = self.request.query_params.get('genre')

		if name is not None:
			# queryset = queryset.filter(name=name,director=director)
			queryset = queryset.filter(name__contains=name.strip())
		if director is not None:
			queryset = queryset.filter(director__contains=director.strip())
		if popularity is not None:
			queryset = queryset.filter(popularity99=popularity.strip())
		if imdb is not None:
			queryset = queryset.filter(imdb_score=imdb.strip())
		# if genre is not None:
		# 	for gen in genre:
		# 		queryset = queryset.filter(genre__contains=gen)

		print genre,imdb,request.query_params
		if genre is not None:
			try:
				genre = genre.split(',')
			except:
				genre = list(genre)
			genre_len = len(genre)
			
			for i in xrange(genre_len):
				genre[i] = genre[i].strip()

			if genre_len == 1:
				queryset = queryset.filter(genre__contains=genre[0])
				queryset = queryset.filter(Q(genre__contains=genre[0])|Q(genre__contains=genre[1]))
			elif genre_len == 3:
				queryset = queryset.filter(Q(genre__contains=genre[0])|Q(genre__contains=genre[1])|Q(genre__contains=genre[2]))
			elif genre_len == 4:
				queryset = queryset.filter(Q(genre__contains=genre[0])|Q(genre__contains=genre[1])|Q(genre__contains=genre[2])|Q(genre__contains=genre[3]))
			else:
				queryset = queryset.filter(Q(genre__contains=genre[0])|Q(genre__contains=genre[1])|Q(genre__contains=genre[2])|Q(genre__contains=genre[3])|Q(genre__contains=genre[4]))
		
		# print type(queryset)

		comparator = {}
		if imdb is None and popularity is None:
			for entry in q:
				try:
					k = entry.split('<')
					comparator[k[0].strip()] = [k[1].strip(),'less'.strip()]
				except:
					try:
						k = entry.split('>')
						comparator[k[0].strip()] = [k[1].strip(),'greater'.strip()]
					except:
						pass
		# print comparator
		# print comparator.get('popularity')
		if 'popularity99' in comparator.keys():
			val = comparator.get('popularity99')
			if val[1] == 'greater':
				exp = ( float(val[0])+0.1,100)
			else:
				exp = (0,float(val[0])-0.1)
			try:
				queryset = queryset.filter(popularity99__range=exp)
			except:
				pass

		if 'imdb_score' in comparator.keys():
			val = comparator.get('imdb_score')
			if val[1] == 'greater':
				exp = (float(val[0])+0.01,10)
			else:
				exp = (0,float(val[0])-0.01)
			try:
				queryset = queryset.filter(imdb_score__range=exp)
			except:
				pass

		# queryset = queryset.filter(Q(genre__contains="Crime")|Q(genre__contains="Drama"))
		# queryset = queryset.filter(genre__contains="Drama")

		serializer = MovieSerializer(queryset,many=True)
		return Response(serializer.data)
