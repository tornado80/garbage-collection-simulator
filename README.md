# Garbage Collection Simulator

This project is a simple simulation of garbage collection using naive mark-and-sweep method on general linked lists.

## How to use the simulator?
You can access the command line interface with `main.py`. 
There are three main command line arguments that could be passed to the `main.py`.
First one is `-h` or `--help` which brings up the help menu.

Second one is `-i` or `--interactive-shell`. 
With this option you can enter the interactive shell and key in as many commands as you want and see their instant execution result.
It is so much like the Python interactive shell. You can also track exceptions too. 

Third command line option is `-x` or `--execute`. With this option you can execute a file containing the commands of the language.

Note that the latter two options ignite an interpreter which executes your command. This interpreter starts a memory simulation. 
Thus you have to pass the initial memory size with commands `-m X` or `--memory-size=X`.

For example, following commands are valid.
```
python3 main.py -i -m 200
```
which initializes an interpreter with 200 free nodes or 800 cells. Or:
```
python3 main.py -x -m 100 /path/to/file
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
1. `Print Salam`
2. `salam_beto2 = (ABC(D(F))G(H))`
3. `Salam = salam_beto2`
4. `Delete salam_beto2 from (***(**`
5. `Garbage-Collect`
6. `Make Salam Child of salam_beto2 at (***(* With Root`
7. `Make Salam Child of salam_beto2 at (***(* Without Root`
8. `Make (PQ(R(T))S) Child of salam_beto2 at (***(* With Root`
9. `Make (PQ(R(T))S) Child of salam_beto2 at (***(* Without Root`
10. `Set Label of salam_beto2 at (** to K`

More examples are available in unittests written for the project in `tests` directory. 
You can see a sample file containing commands too.
Don't remember to use the interactive shell to play with the simulator.