# aifi-challenge

You are given a directed graph that potentially can have tens of thousands of nodes and edges. You can
decide whatever data structure you like for a graph. Any programming language is OK.

SETUP
-----
To quickly run the code I decided to use a combination of FastAPI, pytest, Postman and docker-compose.
- Postman: (https://www.postman.com/downloads/)
- Docker: https://www.docker.com/products/docker-desktop/

The main motiovation behind this decision was that:

1. Didn't want to deal with venv (although this would've been just fine)
2. Setting up this logic as a service has the advantage that we approach the problem from a users' perspective (eg. plugging in a UI). 
3. This environment to be highly replicable + hot-reload container on live code changes.

So for now we use Postman to make HTTP calls to the calculation endpoints (curl also works).

To startup everything, just run the command: 

```docker-compose up --build```

The app service should come up.

To run all tests, you can do a:

```docker exec -it app python -m pytest```

I have also included a postman collection json file in the project root. Simply click on "import" at the top of Postman
to play around with sthe functionality

CODE ARCHITECTURE
-----------------

For this app we use a simple MVC pattern:
UI (Postman or Pytest) <--> API ("graphs" router) <--> Services (graphs service)

The app wraps the router and runs on a uvicorn ASGI server for any potential asynchronous calls made toe the router.


QUESTIONS
---------

**Question 1:**
In practice we favor directed graphs without cycles a.k.a. Directed Acyclic Graph. Your first task is to
write a function that decides if a directed graph is acyclic. It is OK to use 3rd party API.
Input: an arbitrary directed graph
Output: the first loop found in the graph or NULL/None

**Answer:**
The choice was to use the popular networkx as it seems to have plenty of the 
functionality required, possibly however at the cost of performance.

To prove that this works we have:
1. Postman to run the saved collection on 

```http://localhost:5000/api/graphs/acyclic```

(Remember that we are exposing the app docker container on port 5000)

The results, depending on the graph beeing acyclic or not will be of the form 

```[bool, cycle | None]```


with acyclic:

```
{
    "content": "[true, null]",
    "status_code": "201"
}
```

with cyclic (you can create one from the one above by adding a reversed edge eg. ```[27, 0]```)

```
{
    "content": "[false, [0, 92, 85, 20, 64, 27]]",
    "status_code": "201"
}
```

2. Testing:

```docker exec -it app python -m pytest test_api```

This will run 2 examples, an acyclic directeg graph (DAG) check and a cycle graph

You can run tests on the services directly:
```docker exec -it app python -m pytest test_services```


**Question 2:**
What is the runtime and memory complexity of your implementation? If you use external libraries or
API, please read its documentation and report back the complexity.

**Answer:**
From looking at the networkx documentation, they are using the Kahn alorithm for topological sorting.
Doing some further reading on this algorithm, the implications on complexity are the following:

a) Speed complexity is O(V + E) where V=Vertices and E=Edges:

    - O(E) to determine in-degree (how many incoming edges) of each node -> need to iterate through all edges of graph and update in-degree per node (cache of size V)
    - O(V) to look for all nodes that that have in-degree == 0 of the above cache, so nodes iterate through V nodes
    - O(E) for each 0 in-degree, remove it from the graph and decrement all nodes in-degree it points to, so it will depend on all the edges E again
    - O(V) for checking if in-degree of the nodes we are decrementing have reached 0 and add them to an array, this can occur up to V-1 times

    Total O(2V + 2E) = O(V + E)

b) Spatial complexity is O(V):
    
    Creating an array to store in-degree per node requires O(V), then store each node with in-degree == 0 we remove from the graph into an array of O(V)


**Question 3:**
Now that you have your cycle detector for an arbitrary directed graph, let us test it! How to
systematically generate 100 graphs of 100 nodes each? How to ensure your test graph has cycles or not?
Write your test app that can systematically generate complex graphs with cycles and graphs without
cycles. Then run your implementation on these test cases to ensure correctness.
Hint: A cycled graph can be derived from Euclidean Minimal Spanning Tree


**Comments:**
We had to tweak the probabilty of connection to create reasonable graphs (eg. not fully connected)
while considering the time performance and the ability to actually create enough edges to have a reversed one.

**Question 4:**
It is also important to be able to visualize graphs. Display your 100 test graphs in a 25 x 4 grid. Each
graph should be colored red. If the graph has a cycle, mark that subgraph as black. Use your creativity
how to visualize graphs in their most intuitive forms. Please save the graphics as either PDF or PNG file.

**Answer**

Use Postman POST

```http://127.0.0.1:5000/api/graphs/draw```

with an input such as eg.

```
{
	"acyclic_flags_list": [
		false, true, true, false, false, true, false, false, false, true, 
	    true, true, false, false, true, false, true, true, false, true, 
	    true, false, true, false, true, false, true, false, true, false, 
	    true, true, false, true, false, true, false, true, false, false, 
	    false, true, true, false, false, false, true, false, true, true, 
	    true, true, true, true, true, true, false, true, true, false, 
	    false, true, false, false, true, false, false, true, false, true, 
	    false, true, false, true, false, true, false, false, true, true, 
	    true, true, false, true, true, true, true, false, false, false, 
	    true, true, true, false, false, true, true, true, false, true
	],
	"rows": 25,
	"columns": 4,
	"number_of_nodes": 100,
	"return_graph": true,
	"file_path": "some_file_name.pdf"
}
```

Running a

```print([x for x in nx.__dir__() if x.endswith('_layout')])```

exposes all the possible layouts:

```
[
    'bipartite_layout',
    'circular_layout',
    'kamada_kawai_layout',
    'random_layout',
    'rescale_layout',
    'shell_layout',
    'spring_layout',
    'spectral_layout',
    'planar_layout',
    'fruchterman_reingold_layout',
    'spiral_layout',
    'multipartite_layout'
]
```

Out of the above we first chose *shell_layout* (or circular_layout) as it allows to visualise nodes 
clearly and distinguish them from the edges without the former overlapping with the latter. 
The one problem with this layout is that it will ignore any weights so this is immediately placed in 2nd 
place. 
Then we tried out *random_layout* which creates somewhat more realistic graphs at random uniform distances 
belonging to the interval [0.0, 1.0). This is somewhat better but again, in case edge weights matter, then we lose that info.
So we ended up no using the "pos" option to describe the layout wrapper of the graph.



**Submission:**
Document your thought process and results from Q1 – Q4. Submit your results in a .zip file with both
your implementation and a written report. You will be evaluated based on: a) Correctness, b) Efficiency,
c) Creativity, and d) Documentation. 