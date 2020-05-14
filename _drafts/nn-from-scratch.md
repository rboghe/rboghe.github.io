---
layout: single
title:  "Building a neural network from scratch"
header:
  teaser: "unsplash-gallery-image-2-th.jpg"
categories: 
  - Tutorials
tags:
  - edge case
---
### Introduction

Among the exotic buzzwords that are becoming increasingly present in our lives, artificial neural networks is certainly one of the most popular. But what exactly is, a neural network? Simply put, it is computing system capable of finding complex, non-linear relationships between inpunts and outputs, or to spot patterns in data. Let's say we are working for a real estate agency and we want to quickly estimate the price of some new houses based on our previous sales: a neural network can easily help us by inferring their worth using simple parameters such as their height, neighborhood and age. This is commonly called a *regression* problem: estimating the relationships between a continuous dependent variable and one or more independent variables. Another common problem that simple neural networks can solve is *classification*, where we don't predict a continuous value but a class, or label: the species of an animal, the outcome of a match, the positiveness of a test. But this is only the beginning: sofisticated networks are capable of handling images, time series, sounds, texts, probability distributions and much more. However, before going down the rabbit hole, it is important to acquire a solid understanding of the base concepts. For this reason, in this tutorial we'll learn how a simple neural netork works and how we can build one from scratch using Python.

### How it works

The first artificial neural network dates back to 1943, when  the neuroscientist Warren S. McCulloch and the logician Walter Pitts proposed the idea of a perceptron: a single computing neuron capable of solving linear binary classification problems. Its funcioning was relatively simple: given a set of inputs *x<sub>1</sub>, x<sub>2</sub>, ... , x<sub>n</sub>*, and a single output *y*, multiply each input *x<sub>i</sub>* for a weight *w<sub>i</sub>*, normalized in the range (0, 1) or (-1, 1) and sum the results. If you get a positive number output a 1, otherwise a 0. Figure 1 shows a schematic generalization of the perceptron:

![A single neuron](https://github.com/rboghe/rboghe.github.io/blob/master/images/nn/neuron.png)

Where *f* denotes an activation function, which is responsible of determining the output behaviour of a neuron: whether it "fires" a value, or returns 0. In the case of McCulloch-Pitts perceptron, the activation function was limited to outputting a 0, for negative sums, or a 1, for positive sums. Note that in this case we also have a term *b*, along with the set of weights: it is just the constant parameter of the equation, called *bias*. 

Over the years, this concept has evolved and we now use layers of stacked perceptrons to solve a much wider range of linear and non-linear problems. But what about the weights? Can we somehow avoid hardcoding them and let our system figure out their appropriate values? The answer is yes, and that's where the learning part happens. However, let's take a closer look at a simple neural network architecture first:

# IMAGE #

This is called a *sequential* model, as it is a plain stack of layers without forks. The layers are all *fully connected*, which means that each neuron of one layers is connected to all the neurons of the next layer. The network is made up of several layers: an *input layer*, an arbitrary number of *hidden layers*, and an *output layer*. The input layer has the sole purpose of passing the input data to the first hidden layer, and does not have any any weight or activation function. The hidden layers are what makes deep learning "deep": they add extra levels of computations to an otherwise shallow machine learning system. Each hidden layer can have an arbitrary number of neurons and a different activation function. Finally, the output layer is the last level of the network. It has its own activation function, which should be carefully chosen depending on the problem we are trying to solve. 

Now, suppose we have a small network with a single output neuron and random weights and biases, and we feed it with one set of inputs for which we know the target output. The inputs will travel all the way to the end of the network, which in return will toss us his estimated value for the dependent variable. This process is called *feed forward* or *forward propagation*. Given that we just threw some randoms weights into the network, the model will likely return a number that is very far from the expected target. We can easily measure how far, by computing the error, or *loss*, between the expected and actual output. How we calculate this error, is defined by the *loss function* (also called *cost function*) we choose. For a regression problem, an example of loss function might be the mean squared error (MSE): the mean value of the squared difference between a prediction and its respective true value. In the case of a single training sample, it would be just: (y<sub>true</sub> - y<sub>pred</sub>)<sup>2</sup>. At this point, a reasonable goal would be to minimize the error, so that we get our estimation closer to the value we want our network to output. 

To minimize the error, we need to find the global minimum of our loss function. Remember that the derivative of a function tells us how steep the tangent of the function is in each of its points: where the derivative is zero, the tangent of the function is horizontal and we have a minimum, maximum or saddle point. In the case of multivariate functions, the same concept applies to the partial derivatives, where the steepness is referred to the considered variable. For simple problems, we can easily verify each point and check which one is the global minimum. In complex functions however, the amount of points to verify would be potentially infinite, making this approach infeasible. For this reason, we must take a slightly different strategy.


In our case, we are dealing with *vectors*: the weighted sum that we computed inside the output network is a *dot product* between the vector of the inputs *X* from the previous layer and the vector of the weights *W*. Therefore, we have to use a vector of partial derivatives

 be solved by computing the [gradient](https://en.wikipedia.org/wiki/Gradient) of the function with respect to the weights and then moving in the direction of 


using the *gradient descent*. If you don't remember what gradient is, 
