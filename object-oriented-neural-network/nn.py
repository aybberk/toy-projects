import csv
from random import uniform
learningRate = 0.1
bias = True
epochs = 30000


                    ##SYNAPSE CLASS##
class Synapse(object):
    
    def __init__(self, inputNeuron, outputNeuron):
        self.inputNeuron = inputNeuron
        self.outputNeuron = outputNeuron
        self.weight = uniform(-0.5, 0.5) 
        self.delta = None

    def activate(self):
        return self.inputNeuron.activate() * self.weight

    def calculateDelta(self):
        
        self.delta = learningRate \
                     * self.outputNeuron.calculateDelta() \
                     * self.inputNeuron.activate()

    def applyDelta(self):
        self.weight += self.delta
        self.delta = None
                    ##NEURON CLASSES##
class BiasNode(object):

    def __init__(self):
        if bias == True:
            self.output = 1
        else:
            self.output = 0

    def activate(self):
        return self.output

class InputNeuron(object):
    
    def __init__(self):
        self.outputSynapses = []
        self.input = None 

    def connectOutputTo(self, neuron):
        syn = Synapse(self, neuron)
        neuron.inputSynapses.append(syn)
        self.outputSynapses.append(syn)

    def activate(self):
        return self.input
        

class HiddenNeuron(object):

    def __init__(self):
        
        self.outputSynapses = []
        bias = BiasNode()
        syn = Synapse(bias, self)
        self.inputSynapses = [syn]
        self.output = None
        self.delta = None

    def connectOutputTo(self, neuron):
        
        syn = Synapse(self, neuron)
        neuron.inputSynapses.append(syn)
        self.outputSynapses.append(syn)
    
    def activate(self):
        
        if self.output == None:
            net = sum([synapse.activate() for synapse in self.inputSynapses])
            output = 1/(1 + 2.71828 ** -net)
            self.output = output
            return output
        else:
            return self.output

    def calculateDelta(self):
        
        if self.delta == None:
            output = self.activate()
            delta = output \
                * (1 - output) \
                * sum([syn.weight * syn.outputNeuron.calculateDelta() \
                    for syn in self.outputSynapses])
            self.delta = delta
            return delta
        else:
            return self.delta

class OutputNeuron(object):

    def __init__(self):

        self.inputSynapses = [Synapse(BiasNode(), self)]
        self.output = None
        self.delta = None
        self.target = None

    
    def activate(self):
        if self.output == None:
            net = sum([synapse.activate() for synapse in self.inputSynapses])
            output = 1/(1 + 2.71828 ** -net)
            self.output = output
            return output      
        else:
            return self.output

    def calculateDelta(self):
        if self.delta == None:
            output = self.activate() 
            delta = (self.target - output) * output * (1 - output)
            self.delta = delta
            return delta
        else:
            return self.delta

                ##LAYER CLASSES##
class InputLayer(object):
    
    def __init__(self, neuronNumber):
        
        self.neurons = []
        self.nextLayer = []
        self.inputVector = []
        for n in range(neuronNumber):
            self.neurons.append(InputNeuron())
    
    def connectOutputTo(self, nextLayer):

        self.nextLayer = nextLayer
        nextLayer.prevLayer = self
        for neuron in self.neurons:
            for neuron2 in nextLayer.neurons:
                neuron.connectOutputTo(neuron2)

    def takeInput(self, inputVector):
        
        self.inputVector = inputVector    
        for n in range(len(inputVector)):
            self.neurons[n].input = inputVector[n] 


class HiddenLayer(object):
    
    def __init__(self, neuronNumber):
        
        self.neurons = []
        for n in range(neuronNumber):
            self.neurons.append(HiddenNeuron())
    
    def connectOutputTo(self, nextLayer):
        self.nextLayer = nextLayer
        nextLayer.prevLayer = self
        for neuron in self.neurons:
            for neuron2 in nextLayer.neurons:
                neuron.connectOutputTo(neuron2)


