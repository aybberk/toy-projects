# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import os
tf.reset_default_graph()
###############################################################################
try:
    for file in os.listdir("hidden_units"):
        os.remove("hidden_units/"+file)
    for file in os.listdir("reconstructions"):
        os.remove("reconstructions/"+file)
except:
    os.mkdir("hidden_units")
    os.mkdir("reconstructions")
try: 
    os.remove("info.txt")
except:
    pass
###############################################################################

n_inputs =  784
n_hidden1 = 600
n_hidden2 = 400
n_hidden3 = 200
n_hidden4 = n_hidden2
n_hidden5 = n_hidden1
n_outputs = n_inputs

###############################################################################

activation = tf.nn.elu
initializer = tf.contrib.layers.variance_scaling_initializer()
regularizer = tf.contrib.layers.l2_regularizer(0.0001)

###############################################################################

X = tf.placeholder(dtype = tf.float32,
                   shape = [None, 784],
                   name = "X")

###############################################################################

weights1_init = initializer(shape = [n_inputs, n_hidden1])
weights2_init = initializer(shape = [n_hidden1, n_hidden2])
weights3_init = initializer(shape = [n_hidden2, n_hidden3])
weights4_init = initializer(shape = [n_hidden3, n_hidden4])
weights5_init = initializer(shape = [n_hidden4, n_hidden5])
weights6_init = initializer(shape = [n_hidden5, n_outputs])

weights1 = tf.Variable(initial_value = weights1_init,
                       dtype = tf.float32,
                       name = "weights1")
weights2 = tf.Variable(initial_value = weights2_init,
                       dtype = tf.float32,
                       name = "weights2")
weights3 = tf.Variable(initial_value = weights3_init,
                       dtype = tf.float32,
                       name = "weights3")
weights4 = tf.Variable(initial_value = weights4_init,
                       dtype = tf.float32,
                       name = "weights4")
weights5 = tf.Variable(initial_value = weights5_init,
                       dtype = tf.float32,
                       name = "weights5")
weights6 = tf.Variable(initial_value = weights6_init,
                       dtype = tf.float32,
                       name = "weights6")

bias1 = tf.Variable(tf.zeros(shape = n_hidden1), 
                    name = "bias1")
bias2 = tf.Variable(tf.zeros(shape = n_hidden2), 
                    name = "bias2")
bias3 = tf.Variable(tf.zeros(shape = n_hidden3), 
                    name = "bias3")
bias4 = tf.Variable(tf.zeros(shape = n_hidden4), 
                    name = "bias4")
bias5 = tf.Variable(tf.zeros(shape = n_hidden5), 
                    name = "bias5")
bias6 = tf.Variable(tf.zeros(shape = n_outputs), 
                    name = "bias6")

###############################################################################

hidden1 = activation(tf.matmul(X, weights1) + bias1, name = "hidden1")
hidden2 = activation(tf.matmul(hidden1, weights2) + bias2, name = "hidden2")
hidden3 = activation(tf.matmul(hidden2, weights3) + bias3, name = "hidden3")
hidden4 = activation(tf.matmul(hidden3, weights4) + bias4, name = "hidden4")
hidden5 = activation(tf.matmul(hidden4, weights5) + bias5, name = "hidden5")
output = activation(tf.matmul(hidden5, weights6) + bias6, name = "output")



optimizer = tf.train.AdamOptimizer()
#phase1
phase1_output = activation(tf.matmul(hidden1, weights6) + bias6, 
                           name = "phase1_output")
phase1_rec_loss = tf.reduce_mean(tf.square(phase1_output - X))
phase1_reg_loss = regularizer(weights1) + regularizer(weights6)
phase1_loss = tf.add(phase1_rec_loss, phase1_reg_loss,
                     name = "phase1_loss")
phase_1_train_vars = [weights1, bias1, weights6, bias6]
phase1_train_op = optimizer.minimize(phase1_loss, 
                                     var_list = phase_1_train_vars,
                                     name = "phase1_train_op")

#phase2
phase2_output = activation(tf.matmul(hidden2, weights5) + bias5, 
                           name = "phase2_output")
phase2_rec_loss = tf.reduce_mean(tf.square(phase2_output - hidden1))
phase2_reg_loss = regularizer(weights2) + regularizer(weights5)
phase2_loss = tf.add(phase2_rec_loss, phase2_reg_loss,
                     name = "phase2_loss")
phase_2_train_vars = [weights2, bias2, weights5, bias5]
phase2_train_op = optimizer.minimize(phase2_loss, 
                                     var_list = phase_2_train_vars,
                                     name = "phase2_train_op")

#phase3
phase3_output = activation(tf.matmul(hidden3, weights4) + bias4, 
                           name = "phase3_output")
phase3_rec_loss = tf.reduce_mean(tf.square(phase3_output - hidden2))
phase3_reg_loss = regularizer(weights3) + regularizer(weights4)
phase3_loss = tf.add(phase3_rec_loss, phase3_reg_loss,
                     name = "phase3_loss")
phase_3_train_vars = [weights3, bias3, weights4, bias4]
phase3_train_op = optimizer.minimize(phase3_loss, 
                                     var_list = phase_3_train_vars,
                                     name = "phase3_train_op")


###############################################################################

current_epoch = tf.Variable(initial_value = 0,
                            dtype = tf.int32,
                            trainable = False,
                            name = "current_epoch")

current_step = tf.Variable(initial_value = 0,
                           dtype = tf.int32,
                           trainable = False,
                           name = "current_step")

increment_current_epoch = tf.assign(ref = current_epoch, 
                              value = current_epoch + 1,
                              name = "increment_current_epoch")

increment_current_step = tf.assign(ref = current_step,
                             value = current_step + 1, 
                             name = "increment_current_step")

epochs_no_improve = tf.Variable(initial_value = 0,
                                    dtype = tf.int32,
                                    trainable = False,
                                    name = "epochs_no_improve")

increment_epochs_no_improve = tf.assign(ref = epochs_no_improve,
                                        value = epochs_no_improve + 1,
                                        name = "increment_epochs_no_improve")

reset_epochs_no_improve = tf.assign(ref = epochs_no_improve,
                                    value = 0,
                                    name = "reset_epochs_no_improve")

lowest_loss_ph = tf.placeholder(dtype = tf.float32,
                                shape = None,
                                name = "lowest_loss_ph")
lowest_loss = tf.Variable(initial_value = np.inf, 
                          dtype = tf.float32,
                          trainable = False,
                          name = "lowest_loss")
set_lowest_loss = tf.assign(ref = lowest_loss,
                            value = lowest_loss_ph,
                            name = "set_lowest_loss")

phase = tf.Variable(dtype = tf.int32,
                    initial_value = 1,
                    trainable = False,
                    name = "phase")

current_time = tf.Variable(dtype = tf.float32,
                           initial_value = 0,
                           trainable = False,
                           name = "current_time")

time_ph = tf.placeholder(dtype = current_time.dtype,
                         shape = current_time.shape,
                         name = "time_ph")

update_time = tf.assign(ref = current_time,
                        value = current_time + time_ph,
                        name = "update_time")

new_phase = tf.group(tf.assign(phase, phase + 1), 
                     tf.assign(current_epoch, 0),
                     tf.assign(current_step, 0),
                     tf.assign(lowest_loss, np.inf),
                     tf.assign(current_time, 0),
                     name = "new_phase")



###############################################################################



saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    saver.save(sess, "./model.ckpt")



























