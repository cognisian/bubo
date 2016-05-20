Project Bubo
############

Of course Bubo.  Bubo is awesome.

!["Bubo!"][http://www.bigbadtoystore.com/images/products/out/large/GG10138.jpg "Bubo Is Awesome!"]

Investigation of a Neural Network
--------------------------------------

This implementation will incorporate several main areas of investigation:

0) Information Theory
  - information is the representation of change, of probability, of choice
  - if something doesnt change then no need to record it (ie to see if it changed).  If a variable has a 100% percent chance of being a 0, then it aint gonna ever be a 1.
  - so change is good
  - but big change is bad, what is difference between 1234 and 6789.  Was this 5555 (6789 - 1234) hops that I missed or one state change from 1234 to 6789?
  If I change the measurement parameters do I get 1235 (or 6789), change again do I get 1236 (or 6789).  Bayesian.  Rinse lather repeat.
  - given a range of all probabilities, it is the measurement which coaleases the probability into an actual event (1234 or 6789).  Measurement then, is an operator (a function over space of states applied to a state function (space of all possible states) to obtain a new state with some additional info, given the current state.
  - who chooses what measurement?
  - measurement is fixed (ie rods and cones measure different properties of light) or it can be controlled (eye movement/attention)
  - knowledge is built from information, not gleaned (evolution)
1) Brain Structure
  - Neurons grow and move into place.  This is fixed and determined at runtime
  - Neurons are fully connected once initial growth is completed
  - Neuronal placement is in regions dictating form and function of neuron
      Region > Lobe > Area > Column > Row

2) Neuron Structure
  - Neurons have a response
    + inhibitory
    + excitory
  - Neurons have structure
      + unipolar
      + bipolar
      + multipolar
        * golgi I (long axon)
        * golgi II (local axon)
  - Neurons have a size
    + large
    + small
  - Neurons have direction
    + efferent (neuron to external interface)
    + afferrent (external interface to neuron)
    + interneuron (neuron to neuron)
  - Neurons have response type
    + regular (tonic)
    + bursting (phasic)
    + fast spiking
  - Neurons have 2 types of dendrites (to segregate the input)
    + apical
      * distal (remote)
      * proximal (local)
    + basal (local)
  - Neurons can change runtime parameters
    + resting potential (threshold)
    + membrane resistance (work/power)
    + increase peak action potential (response)

3) Runtime
  - Brain/Neuronal structure and initial synapse weights are the result of evolution
  - Once brain is grown, changing synaptic weights and pruning connections is learning in addition to altering the runtime parameters listed above
  - Neurons fire at a frequency, not continuously so has clock frequency and neurons fire at multiples of this rate (ie difference between regular and fast spikes; the difference between peaks is much shorter for fast)
  - The ever changing environment is what puts pressure and rewards (The Brain Virtual Machine BVM) and provides the measuring stick (ie memory mapping; network to buffer for example)
  - BVM executes neurons at VM clock freq, and each neuron is its own virtual machine (The Neuron Virtual Machine NVM)
  - BVM executes 2 loops:
    + outer environment loop (CPU): answer all pending questions from event loop at t0, give event loop its energy budget at t1, update current available energy pool at t2, update global tick at t3, process event loop at t4, back to t0
    + inner event loop (GPU): predict future from model at t0 for t1, sample data at t1, compare expected (t0) with actual (t1) at t2 for reward/failure, update model at t3, back to t0.

4) Success
  - Of course the original standard for the determiniation of artifical intelligence is the Turing test
    + Short comings of this test are known however, it is a good approximation of human intelligence (abstract, iconic, symbolic)
      * Still GOOD though
  - 2 other defining characteristics of human intelligence:
    + tool use (We think with tools)
      * When my AI creates its own AI.  Then it's AIs all the way down.
      * Writes a program to do a calculation (sine or cosine or tanh)
    + social structures
      * When AI joins Facebook
      * When AI builds new social network with only other AIs

Architecture
------------

The human brain is divided into several distinct (from an evolutionary point of view) regions.  These regions can be generally understood as different abstraction levels to the external world (The Brain VM):

### Hindbrain
Will mediate the input interface and integrate any outputs and update the environment as necessary.  This section is fixed and no significant learning (ie runtime parameter optimization) is done, more of overall consequence of environment. SPEED and then PRECISION.

### Midbrain
Midbrain is the router, motivator and the reward center.  Does some significant learning (ie runtime parameter optimization). It is divided into modules (ie protected interface) SPEED and then PRECISION.

### Forebrain
Forebrain is the computational center.  It is divided into lobes (libraries ie public interface), areas (modules ie protected interface), columns (abstract base classes), minicolumns (concrete classes), rows (interface).  

  **Lobes**
  Lobes, as libraries, represent the set of algorithms related to manipulating  input (afferent signal), output (efferent signal) or relations (math sense)
    + Frontal Lobe - Time (prediction) and choice (given prediction choose an action) - Environment (time input signal) and Reward (good/bad output signals) channel
    + Parietal Lobe - Relations/Mappings and sensory integration (input and output specific attributes cross indexed and associated)
    + Temporal Lobe - Memory (storage of relations and indices) and recognition (lookup/recall) and audio processing (input and output signals)
    + Occipital Lobe - Visual processing (input and output signals)

  Lobes are further broken down into areas (and no further for hindbrain and midbrain) where specific tasks related to input/output channels

  **Columns**
  There are about 100M minicolumns total with 50-100 minicolumns to a column, with a minicolumn coontaining about 80-110 neurons with 6 rows.

  **Rows**
  Also refered to as layers

The Brain VM
-------------

The underlying compute architecture is based on CUDA.  We will be using Python for the core development, with the exception of CUDA C code for the kernel functions.  As such we will rely on PyCUDA to provide the Python interface to the CUDA compute architecture.
