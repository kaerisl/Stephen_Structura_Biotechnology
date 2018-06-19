Stephen Lu 
Structura Biotechnology Challenge

Installed Libraries:
Python 3.6.5, 
flask 1.0.2, 			-> Flask server
pymongo 3.6.1,			-> MongoDB/Python library
numpy 1.8.2, 			-> image processing
scipy 1.1.0, 			-> image processing
opencv-python 3.4.1.15 	-> image processing
scikit-image 0.14.0 	-> image processing
psutil-5.4.6 			-> measures system stats 
datetime				-> measures time

To run:
1. Ensure that flask and associated libraries are installed (I used pip install)
2. Simply type ./startup.sh
3. Server should be accessed at http://localhost:3000, via browser or curl
4. Dump and Memory Access are accessed by http://localhost:3000/dump and http://localhost:3000/mem respectively

Challenges:

With regards to ordering of the database as to improve efficiency, unfortunately I do not know the algorithm that MongoDB employs to match entries, but if 
it is doing a match search, then ordering of the primary key may not be an efficient solution, as it will take O(n) time to find any entry regardless of 
primary key. However, if MongoDB employs a schema in where it can only search up to the Nth entry, we can do a targetted input on the initial input of the 
document entry; if our database collection is always sorted in an ascending order for width, fetch time for entries should theoretically be reduced. However,
I am new to working with MongoDB and do not know its characteristics.

Some things that I would work on but are outside the scope of the challenge:
	--implement server-side saving of requests
	--implement a multi-threaded server (though I'm unfamiliar as to how this would work with the flask framework)

Closing remarks and feedback:

I found the challenge pretty interesting, it was my first time working with Flask and MongoDB, even though I have prior experience with Python and SQL, 
learning about how MongoDB approaches queries is pretty neat. Sorry if you have any issues running my scripts, I was programming on my Windows machine using
Git Bash, as I don't have memory to run my VMWare, although I do believe everything should be fully functional, but do not hesitate to contact me if there is 
a problem. 	