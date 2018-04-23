# LeNet-with-some-tweaks
Implementation of LeNet(Yann LeCun, 1995) with some modifications.

<ul><b>Modifications:</b>
  <li> Original paper used tanh at hidden layers while this implementation used ELU(Exponential Linear Unit). </li>
  <li> Original paper used RBF at final layer while this implementation used softmax. </li>
  <li> Original paper used no padding at convolutional layers while this implementation has zero padding</li>
  <li> Original paper has no dropout at any layers, this implementation has one at the layer before logits </li>
  <li> I recently added batch normalization feature, however image saving does not work with this feature for some reason. </li>
</ul>





Run "model-init.py" to initialize the model.

Run "train.py" to continue training from the last best checkpoint. When training, hidden layer representations are saved in "hidden_layers/" for a specific input.



<ul>TODO:
  <li>code is somewhat messy. refactor.</li>
  <li><del>implement validation set</del></li>
  <li><del>add more visualization, test tools</del></li>
  <li>add a pretrained model in .ckpt format</li>
  <li><del>add batch normalization</del></li>
</ul>
