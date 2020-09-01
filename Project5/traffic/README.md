# traffic.py - A CNN Traffic Sign Identifier

## What did I try?
**Test 1**
2DConv with 32 3x3 filters and relu activation, 2x2 max-pooling, no dropout layer, and flattening.

**Test 2**
Identical to above, but with 128-unit Dense layer and Dropout with rate of 0.5.

**Test 3**
Try Test 1 again, but realized should be using categorical_crossentropy on compile; not binary_crossentropy.

**Test 4**
Try Test 2 again, but realized should be using categorical_crossentropy on compile; not binary_crossentropy. Makes sense now - dropout layer improves performance.

**Test 5:** 
Try tanh on the output layer (just for fun). Note to self: tanh is best used for classification between 2 categories.

**Test 6:**
Trying Dropout at rate of 0.75 - this may make us less biased? Yes!

**Test 7:**
Trying Dropout at rate of 0.9 - this may make us less biased? Yes!

**Test 8:**
Trying Dropout at rate of 0.99 - Didn't help. Leaving at 0.9.

**Test 9:**
Bringing dropout back to 0.5 - realize that high dropout may be ineffective. https://stats.stackexchange.com/questions/291779/why-accuracy-gradually-increase-then-suddenly-drop-with-dropout
I noticed that although the accuracy improved, the loss was still significant. Now trying (4,4) pool size in first 2DConv layer - seeing reduced loss compared to test 6-8.

**Test 10:**
Testing a second convolutional layer and 2x2 max pooling. Gives less loss.

**Test 11:**
Keep 2nd convolutional layer and its 2x2 max pooling, but remove the 1st 2x2 max pooling. Way better accuracy and minimal loss!!

**Test 12:**
Double the units in the hidden layer. Did not help.

**Test 13:**
Added a 3rd convolutional layer. Less accurate compared to test 11.

**Test 14:**
Added a 4th convolutional layer. Improvement!

**Test 15:**
Added Batch Normalization after each

**Test 16:**
Added 5th convolution layers. 

**Test 17:**
6th layer. Using global max pooling with no flattening now.

**Test 18:**
Try flattening instead of global max pooling. Less performance. 
Test 17 is the best!

## Test Results
**Test 1 (Irrelevant):** 10656/10656 - 1s - loss: 0.0220 - acc: 0.9961
**Test 2 (Irrelevant):** 10656/10656 - 1s - loss: 0.6886 - acc: 0.9552
**Test 3:** 10656/10656 - 1s - loss: 1.0814 - acc: 0.9060  
**Test 4:** 10656/10656 - 1s - loss: 0.7551 - acc: 0.9188  
**Test 5:** 10656/10656 - 1s - loss: 7.5569 - acc: 0.0059 **woah!**  
**Test 6:** 10656/10656 - 1s - loss: 0.5831 - acc: 0.9389  
**Test 7:** 10656/10656 - 1s - loss: 0.5524 - acc: 0.9455  
**Test 8:** 10656/10656 - 1s - loss: 0.7447 - acc: 0.9162  
**Test 9:** 10656/10656 - 1s - loss: 0.5047 - acc: 0.9240  
**Test 10:** 10656/10656 - 1s - loss: 0.4789 - acc: 0.8725  
**Test 11:** 10656/10656 - 1s - loss: 0.1993 - acc: 0.9702  
**Test 12:** 10656/10656 - 1s - loss: 0.2867 - acc: 0.9482  
**Test 13:** 10656/10656 - 1s - loss: 0.2053 - acc: 0.9652  
**Test 14:** 10656/10656 - 1s - loss: 0.1393 - acc: 0.9788  
**Test 15:** 10656/10656 - 2s - loss: 0.0500 - acc: 0.9885  
**Test 16:** 10656/10656 - 2s - loss: 0.0718 - acc: 0.9790  
**Test 17:** 10656/10656 - 2s - loss: 0.0648 - acc: 0.9806  
**Test 17 - Run 2:** 10656/10656 - 2s - loss: 0.0553 - acc: 0.9844 **BEST**  
**Test 18:** 10656/10656 - 2s - loss: 0.0821 - acc: 0.9753  

## What worked well? 
- Adding convolutional layers in pairs, with pooling and batch normalization following

## What didn’t work well?
- Adding too many units to the Conv2D or hidden Dense layers.

## What did you notice?
- Having many 'grouped' units of layers works well. i.e. have a convolution with some pooling and batch normalization, then having another convolution with pooling again, and so on.