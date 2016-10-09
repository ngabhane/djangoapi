This is an attempt to create a RESTful api to search for movies by using following search parameters:

1. name
2. director
3. genre
4. popularity99
5. imdb_score

This api is case insensitive.
eg., query "?name=King Kong" is euivalent to "?name=king kong". Same is valid for other search parameters

It works well with multiple search parameters
eg., "?name=King kong&director=Merian C. Cooper"

There are 3 options for popularity99 and imdb_score
1. "="  => Exactly equal : "?imdb_score=8.5"
2. ">"	=> Greter than(exclude given number) : "?popularity99>85"
3. "<" 	=> Less than(exclude given number) : "?popularity99<85"

You can enter comma seperated values for "genre"
eg., "?genre=Drama"
	 "?genre=Drama,Crime"