class OutputLayer(object):
    
    def __init__(self, neuronNumber):
        
        self.neurons = []
        for n in range(neuronNumber):
            self.neurons.append(OutputNeuron())
            
    def giveOutput(self):
        
        outputVector = [neuron.activate() for neuron in self.neurons]
        return outputVector

    def setTarget(self, targetVector):
        
        for tup in zip(targetVector, self.neurons):
            tup[1].target = tup[0]
                ## NETWORK CLASS##

class FeedforwardNetwork(object):

    def __init__(self, inn, hidn, outn):
        
        self.inputLayer = InputLayer(inn)
        self.hiddenLayer = HiddenLayer(hidn)
        self.outputLayer = OutputLayer(outn)

        self.inputLayer.connectOutputTo(self.hiddenLayer)
        self.hiddenLayer.connectOutputTo(self.outputLayer)

    def forwardPropagate(self, inputVector, outputVector):
        
        self.outputLayer.setTarget(outputVector) 
        self.inputLayer.takeInput(inputVector)
        return self.outputLayer.giveOutput()
        

    def backPropagate(self):

        for neuron in self.inputLayer.neurons:
            for syn in neuron.outputSynapses:
                syn.calculateDelta()

        for neuron in self.hiddenLayer.neurons:
            for syn in neuron.outputSynapses:
                syn.calculateDelta()
            neuron.inputSynapses[0].calculateDelta()
            
        for neuron in self.outputLayer.neurons:
            neuron.inputSynapses[0].calculateDelta()

    def applyDeltas(self):
        for neuron in self.inputLayer.neurons:
            for syn in neuron.outputSynapses:
                syn.applyDelta()

        for neuron in self.hiddenLayer.neurons:
            for syn in neuron.outputSynapses:
                syn.applyDelta()
            neuron.inputSynapses[0].applyDelta()

        for neuron in self.outputLayer.neurons:
            neuron.inputSynapses[0].applyDelta()



                                
    def reset(self):
        for n in self.inputLayer.neurons:
            n.input = None
        for n in self.hiddenLayer.neurons:
            n.output = None
            n.delta = None
        for n in self.outputLayer.neurons:
            n.output = None
            n.delta = None



features = []
labels = []
labelsOneHot = []
with open('datamnist.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter = ',')
    for row in readCSV:
        labels.append(int(row[0]))
        features.append([float(n)/200 for n in row[1:]])

for n in range(len(labels)):
    labelsOneHot.append([0]*10)
    labelsOneHot[n][labels[n]] = 1 



#ffNet = FeedforwardNetwork(784, 40, 10)
#for n in range(epochs):
#    error = 0
#    for i in range(500):
#
#        inputVector = features[i]
#        targetVector = labelsOneHot[i] 
#        outputVector = ffNet.forwardPropagate(inputVector, targetVector)
#        ffNet.backPropagate()
#        ffNet.applyDeltas()
#        ffNet.reset()
#
#    error += sum((a[0]-a[1])**2 for a in zip(targetVector, outputVector)) / 2
#    print("Epoch: ", n+1)
#    print("Error: ", error)




ffNet = FeedforwardNetwork(16, 4, 16)

inOutMatrix = []
for n in range(16):
    element = [0]*16
    element[n] = 1
    inOutMatrix.append(element)




for n in range(epochs):
    error = 0
    for a in range(16):
        inn = inOutMatrix[a]
        out = ffNet.forwardPropagate(inn, inn)
        ffNet.backPropagate()
        ffNet.applyDeltas()
        ffNet.reset()
        error += sum((a[0]-a[1])**2 for a in zip(inn, out)) / 2
    
    error /= 16
    if(n%1000 == 0):
        print("Epoch: ", n, "\nError: ", error)


print("Training completed!")

for a in range(16):
    print("Input:")
    print(inOutMatrix[a])
    print("Output:")
    print(ffNet.forwardPropagate(inOutMatrix[a]))
    print("Hidden Layer Representation")
    print([n.output for n in ffNet.hiddenLayer.neurons])
    ffNet.reset()
