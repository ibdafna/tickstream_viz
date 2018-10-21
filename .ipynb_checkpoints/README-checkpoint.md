# tickstream_viz
### Local tick streaming visualisation solution for Jupyter Notebooks

Generally speaking, tick streaming visualisation solutions have been always offered by third parties as a hosted solution on their servers. Plotly used to offer this as a part of their normal API, which required users to create an account, generate API keys and repackage the tick data into a format Plotly's servers can read. This solution has now been migrated to their Dash offering, requiring users to learn Dash and set up an entire dashboard server - locally or hosted, just for this service.

__tickstream_viz__ is a *proof of concept* solution. It is not aimed at replacing services like Dash. Instead, what I try to solve for here is providing a quick and simple soultion for visual tick streaming which does not depend on external service providers. 

The solution is self contained and is 'plug and play' - just instantiate the class and invoke the 'run' method. It is also multithreaded, allowing you to continue working whilst the visualisation running in the notebook. This particularly useful when leveraging Jupyter Lab with the Sidecar add-in. 

You get three calculated lines: the asset price, SMA1 (5 ticks), SMA2 (10 ticks). The asset price evolution follows an Euler discretization scheme of a Geometric Brownian Motion (S0=100, sigma=0.4 and r=0.05).

There are a few main dependencies we rely on here:

1. bqplot for the graph objects (all rendering is done in the front end)
2. zeromq for both the server and client interfaces
3. numpy/pandas for the data aggregation and manipulation

TODO:

* Properly package this
* Better separation of concerns (MVC)
* Improve the server so it accepts parameters for S0, r and sigma
* Allow for custom functions instead of SMA
* Add a GUI with controls
* Multiple streams


![tickstream_viz](tickstream_viz.PNG)


