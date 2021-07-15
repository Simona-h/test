import os
import glob
from skimage.io import imread
import numpy as np
from scipy.spatial.distance import cdist,squareform
from skimage.feature import hog
import matplotlib.pyplot as plt
import palsgraph
import networkx as nx

def get_image_paths(data_path, categories, num_train_per_cat):
    '''
    This function returns lists containing the file path for each image, 
    as well as lists with the label of each image. 
    By default both lists will be 1100*1, where each entry is a char array (or string).
    '''
    num_categories = len(categories) # number of scene categories.
    image_paths = [None] * (num_categories * num_train_per_cat)
    
    # The name of the category for each training and test image. With the
    # default setup, these arrays will actually be the same, but they are built
    # independently for clarity and ease of modification.
    labels = [None] * (num_categories * num_train_per_cat)
    genres = [None] * (num_categories * num_train_per_cat)
    for i,cat in enumerate(categories):
        images = glob.glob(os.path.join(data_path, cat, '*.webp'))
        for j in range(num_train_per_cat):
            #print(j,len(images),i,len(image_paths))
            image_paths[i * num_train_per_cat + j] = images[j]
            labels[i * num_train_per_cat + j] = os.path.join(cat,str(j))
            genres[i * num_train_per_cat + j] = os.path.join(cat)
    return (image_paths, labels,genres)

# feature abstraction: HOG; CNN; SIFT
'''
input: image_paths: n*1 ;
return: feature_vectors_images: n * m, m is the feature of each picture
'''
def get_feature_hog(image_paths):
    image_list = [imread(f) for f in image_paths]
    feature_vectors_images = []
    for image in image_list:
        feature_vectors = hog(image, feature_vector=True,
                              visualize=False)
        feature_vectors_images.append(feature_vectors)
    #print(np.array(feature_vectors_images).shape)
    return feature_vectors_images

def get_feature_sift(image_path):
    feature_vectors_images = None
    return feature_vectors_images

def get_feature_cnn(image_path):
    feature_vectors_images = None
    return feature_vectors_images

def get_feature_autoencoder(image_path):
    feature_vectors_images = None
    return feature_vectors_images

# similarity/dissamilarity matrix
def get_distance(features,num_pictures):
    distance = cdist(features,features, 'euclidean')
    return distance

# construct edges between vertices
def get_graph(dismat,threshold):
    adjmat = np.ones(dismat.shape)
    adjmat[(dismat >= threshold)] = 0
    
    #plt.figure(figsize=(6,6))
    #plt.imshow(adjmat)
    #plt.show()
    return adjmat

def main():
    categories = ['animal','animation','dance','fashion','food','game','kichiku','knowledge','life','music','tech']
    num_train_per_cat = 5
    num_pictures = len(categories)*num_train_per_cat
    data_path = './img/'
    threshold = 19.2
    image_paths,labels,genres = get_image_paths(data_path, categories, num_train_per_cat)
    features = get_feature_hog(image_paths)
    distance = get_distance(features,num_pictures)
    #plt.figure(figsize=(15, 4))
    #_ = plt.hist(squareform(distance), bins=200)
 
    # Using adjmat or G for CD
    adjmat = get_graph(distance,threshold)
    #print(adjmat.shape)
    G = palsgraph.make_graph(adjmat, labels=labels, show_singletons=False)
    nx.draw(G, with_labels=True,font_size=10,font_color='darkslategray',edge_color='gray')

    #G1 = palsgraph.make_graph(adjmat, labels=genres, show_singletons=False)
    #nx.draw(G1, with_labels=True,font_size=10,font_color='darkslategray',edge_color='gray')


    
