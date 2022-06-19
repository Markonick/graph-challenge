# aifi-challenge

You are given a directed graph that potentially can have tens of thousands of nodes and edges. You can
decide whatever data structure you like for a graph. Any programming language is OK.

**Question 1:
In practice we favor directed graphs without cycles a.k.a. Directed Acyclic Graph. Your first task is to
write a function that decides if a directed graph is acyclic. It is OK to use 3rd party API.
Input: an arbitrary directed graph
Output: the first loop found in the graph or NULL/None


Question 2:
What is the runtime and memory complexity of your implementation? If you use external libraries or
API, please read its documentation and report back the complexity.


Question 3:
Now that you have your cycle detector for an arbitrary directed graph, let us test it! How to
systematically generate 100 graphs of 100 nodes each? How to ensure your test graph has cycles or not?
Write your test app that can systematically generate complex graphs with cycles and graphs without
cycles. Then run your implementation on these test cases to ensure correctness.
Hint: A cycled graph can be derived from Euclidean Minimal Spanning Tree


Question 4:
It is also important to be able to visualize graphs. Display your 100 test graphs in a 25 x 4 grid. Each
graph should be colored red. If the graph has a cycle, mark that subgraph as black. Use your creativity
how to visualize graphs in their most intuitive forms. Please save the graphics as either PDF or PNG file.


Submission:
Document your thought process and results from Q1 – Q4. Submit your results in a .zip file with both
your implementation and a written report. You will be evaluated based on: a) Correctness, b) Efficiency,
c) Creativity, and d) Documentation. 