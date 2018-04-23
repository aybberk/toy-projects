import tensorflow as tf
input_list = []
for n in range(16):
    input_list_element = [0]*16
    input_list_element[n] = 1
    input_list.append(input_list_element)

input_vec = tf.placeholder(tf.float32, [None, 16])
output_vec = tf.placeholder(tf.float32, [None, 16])

hidden_layer1 = tf.layers.dense(inputs=input_vec,
                               units = 8,
                               activation = tf.nn.sigmoid,
                               kernel_initializer=tf.variance_scaling_initializer)
hidden_layer2 = tf.layers.dense(inputs=hidden_layer1,
                               units = 4,
                               activation = tf.nn.sigmoid,
                               kernel_initializer=tf.variance_scaling_initializer)
hidden_layer3 = tf.layers.dense(inputs=hidden_layer2,
                               units = 8,
                               activation = tf.nn.sigmoid,
                               kernel_initializer=tf.variance_scaling_initializer)
output_layer = tf.layers.dense(inputs = hidden_layer3,
                               units = 16,
                               activation = tf.nn.sigmoid,
                               kernel_initializer=tf.variance_scaling_initializer)


loss = tf.losses.mean_squared_error(output_layer, output_vec)

optimizer = tf.train.AdamOptimizer(0.1)
train = optimizer.minimize(loss)
init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    for n in range(1000000):
        train.run(feed_dict = {input_vec: input_list,
                               output_vec: input_list})
        if(n%100 == 0):
            print("Epoch: ", n)
            print("Loss: ", loss.eval(feed_dict={input_vec: input_list,
                                             output_vec: input_list}))

    final_hidden_repr = (sess.run(hidden_layer2, feed_dict= {input_vec: input_list}))
    print("Final hidden layer represantation: ")
    for elem in final_hidden_repr:
        print(['%.2f' % n for n in elem])
