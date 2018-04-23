# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import time
import matplotlib.pyplot as plt
plt.ioff()
import math

###############################################################################

tf.reset_default_graph()
saver = tf.train.import_meta_graph("./model.ckpt.meta")

###############################################################################

G = tf.get_default_graph()

output = G.get_tensor_by_name("output:0")
X = G.get_tensor_by_name("X:0")
weights1 = G.get_tensor_by_name("weights1:0")

###############################################################################

from sklearn.datasets import fetch_mldata
mnist = fetch_mldata('MNIST original')
X_train = mnist.data/255
y_train = mnist.target

###############################################################################

def get_batch(X, y, batch_size):
    random_sample_indexes = np.random.choice(X.shape[0],size=batch_size)
    return X[random_sample_indexes,:],y[random_sample_indexes]

def kernels_of(matrix):
    kernels = matrix.transpose()
    k_size = int(math.sqrt(kernels.shape[1]))
    kernels = kernels.reshape(-1, k_size, k_size)
    n_n = int(math.sqrt(kernels.shape[0]))
    img = np.zeros(shape=(k_size*n_n, k_size*n_n), dtype = np.float32)
    for row in range(n_n):
        row_start = row*k_size
        for column in range(n_n):
            column_start = column*k_size
            kernel = kernels[row*n_n + column]
            kernel = kernel - kernel.min()
            kernel = kernel/kernel.max()
            img[row_start:row_start+k_size, column_start:column_start+k_size] = kernel
    return img

def save_image(image, name):
    plt.figure(figsize=(300, 300), dpi=1)
    fig = plt.imshow(image, cmap="gray")
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.axis("off")
    plt.savefig(name, bbox_inches="tight", pad_inches=0)
    plt.close()

###############################################################################
    
with tf.Session() as sess:
    saver.restore(sess, "./best_model.ckpt")
    out, w1 = sess.run([output, weights1], {X:X_train})
    
    #Reconstructions
    for n in range(0, X_train.shape[0], 1000):
        image = X_train[n].reshape(28,28)
        image = image - image.min()
        image = image / image.max()
        reconstruction = out[n].reshape(28,28)
        reconstruction = reconstruction - reconstruction.min()
        reconstruction = reconstruction / reconstruction.max()
        saved = np.concatenate([image, reconstruction], axis=1)
        save_image(saved, "reconstructions/sample{}".format(n))
    #Hidden layer kernels
    for n in range(0,w1.shape[1],5):
        save_image(w1[:,n].reshape(28,28), "hidden_units/hidden{}".format(n))
    
    

