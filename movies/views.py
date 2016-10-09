from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer
import re
from django.db.models import Q

class MovieList(APIView):

	def post(self):
		pass

	def pop_imdb_list(self,keys):
		keys = ','.join(keys)
		pattern = r'popularity99[^,?]*|imdb_score[^,?]*'
		regex = re.compile(pattern)
		return re.findall(regex,keys)		

	def get(self,request):

		queryset = Movie.objects.all()
		keys = request.query_params.keys()

		q = self.pop_imdb_list(keys)

		name 		= self.request.query_params.get('name')
		director 	= self.request.query_params.get('director')
		imdb 		= self.request.query_params.get('imdb_score')
		popularity 	= self.request.query_params.get('popularity99')
		genre 		= self.request.query_params.get('genre')

		if name is not None:
			queryset = queryset.filter(name__contains=name.strip())
		if director is not None:
			queryset = queryset.filter(director__contains=director.strip())
		if popularity is not None:
			queryset = queryset.filter(popularity99=popularity.strip())
		if imdb is not None:
			queryset = queryset.filter(imdb_score=imdb.strip())

		# print genre,imdb,request.query_params
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
			elif genre_len == 2:
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

		serializer = MovieSerializer(queryset,many=True)
		return Response(serializer.data)
