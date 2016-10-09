import re

pattern = r"rasp[^,?]*|stra[^,?]*"
regex = re.compile(pattern)
test_str = "raspberry,apple,strawberry"
for match in regex.match(test_str):
    print match.group()
	

# for matchNum, match in enumerate(matches):
#     print 