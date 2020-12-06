# Garbage Collection Simulator

This project is a simple simulation of garbage collection using naive mark-and-sweep method on general linked lists.

## How to use the simulator?
You can access the command line interface with `main.py`. 
There are three main command line arguments that could be passed to the `main.py`.
First one is `-h` or `--help` which brings up the help menu.

Second one is `-i` or `--interactive-shell`. 
With this option you can enter the interactive shell and key in as many commands as you want and see their instant execution result.
It is so much like the Python native interactive shell. You can also track exceptions too. 

Third command line option is `-x` or `--execute`. With this option you can execute a file containing the commands of the language.

Note that the latter two options ignite an interpreter which executes your command. This interpreter starts a memory simulation. 
Thus you have to pass the initial memory size with commands `-m X` or `--memory-size=X`.

For example, following commands are valid.
```
python3 main.py -i -m 200
```
which initializes an interpreter with 200 free nodes or 800 cells. Or:
```
python3 main.py -x -m 100 tests/sample.txt
```

## Definitions
* `$NODE_EXPRESSION`: A string containing only `*` and `(` which represents each node in general list uniquely.
* `$NODE_LABEL`: A single character string with ascii number from 33 to 126 inclusive.
* `$VAR_NAME`: A variable containing underscores, digits (except at the beginning), capital and small letter.
* `$LIST_EXPRESSION`: General list representation using parentheses and single character labels

## Which commands are supported?
1. `$VAR_NAME = $VAR_NAME` (Left hand side variable will point to the right hand side variable)
2. `$VAR_NAME = $LIST_EXPRESSION`
3. `Print $VAR_NAME`
4. `Garbage-Collect` (non recursive without stack implementation)
5. `Make $VAR_NAME Child of $VAR_NAME at $NODE_EXPRESSION With Root` (enclosed with parentheses)
6. `Make $VAR_NAME Child of $VAR_NAME at $NODE_EXPRESSION Without Root` (normal make child, not enclosed with parentheses)
7. `Make $LIST_EXPRESSION Child of $VAR_NAME at $NODE_EXPRESSION With Root` (enclosed with parentheses)
8. `Make $LIST_EXPRESSION Child of $VAR_NAME at $NODE_EXPRESSION Without Root` (normal make child, not enclosed with parentheses)
9. `Delete $VAR_NAME from $NODE_EXPRESSION`
10. `Set Label of $VAR_NAME at $NODE_EXPRESSION to $NODE_LABEL` (Sets the label of mentioned node to a new single character label)

## Notes
1. You can use the command `Make ... Child of ...` for a node which has down pointer. In this case those nodes will be garbage and could be swept by calling `Garbage-Collect`. 
2. You can use the command `Make ... Child of ...` for a inline list not especially a variable.
3. Garbage collector function prints the traversed lists, which are marked as not garbage, so you can track the garbage nodes easily.
## Examples
Numbers are corresponding to commands cited above:
1. `Salam = salam_beto2`
2. `salam_beto2 = (ABC(D(F))G(H))`
3. `Print Salam`
4. `Garbage-Collect`
5. `Make Salam Child of salam_beto2 at (***(* With Root`
6. `Make Salam Child of salam_beto2 at (***(* Without Root`
7. `Make (PQ(R(T))S) Child of salam_beto2 at (***(* With Root`
8. `Make (PQ(R(T))S) Child of salam_beto2 at (***(* Without Root`
9. `Delete salam_beto2 from (***(**`
10. `Set Label of salam_beto2 at (** to K`

More examples are available in unittests written for the project in `tests` directory. 
You can see a sample file called `sample.txt` containing commands too.
Don't remember to use the interactive shell to play with the simulator.

## Implementation
Memory cells are grouped four by four such that each group represents a node. Thus nodes have 4 fields:
1. Next: An integer is used to store the next node address.
2. Down: An integer is used to store the down node address.
3. Tag: A boolean (True or False) which is only used in garbage collection to mark traversed lists nodes and then sweep the garbage nodes.
4. Label: It is the value stored in the node and could be anything but mostly for beautiful printing a single character.
Label is valuable for nodes which don't have children. For other nodes (those who have children), we use it in garbage collection to store father's node address.
In cases in which the node does not have a father, we use it for storing address of the next node:
For example, in situation below, after reversing pointers in garbage collection we miss the next value of `B`, so we store address of `D` int the label of node `B`. 
```
A -> B -> D                                A <- B   D
     |          in Garbage Collection:          |
     C                                          C
```
Otherwise we use label to store the father node address: For example, here we change the label of node `B` to point to node `A`. (This is called a ladder of nodes in code)
```
A -> ...
|
B -> ...
|
C -> ...
```
It is note worthy to say that in this implementation we don't change `down` fields except in cases like node `C` for which `label` is valuable and only its `down` field could be used. (For node `C` we set the down field to `B` thus a loop is created and we can detect this loop when traversing backward in list. This pointer helps us to find the father node too).

Also in our implementation for general lists we create a root node which its down field points to the first node of list. In such way most actions in printing, node expression, and list expression analysis are automated without handling the beginning open parenthesis (`(`) or trailing close parenthesis (`)`). 
For example a list like `(A(D)B)` is stored as:
```
root
|
A -> X -> B
     |
     D
```
