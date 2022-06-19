# aifi-challenge

You are given a directed graph that potentially can have tens of thousands of nodes and edges. You can
decide whatever data structure you like for a graph. Any programming language is OK.

SETUP
-----
To quickly run the code I decided to use a combination of FastAPI, pytest, Postman and docker-compose.
The main motiovation behind this decision was that 

1. Didn't want to deal with venv (although this would've been just fine)
2. Setting up this logic as a service has the extra advatage of making you think of this
from a users' perspective (eg. plugging in a UI). 
3. This environment to be highly replicable.

For now we used Postman to make any calls to the calculation
endpoints.

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

Question 1:
In practice we favor directed graphs without cycles a.k.a. Directed Acyclic Graph. Your first task is to
write a function that decides if a directed graph is acyclic. It is OK to use 3rd party API.
Input: an arbitrary directed graph
Output: the first loop found in the graph or NULL/None

The choice was to use the popular networkx as it seems to have plenty of the 
functionality required, possibly however at the cost of performance.

To prove that this works we have:
1. Postman to run the saved collection on 

```http://localhost:5000/api/graphs/acyclic```

(Remember that we are exposing the app docker container on port 5000)

The results, depending on the graph beeing acyclic or not will be of the form 

```[bool, cycle | None]```

eg. 
with acyclic:

```
{
    "content": "[true, null]",
    "status_code": "201"
}
```

with cyclic (you can create one from the one above by adding and reversed edge eg. ```[27, 0]```)

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


Question 2:
What is the runtime and memory complexity of your implementation? If you use external libraries or
API, please read its documentation and report back the complexity.


Question 3:
Now that you have your cycle detector for an arbitrary directed graph, let us test it! How to
systematically generate 100 graphs of 100 nodes each? How to ensure your test graph has cycles or not?
Write your test app that can systematically generate complex graphs with cycles and graphs without
cycles. Then run your implementation on these test cases to ensure correctness.
Hint: A cycled graph can be derived from Euclidean Minimal Spanning Tree


Comments: We had to tweak the probabilty of connection to create reasonable graphs (eg. not fully connected)
while considering the time performance and the ability to actually create enough edges to have a reversed one.

Question 4:
It is also important to be able to visualize graphs. Display your 100 test graphs in a 25 x 4 grid. Each
graph should be colored red. If the graph has a cycle, mark that subgraph as black. Use your creativity
how to visualize graphs in their most intuitive forms. Please save the graphics as either PDF or PNG file.


Submission:
Document your thought process and results from Q1 – Q4. Submit your results in a .zip file with both
your implementation and a written report. You will be evaluated based on: a) Correctness, b) Efficiency,
c) Creativity, and d) Documentation. 