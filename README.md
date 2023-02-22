# distributed-image-processing
This project implements a parallel image processing pipeline distributed among multiple nodes

## Design
 The client makes an RPC call to the server and the server selects a compute node and tasks that node to do an image processing operation. One job will have multiple tasks and all tasks happen in parallel on different compute nodes.
 The client calls one function - submit_request along with 2 arguments - the base path of the directory which contains all the images and whether we want random or load-balancing distribution of tasks among the compute nodes.
The server takes the request, and selects a node randomly from the machine.txt file and assigns it an image processing task. The server-computenode interface has 2 functions - execute and delayed_execute. The function to call is selected based on what kind of task distribution is expected for the job. These functions expect the base path of file along with the filename of the image to be processed as arguments.
The computenode implements the function to actually process these images using the opencv library. Compute node server takes in load-probability as a command line argument. Depending on the value of load-probability, the node might sleep for a few seconds before starting to execute the task or the node might reject the task itself. If the node rejects the task, the server has to retry executing that task to some other node which might pick the task.

## Operation
The client gets the ip of the server from the machine.txt. Creates a connection to the server, and sends the request.
The server gets all the eligible files from the source path. For each of the files, it creates a new thread and based on the strategy, it selects computenode to submit job request to. Makes sure all the requests are submitted. Then prints the amount of time it took.
computenodes are the machines which will process the image using opencv and write the processed image to the output_dir folder. The computenodes delay and reject requests from servers based on the load probability value. 
To run the project we need to have installed thrift and opencv into the system and once the installation is ready. Import the code into the desired location and run the following commands in the linux terminal where the project is located: 

To start the Nodes : 
```python3 computenode.py <load_probability>```

To start the Server 
```python3 server.py```

To start the Client 
```python3 client.py```

Once the job is completed,processed images will be saved in data/output_dir location.

