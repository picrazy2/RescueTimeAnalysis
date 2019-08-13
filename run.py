import kmeans_create
import kmeans_from_txt
import kmeans_tune
import sys
import lfa

if __name__ == '__main__':
	args = sys.argv[1:]
	if len(args) < 1:
		print('Options include: lfa, kmeans create, kmeans load, kmeans tune') 
	elif args[0] == 'lfa':
		lfa.run()
	elif args[0] == 'kmeans':
		if len(args) < 2:
			print('Specify create, load, or tune.')
		elif args[1] == 'create':
			kmeans_create.run()
		elif args[1] == 'load':
			kmeans_from_txt.run()
		elif args[1] == 'tune':
			kmeans_tune.run()
		else:
			print('Unrecognized command.')
	else:
		print('Unrecognized command.')