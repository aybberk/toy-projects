import tensorflow as tf
from functools import partial
import os

try:
    for file in os.listdir("hidden_layers"):
        os.remove("hidden_layers/"+file)
except:
    os.mkdir("hidden_layers")

tf.reset_default_graph()

with tf.name_scope("Inputs"):
    X = tf.placeholder(tf.float32, shape=(None, 28, 28, 1), name="X")
    y = tf.placeholder(tf.int32, shape=(None), name="y")


with tf.name_scope("Global_Parameters") as scope:
    num_epochs = tf.constant(300, dtype=tf.int32)
    batch_size = tf.constant(10000, dtype=tf.int32)
    current_epoch = tf.Variable(initial_value=0, trainable=False, dtype=tf.int32)
    current_step = tf.Variable(initial_value=0, trainable=False, dtype=tf.int32)
    training = tf.Variable(initial_value=True, trainable=False, dtype=tf.bool)
    best_accuracy = tf.Variable(0, name='best_accuracy', dtype = tf.float32, trainable = False)

    
with tf.name_scope("Assign_Operations"):
    increment_epoch = tf.assign(current_epoch, current_epoch+1)
    increment_step = tf.assign(current_step, current_step+1)
    set_training_true = tf.assign(training, True)
    set_training_false = tf.assign(training, False)
    best_accuracy_placeholder = tf.placeholder(best_accuracy.dtype, best_accuracy.shape)
    set_best_accuracy = tf.assign(best_accuracy, best_accuracy_placeholder)
    

poollayer = partial(tf.layers.average_pooling2d, pool_size=2, strides=2)
 
def convlayer(inputs,
              filters,
              kernel_size=(5),
              strides=1,
              padding="SAME",
              batch_norm=False,
              momentum=0.9,
              activation = tf.nn.elu,
              name=None):
    
    with tf.name_scope(name):
        conv = tf.layers.conv2d(inputs=inputs, 
                                filters=filters, 
                                kernel_size=kernel_size,
                                strides=strides,
                                padding=padding,
                                name=name+"convolution")
        if batch_norm == True:
            bn = tf.layers.batch_normalization(conv, 
                                               momentum=momentum,
                                               training=training,
                                               epsilon=1e-3)
        else:
            bn = conv
            
        act = activation(bn)
        return act  
    
with tf.name_scope("LeNet") as scope:
    
#    convlayer3 = partial(tf.layers.conv2d, kernel_size=5, padding="VALID")
#    convlayer2 = partial(tf.layers.batch_normalization, inputs=convlayer3, training=training, momentum=0.9)
#    convlayer =  partial(tf.nn.elu, features=convlayer2)
#    bn = partial(tf.layers.batch_normalization, training=training, momentum = 0.9)
    #original paper used tanh, but i prefer elu 
    #original paper used no padding, i used YES PADDING :3
    
    

    #conv layer filters must be square numbers for visualization purposes
    #so i changed them slightly 
    conv1 = convlayer(X, filters=6, name="conv1", batch_norm=False)
    avgpool2 = poollayer(conv1, name="avgpool2")
    conv3 = convlayer(avgpool2, filters=16, name="conv3", batch_norm=False)   
    avgpool4 = poollayer(conv3, name="avgpool4")
    conv5 = convlayer(avgpool4, filters=120, name="conv5", batch_norm=False)
    avgpool6 = poollayer(conv5, name="avgpool4")
    flatten = tf.layers.flatten(avgpool6)
    full = tf.layers.dense(flatten, units=84, activation=tf.nn.elu)  
    dropout = tf.layers.dropout(full, rate=0.5, training=training)
    #original paper does not have dropout layer, but it definitely helps
    #so i decided to use one 
    logits = tf.layers.dense(full, units=10)
    #original paper uses rbf but i prefer softmax for output layer,
    # which will be defined at loss function
    
with tf.name_scope("Evaluation"):
    loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits), name="loss")
    correct = tf.nn.in_top_k(logits, y, k=1)
    accuracy = tf.reduce_mean(tf.cast(correct, dtype=tf.float32), axis=0)
    
with tf.name_scope("Optimizer") as scope:
    optimizer = tf.train.AdamOptimizer()
    train_op = optimizer.minimize(loss)
    
 
with tf.name_scope("Initializer") as scope:
    init = tf.global_variables_initializer()

with tf.name_scope("Loss"):    
    x_entropy_loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits))
    
    x_entropy_loss = tf.add_n([x_entropy_loss] + tf.get_collection('regularization_losses'))               
                                                                                   
with tf.name_scope("Training"):
    optimizer = tf.train.AdamOptimizer(learning_rate=0.0001)
    training_op = optimizer.minimize(x_entropy_loss, name="training_op")
    
    
with tf.name_scope("Evaluation"):
    correct = tf.nn.in_top_k(logits, y, 1)
    accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")


for op in (X, y, current_epoch, current_step, accuracy, 
           best_accuracy, training_op, training, 
           increment_epoch, increment_step, loss,
           set_training_true, set_training_false,
           best_accuracy_placeholder, set_best_accuracy):
    
    tf.get_default_graph().add_to_collection("needed_for_training", op)
    
    
for op in (X, y, accuracy, training):
    tf.get_default_graph().add_to_collection("needed_for_test_and_visual", op)
    
init = tf.global_variables_initializer()
saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(init)
    saver.save(sess,"./LeNet.ckpt")
    
    
    
    
    