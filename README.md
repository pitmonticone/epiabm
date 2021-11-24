
## General Information

This programme implements a SEIR based model with added spatial complexity. It immitates the Imperial CovidSim model, but aims to simplify and.

The model contains two main sections: transmission mechanisms and within host progression.

For each timestep the code loops through the population and records interations between infected and susceptible people which may lead to infections. Individuals are allocated a susceptibility based on age and location data and pairs of individuals considered to see whether their interaction leads to infection. The likelihood of a pair interacting is weighted by spatial distance and age factors (as people are more likely to socialise with those of the same age, and children maintain close contact with parents). This incorporates the major spatial variation within the model.
 
Once an individual becomes exposed, their progression through the various stages of infection is determined by generating a series of random timesteps to mark their movements between infection categories. The possible paths an individual can take are indicated on the schema below.

![SEIR model conceptualisation](./images/covidsim_schema.png)

## pyEpiabm
Python is more readable and user-friendly, but is not able to cope with large population sizes 


## cppEpiabm
C++ is far more computationally efficient and so can run simulations for populations comparable to the UK in a reasonable timeframe. 
This code may be superficially less readable, but the parallels with the python code should be sufficiently informative for users who wish to look deeper into the code.

## Set up

Add text on how to install and use module. 

&nbsp;


## Documentation 
Some documentation on the program's classes and methods can be found here: https://epiamb.readthedocs.io/en/latest/

### References
List of ressources that can be useful for the project:
* Ferguson N, 2020. Impact  of  non-pharmaceutical  interventions (NPIs) to reduce COVID-19 mortality and healthcare demand (https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-NPI-modelling-16-03-2020.pdf)
* Gillespie D, 1977. Exact stochastic simulation of coupled chemical reactions (https://doi.org/10.1021/j100540a008)
* Erban R, Chapman J and Maini P, 2007. A practical guide to stochastic simulations of reaction-diffusion processes (https://arxiv.org/abs/0704.1908)
* Bauer F, 2008. Compartmental models in epidemiology (https://link.springer.com/chapter/10.1007/978-3-540-78911-6_2).

