---
layout: single
title:  "Building a neural network from scratch"
header:
  teaser: "unsplash-gallery-image-2-th.jpg"
categories: 
  - Jekyll
tags:
  - edge case
---
### Introduction

Among the exotic buzzwords that are becoming increasingly present in our lives, artificial neural networks is certainly one of the most popular. But what exactly is, a neural network? Simply put, it is computing system capable of finding complex, non-linear relationships between inpunts and outputs, or to spot patterns in data. Let's say we are working for a real estate agency and we want to quickly estimate the price of some new houses based on our previous sales: a neural network can easily help us by inferring their worth using simple parameters such as their height, neighborhood and age. This is commonly called a *regression* problem: estimating the relationships between a continuous dependent variable and one or more independent variables. Another common problem that simple neural networks can solve is *classification*, where we don't predict a continuous value but a class, or label: the species of an animal, the outcome of a match, the positiveness of a test. But this is only the beginning: sofisticated networks are capable of handling images, time series, sounds, texts, probability distributions and much more. However, before going down the rabbit hole, it is important to acquire a solid understanding of the base concepts. For this reason, in this tutorial we'll learn how a simple neural netork works and how we can build one from scratch using Python.

### How it works

The first artificial neural network dates back to 1943, when  the neuroscientist Warren S. McCulloch and the logician Walter Pitts proposed the idea of a perceptron: a single computing neuron capable of solving linear binary classification problems. Its funcioning was relatively simple: given a set of inputs *x<sub>1</sub>, x<sub>2</sub>, ... , x<sub>n</sub>*, and a single output *y*, multiply each input *x<sub>i</sub>* for a weight *w<sub>i</sub>*, normalized in the range (0, 1) or (-1, 1) and sum the results. If you get a positive number output a 1, otherwise a 0. Figure 1 shows a schematic generalization of the perceptron:

![A single neuron](https://github.com/rboghe/rboghe.github.io/blob/master/images/nn/neuron.png){:height="50%" width="50%"}

Where *f* denotes an activation function, which is responsible of determining the output behaviour of a neuron: whether it "fires" a value, or returns 0. In the case of McCulloch-Pitts perceptron, the activation function was limited to outputting a 0, for negative sums, or a 1, for positive sums.

Over the years, this concept has evolved and we now use layers of stacked perceptrons to solve a much wider range of linear and non-linear problems. But what about the weights? Can we somehow avoid hardcoding them and let our system figure out their appropriate values? The answer is yes, and that's where the learning part happens. Let's take a closer look at a simple neural network architecture:
