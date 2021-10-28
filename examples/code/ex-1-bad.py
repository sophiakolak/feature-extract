import numpy as np

a = [] #empty list
for i in range(0,6): 
    a.append(i) 
b = np.array(a) #np array of shape (6,1)

#empty list -> np array 
#    -> array creation category 
#array shape (6,1) 
#    -> create array of shape (6,1)
#array incrementing by 1 
#    -> create array of shape (6,1) where each element is i+1
#result = np.arrange(6)

