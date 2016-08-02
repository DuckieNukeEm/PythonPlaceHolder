#### From a blog post on LinkendIn by Bowen Gong
#### "Extending l-Means Algorithm for Big Data & Time Series' August 1, 2016 
#### https://www.linkedin.com/pulse/extending-k-means-algorithm-big-data-time-series-bowen-gong?trk=prof-post

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from fractions import gcd
import numpy as np

def kmeans_end(centersCollection, weights, k, max_iter):
	# only use this if skipping expand_new_x() function
	divisor = reduce(gcd, weights)
	ws = np.asarray(weights)/divisor
	x = []
	for i in xrange(0, len(centersCollection)):
		c = centersCollection[i]
		w = ws[i]
		x = x + c*int(w)
		km = KMeans(n_clusters=k, n_init=10, max_iter=max_iter, tol=0.001, random_state=0)
		km.fit(x)
	return km

# determine k value
def k_finder_stream(numbers, distortions):
	k=max(numbers)
	uniqueNumbres = list(set(numbers))
	uniqueDistortions = []
	for num in uniqueNumbres:
		subdistorts=[]
		for i in xrange(0, len(numbers)):
			if numbers[i]==num:
				subdistorts.append(distortions[i])
		uniqueDistortions.append(np.mean(subdistorts))
	numbers, distortions = zip(*sorted(zip(uniqueNumbres, uniqueDistortions)))
	for i in reversed(xrange(0, len(numbers)-1)):
		ratio = (distortions[i] - distortions[i+1]+1)/(distortions[i+1]+1)
		print ratio
		if ratio > .1:
			k = i+1
			return k
	return k
 
def expand_new_x(centersCollection, weights):
	divisor = reduce(gcd, weights)
	ws = np.asarray(weights)/divisor
	x = []
	for i in xrange(0, len(centersCollection)):
		c= centersCollection[i]
		w = ws[i]
		x = x + c*int(w)
return x

 ######################################################
# simulate data

xs=[]
weights=[]
centersCollection = []
centers = 13
chunkSize=400
numberOfChunks=1000
sampleSize = centers*chunkSize*numberOfChunks
xs,ys = make_blobs(n_samples=sampleSize, n_features=20, centers=centers, cluster_std=0.5, shuffle=True, random_state=1)
xs_collection = [xs[i:i+chunkSize] for i in xrange(0, len(xs), chunkSize)]

# learn each chunk separately
ks=[]
distorts=[]
for i in xrange(0, numberOfChunks):
	x=xs_collection[i]
	k = np.random.randint(1, chunkSize/10, 1)[0]
	km = KMeans(n_clusters=k, n_init=10, max_iter=100, tol=0.001, random_state=0)
	km.fit(x)
	kc = (km.cluster_centers_).tolist()
	centersCollection.append(kc)
	weights.append(sampleSize)
	ks.append(k)
	distorts.append(km.inertia_)
 
# use resulting centroids and weights as new learning input
new_x = expand_new_x(centersCollection, weights)

# find optimal k
k = k_finder_stream(ks, distorts)

# learn new input
km = KMeans(n_clusters=k, n_init=10, max_iter=300, tol=0.001, random_state=0)
km.fit(new_x)



