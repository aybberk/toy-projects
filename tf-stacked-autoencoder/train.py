import tensorflow as tf
import numpy as np
import time
import matplotlib.pyplot as plt
plt.ioff()

###############################################################################

tf.reset_default_graph()
saver = tf.train.import_meta_graph("./model.ckpt.meta")

###############################################################################

G = tf.get_default_graph()

current_epoch = G.get_tensor_by_name("current_epoch:0")
current_step = G.get_tensor_by_name("current_step:0")
current_time = G.get_tensor_by_name("current_time:0")
epochs_no_improve = G.get_tensor_by_name("epochs_no_improve:0")
hidden1 = G.get_tensor_by_name("hidden1:0")
hidden2 = G.get_tensor_by_name("hidden2:0")
hidden3 = G.get_tensor_by_name("hidden3:0")
hidden4 = G.get_tensor_by_name("hidden4:0")
hidden5 = G.get_tensor_by_name("hidden5:0")
increment_current_epoch = G.get_operation_by_name("increment_current_epoch")
increment_current_step = G.get_operation_by_name("increment_current_step")
increment_epochs_no_improve = G.get_operation_by_name("increment_epochs_no_improve")
lowest_loss_ph = G.get_tensor_by_name("lowest_loss_ph:0")
lowest_loss = G.get_tensor_by_name("lowest_loss:0")
new_phase = G.get_operation_by_name("new_phase")
output = G.get_tensor_by_name("output:0")
phase =  G.get_tensor_by_name("phase:0")
phase1_loss = G.get_tensor_by_name("phase1_loss:0")
phase2_loss = G.get_tensor_by_name("phase2_loss:0")
phase3_loss = G.get_tensor_by_name("phase3_loss:0")
phase1_train_op = G.get_operation_by_name("phase1_train_op")
phase2_train_op = G.get_operation_by_name("phase2_train_op")
phase3_train_op = G.get_operation_by_name("phase3_train_op")
reset_epochs_no_improve = G.get_operation_by_name("reset_epochs_no_improve")
set_lowest_loss = G.get_operation_by_name("set_lowest_loss")
time_ph = G.get_tensor_by_name("time_ph:0")
update_time = G.get_operation_by_name("update_time")
weights1 = G.get_tensor_by_name("weights1:0")
weights2 = G.get_tensor_by_name("weights2:0")
weights3 = G.get_tensor_by_name("weights3:0")
weights4 = G.get_tensor_by_name("weights4:0")
weights5 = G.get_tensor_by_name("weights5:0")
weights6 = G.get_tensor_by_name("weights6:0")
X = G.get_tensor_by_name("X:0")

###############################################################################

from sklearn.datasets import fetch_mldata
mnist = fetch_mldata('MNIST original')
X_train = mnist.data/255
y_train = mnist.target

###############################################################################

def get_batch(X, y, batch_size):
    random_sample_indexes = np.random.choice(X.shape[0],size=batch_size)
    return X[random_sample_indexes,:],y[random_sample_indexes]

def save_info(filename, phase, epoch, loss, time):
    with open(filename, "a") as f: 
        f.write("Phase {}:\n".format(phase))
        f.write("-Final Loss: {}\n".format(loss))
        f.write("-Lasted: {} minutes \n".format(int(time / 60)))
###############################################################################
    
batch_size = 5000
step_per_epoch = X_train.shape[0] // batch_size 
with tf.Session() as sess:
    saver.restore(sess, "./model.ckpt")
    while True:
        start_time = time.time()
        if sess.run(phase) == 1:
            loss = phase1_loss
            train_op = phase1_train_op
        elif sess.run(phase) == 2:
            loss = phase2_loss
            train_op = phase2_train_op            
        else:
            loss = phase3_loss
            train_op = phase3_train_op
            
            
        for step in range(step_per_epoch):
            X_batch, _ = get_batch(X_train, y_train, batch_size)
            sess.run(train_op, 
                     feed_dict = {X: X_batch})
            sess.run(increment_current_step)
        sess.run(increment_current_epoch)

        print("Training Phase: {}".format(sess.run(phase)))
        print("Epoch: {}".format(sess.run(current_epoch)))
        loss_value = sess.run(loss, {X:X_train})
        print("Loss: {}".format(loss_value))
        end_time = time.time()
        duration = end_time - start_time
        sess.run(update_time,
                 feed_dict = {time_ph: duration})
        
        
        wait_for = sess.run(current_epoch) // 10 + 1
        if loss_value < sess.run(lowest_loss) * (1.0 - 1e-4):
            print("New best performance!")
            sess.run([set_lowest_loss, reset_epochs_no_improve],
                     feed_dict = {lowest_loss_ph:loss_value})
            saver.save(sess, "./best_model.ckpt")
            
            
        else:
            sess.run(increment_epochs_no_improve)
            print("{}/{} epochs without improvement"\
                  .format(sess.run(epochs_no_improve), wait_for))
        saver.save(sess, "./model.ckpt")
        if(sess.run(epochs_no_improve) > wait_for):
            print("Finished phase {}.".format(sess.run(phase)))
            save_info(filename = "info.txt",
                      phase = sess.run(phase), 
                      epoch = sess.run(current_epoch) - 1, 
                      loss = sess.run(lowest_loss),
                      time = sess.run(current_time))
            sess.run(new_phase)
            if sess.run(phase) > 3:
                print("Finished training.")
                break
        
            
        

