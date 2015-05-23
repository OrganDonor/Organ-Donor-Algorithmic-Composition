register_list = []
#an ordered list of the octaves involved in the signature
for index, number in enumerate(signature): 
	#index is the index, number is the value 0 or 1 at each index
	if number != 0:
		register_list.append(number)
print register_list