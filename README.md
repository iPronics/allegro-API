# allegro-API

Mock API for Allegro project 


## Installation

It is recommended to use a python virtual environment (e.g. using conda).

Python >=3.11 is required

```
pip install <GIT_REPO_CLONE_OR_RELEASE_FILE>
```

## Example of usage

```python
# Instantiate Allegro and connect subsystems.
a = Allegro()
a.connect()
print(f"{a.connected=}")

# Set PUC 2 to bar state and PUC 5 to cross state. PUC 2 phase is also set to pi.
a.set_puc_states({2: PUCState(k=0.0, phase=3.14), 5: PUCState(k=1.0)})

# Reset mesh state and set all PUCs to bar state.
a.reset()
all_puc_ids = a.get_puc_states().keys()
a.set_puc_states({i: PUCState(k=0.0) for i in all_puc_ids})

# Split the signal from port 2 into ports 17 and 19. Mesh is automatically reset.
# Print the output power from ports 17 and 19
states = a.beamsplitter(inport=2, outports=[17, 19])
print(f"{states=}")
print(f"{a.get_output_power([17, 19])=}")

# Try to set an additional interconnect without resetting the mesh.
# Check if it is compatible and rollback to previous state if
# it is not.
new_states = a.interconnect(inport=25, outport=29, reset=False)
print(f"{new_states=}")

incompatible = bool(set(states).intersection(new_states))
if incompatible:
    print("Resetting")
    a.reset()
    a.set_puc_states(states)

# Disconnect subsystems
a.disconnect()
```
