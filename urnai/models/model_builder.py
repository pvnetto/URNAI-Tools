class ModelBuilder():

    LAYER_INPUT = 'input'
    LAYER_OUTPUT = 'output'
    LAYER_FULLY_CONNECTED = 'fullyconn'
    LAYER_CONVOLUTIONAL = 'conv'

    def __init__(self):
        self.layers = []

    def add_input_layer(self, size, custom_shape = None):
        shape = None
        if custom_shape == None: 
            shape = [None, size]
        else: 
            shape = custom_shape

        if type(shape) == list:
            self.layers.append({
                'type' : ModelBuilder.LAYER_INPUT,
                'shape' : shape 
                })
        else:
            raise TypeError("Input layer shape should be a list with its dimensions in it.")

    def add_fullyconn_layer(self, nodes, name = "default"):
        if name == "default":
            cont = 0
            for layer in self.layers:
                if "name" in layer:
                    if "default" in layer['name']:
                        cont += 1

            name = "default" + str(cont)

        if type(nodes) == int:
            self.layers.append({
                'type' : ModelBuilder.LAYER_FULLY_CONNECTED,
                'nodes' : nodes,
                'name' : name,
                })
        else:
            raise TypeError("Fully connected layer's number of nodes should be an integer.")

    def add_output_layer(self, length):
        if type(length) == int:
            self.layers.append({
                'type' : ModelBuilder.LAYER_OUTPUT,
                'length' : length,
                })
        else:
            raise TypeError("Output layer's length should be an integer.")

    def get_model_layout(self):
        return self.layers