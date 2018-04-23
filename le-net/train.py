import tensorflow as tf
import numpy as np
import time
import matplotlib.pyplot as plt
plt.ioff()
import math


tf.reset_default_graph()
saver = tf.train.import_meta_graph("./LeNet.ckpt.meta")


X, y, current_epoch, current_step, accuracy, best_accuracy,\
training_op, training, increment_epoch, increment_step, loss,\
set_training_true, set_training_false,\
best_accuracy_placeholder, set_best_accuracy\
=tf.get_default_graph().get_collection("needed_for_training")

extra_update_ops = tf.get_collection("update_ops")


from sklearn.datasets import fetch_mldata
mnist = fetch_mldata('MNIST original')
mnist_data = mnist.data.reshape(-1,28,28,1)/255
mnist_target = mnist.target

from sklearn.model_selection import train_test_split
X_train, X_test_valid, y_train, y_test_valid = train_test_split(mnist_data, mnist_target, test_size=0.20, random_state=42)
X_test, X_valid, y_test, y_valid = train_test_split(X_test_valid, y_test_valid, test_size=0.50, random_state=42)


def get_batch(X, y, batch_size):
    random_sample_indexes = np.random.choice(X.shape[0],size=batch_size)
    return X[random_sample_indexes,:],y[random_sample_indexes]

def calculate_remaining_time(current_ep, last_ep, time_per_ep):
    remaining_epochs = last_ep - current_ep
    m, s = divmod(time_per_ep*remaining_epochs, 60)
    h, m = divmod(m, 60)
    return h,m,s

def save_image(image, name):
    plt.close()
    plt.figure(figsize=(800, 800), dpi=1)
    fig = plt.imshow(image, cmap="gray")
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.axis("off")
    plt.savefig(name, bbox_inches="tight", pad_inches=0)
    plt.close()

def activation(layer_name, X_vis, sess):
    layer = tf.get_default_graph().get_tensor_by_name("LeNet/"+layer_name+"/Elu:0")
    a = sess.run(layer, feed_dict={X:X_vis[0:1]})[0]
    
    while int(math.sqrt(a.shape[2])) != math.sqrt(a.shape[2]):
        a = np.append(a, np.zeros(shape=(a.shape[0],a.shape[1],1)), axis=2)
        
        
    a = a.reshape(a.shape[0], a.shape[1], int(math.sqrt(a.shape[2])), int(math.sqrt(a.shape[2])))
    act_img = np.zeros(shape=(a.shape[0]*a.shape[2],\
                              a.shape[1]*a.shape[2]))
    
    for row in range(a.shape[2]):
        for column in range(a.shape[3]):
            act_img[row*a.shape[0]:(row+1)*a.shape[0], column*a.shape[1]:(column+1)*a.shape[1]]\
            = a[:,:,row,column]
    
    return act_img


n_epochs = 600
batch_size = 200
step_per_save = 150

with tf.Session() as sess:
    saver.restore(sess,"./LeNet.ckpt")
    for epoch in range(current_epoch.eval(), n_epochs):
        
        start_epoch = time.time()
        
        sess.run(set_training_true)
        print("Epoch: {}".format(current_epoch.eval()+1))
        
        steps_per_epoch = X_train.shape[0] // batch_size
        
        
        sess.run(set_training_true) 
        for iteration in range(steps_per_epoch):
            
            X_batch, y_batch = get_batch(X_train, y_train, batch_size)
            losss = sess.run(loss, {X:X_batch,y:y_batch})
            a=sess.run([training_op, extra_update_ops], feed_dict={X:X_batch,
                                                                 y:y_batch})
   
        
            sess.run(set_training_false)   
            sess.run(increment_step)
            if current_step.eval() % step_per_save == 1:
                #print("Loss: {}".format(sess.run(loss, {X:X_batch,y:y_batch})))
                try:
                    act1 = activation("conv1", X_test[0:1], sess)
                    act3 = activation("conv3", X_test[0:1], sess)
                    act5 = activation("conv5", X_test[0:1], sess)
                    
                    save_image(act1, "hidden_layers/conv1_{}".format(current_step.eval()))
                    save_image(act3, "hidden_layers/conv3_{}".format(current_step.eval()))
                    save_image(act5, "hidden_layers/conv5_{}".format(current_step.eval()))
                    print("Image saved for step: {}/{} of epoch {}"\
                          .format(current_step.eval()%steps_per_epoch,
                                  steps_per_epoch,current_epoch.eval()+1))
                    
                except:
                    print("Image save failed for step: {}/{} of epoch {}"\
                          .format(current_step.eval()%steps_per_epoch,
                                  steps_per_epoch,current_epoch.eval()+1))
            
            
                
            
        
        sess.run(increment_epoch)
        accuracy_valid = sess.run(accuracy, feed_dict={X:X_valid,
                                                 y:y_valid})

        print("Validation accuracy is {}".format(accuracy_valid))
        if accuracy_valid > best_accuracy.eval():
            sess.run(set_best_accuracy, {best_accuracy_placeholder:accuracy_valid})
            print("New best accuracy:{}!".format(accuracy_valid))
            saver.save(sess, "./LeNet_best.ckpt")
        
        saver.save(sess, "./LeNet.ckpt")    
    
    
        end_epoch = time.time()
        seconds_per_epoch = end_epoch-start_epoch    
        h,m,s = calculate_remaining_time(sess.run(current_epoch), n_epochs, seconds_per_epoch)
        print("{0:.2f} seconds per epoch".format(seconds_per_epoch)) 
        print("Estimated time remaining: %d:%02d:%02d" % (h, m, s))
        
    
