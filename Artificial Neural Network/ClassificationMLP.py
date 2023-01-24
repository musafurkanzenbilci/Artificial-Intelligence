import numpy as np


# class Network :
# Create Directed Acyclic Network of given number layers .


def BackPropagationLearner(X, y, net, learning_rate, epochs):
    # initialize each weight with the values min_value = -0.5 , max_value =0.5
    for layer in net:
        for i in range(len(layer['weights'])):
            layer['weights'][i] = np.random.uniform(-0.5, 0.5)

    for epoch in range(epochs):
        for i in range(len(X)):
            # Activate input layer
            input_layer = X[i]
            # Forward pass
            output_layer = forward_pass(input_layer, net)
            # Error for the MSE cost function
            expected_output = np.zeros(len(output_layer))
            expected_output[y[i]] = 1
            error = expected_output - output_layer
            # Backward pass
            back_propagation(error, net)
            # Update weights
            update_weights(net, learning_rate)
    return net


def forward_pass(inputs, net):
    for i in range(len(net)):
        layer = net[i]
        dot_product = np.dot(inputs, layer['weights'])
        outputs = sigmoid(dot_product)
        layer['output'] = outputs
        inputs = outputs
    return outputs


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def back_propagation(error, net):
    for i in range(len(net) - 1, -1, -1):
        layer = net[i]
        if i != len(net) - 1:
            next_layer = net[i + 1]
            layer['error'] = np.dot(next_layer['error'], next_layer['weights'].T) * sigmoid_derivative(layer['output'])
        else:
            layer['error'] = error * sigmoid_derivative(layer['output'])


def sigmoid_derivative(x):
    return x * (1 - x)


def update_weights(net, learning_rate):
    for i in range(len(net)):
        layer = net[i]
        if i != 0:
            previous_layer = net[i - 1]
            layer['weights'] += learning_rate * np.dot(previous_layer['output'].T, layer['error'])


def NeuralNetLearner(X, y, hidden_layer_sizes=None, learning_rate=0.01, epochs=100):
    # If no hidden_layer_sizes specified, default to one hidden layer with 3 units
    if hidden_layer_sizes is None:
        hidden_layer_sizes = [3]
    # Initialize empty list to hold layers of the network
    net = []
    # Create input layer with randomly initialized weights
    input_layer = {'weights': np.random.rand(X.shape[1], hidden_layer_sizes[0])}
    net.append(input_layer)
    # Create hidden layers with randomly initialized weights
    for i in range(len(hidden_layer_sizes) - 1):
        hidden_layer = {'weights': np.random.rand(hidden_layer_sizes[i], hidden_layer_sizes[i + 1])}
        net.append(hidden_layer)
    # Create output layer with randomly initialized weights
    output_layer = {'weights': np.random.rand(hidden_layer_sizes[-1], len(np.unique(y)))}
    net.append(output_layer)
    # Train the network using BackPropagationLearner function
    net = BackPropagationLearner(X, y, net, learning_rate, epochs)

    def predict(example):
        # activate input layer
        input_layer = example
        # forward pass
        output_layer = forward_pass(input_layer, net)
        # find the max node from output nodes
        prediction = np.argmax(output_layer)
        return prediction

    return predict


from sklearn import datasets

iris = datasets.load_iris()
X = iris.data
y = iris.target

nNL = NeuralNetLearner(X, y)
print(nNL([4.6, 3.1, 1.5, 0.2]))  # 0
print(nNL([6.5, 3., 5.2, 2.]))  # 2
