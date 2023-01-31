# D3B
Depressive Disorder Data Base

## Workflow
To compose the architecture is needed at least:
* A d3bfed instance up and running
* A d3bagent instange up and running 

The folders **d3bfed/** and **d3bagent/** contain the service
implementation and the **Docker** configuration.

_It is required to first deploy an instance of **d3bagent** and
then several instances of **d3bfed** can be launched._

Once launched the d3bagent a **Registry service**, used by the
d3bfed instances, is build up.

The **d3bfed** `docker-compose.yaml` allows to declare a `D3BFED_NAME`
const used to define the federation's name, in example the **fedX** 
name is used.
Furthermore, the file configures the required services and build them up.



