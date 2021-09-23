# MiniModeling

We're looking at the modeling of the following loop:
```
for i in 0 to iN:
  for j in 0 to jN:
    a(i,j) = b(i,j)
```

We're going to create an ILP problem whose solution corresponds to the ideal data layout for the arrays a and b. So for this computation, we have 4 decision variables

- d_a_0_1: decision variable for a's layout being 0,1
- d_a_1_0: decision variable for a's layout being 1,0
- d_b_0_1: decision varialbe for b's layout being 0,1
- d_b_1_0: decision variable for b's layout being 1,0

Let's set iN and jN both to 1024.

We also have some coefficients for these decision variables based on access speed:

- coef_0_1: cost per access when layout is 0,1
- coef_1_0: cost per access when layout is 1,0

Our objective function ends up something like (sum of lines):
```
coef_0_1 * iN * jN * d_a_0_1 +
coef_1_0 * iN * jN * d_a_1_0 +
coef_0_1 * iN * jN * d_b_0_1 +
coef_1_0 * iN * jN * d_b_1_0
```

We then have the following constraints.
```
d_a_0_1 + d_a_1_0 == 1
d_b_0_1 + d_b_1_0 == 1
d_a_0_1 >= 0
d_a_1_0 >= 0
d_b_0_1 >= 0
d_b_1_0 >= 0
```

Let's get some values for the coefficients. I'm going to write that code in the file `coefs.cpp`. I originally intended to do total time divided by number of accesses, but there are too many accesses for the division to give decent results, and as long as the same number of accesses are made it should be okay. That gives us
```
coef_0_1 = 20613
coef_1_0 = 65409
```

Now that I've got the problem pretty much set up, its time to get an ILP solver in here. Let's do something in python for the sake of having things work. Its found in `minimodel.py`.

The results give d_a_0_1 = 1 and d_b_0_1 = 1, as expected. 

When we write the problem to a file, it looks like
```
Minimize
OBJ: 21614297088 d_a_0_1 + 68586307584 d_a_1_0 + 21614297088 d_b_0_1
 + 68586307584 d_b_1_0
Subject To
_C1: d_a_0_1 + d_a_1_0 = 1
_C2: d_b_0_1 + d_b_1_0 = 1
_C3: d_a_0_1 >= 0
_C4: d_a_1_0 >= 0
_C5: d_b_0_1 >= 0
_C6: d_b_1_0 >= 0
Bounds
 d_a_0_1 free
 d_a_1_0 free
 d_b_0_1 free
 d_b_1_0 free
End
```

# Take 2: Multiple Loops

Let's see what we can do with a similar situation for a 3 loop situation.
```
for i0 in 0 to N0:
  for i1 in 0 to N1:
    a(i0,i1) = b(i0,i1)

for i1 in 0 to N1:
  for i0 in 0 to N0:
    b(i0,i1) = c(i1,i0)
    
for i1 in 0 to N1:
  for i0 in 0 to N0:
    d(i0, i1) = b(i0,i1)
```

For this example we're saying no conversions. We would expect to have 
- a : 0,1
- b : 1,0
- c : 0,1
- d : 1,0

We need a new decision variable naming scheme. Lets try var_loopnum_layout. So we have
```
a_0_0_1
a_0_1_0
b_0_0_1
b_0_1_0
b_1_0_1
b_1_1_0
c_1_0_1
c_1_1_0
d_2_0_1
d_2_1_0
b_2_0_1
b_2_1_0
```
Since we're not doing conversions, we could actually just use one for each variable, but let's keep in general for when that'll come in handy.

So our objective terms are (omiting the problem size bc thats not currently relevant:
```
coef_0_1 * a_0_0_1
coef_1_0 * a_0_1_0
coef_0_1 * b_0_0_1
coef_1_0 * b_0_1_0
coef_1_0 * b_1_0_1
coef_0_1 * b_1_1_0 
coef_0_1 * c_1_0_1 
coef_1_0 * c_1_1_0
coef_1_0 * d_2_0_1
coef_0_1 * d_2_1_0
coef_1_0 * b_2_0_1
coef_0_1 * b_2_1_0
```
Notice that b_1_0_1 is multiplied by coef_1_0. This is because for the second loop, b's access is not in the same order as the loop nesting. My intuition here is that the coefficient indexing is based on the permutation from the access indices to the nesting indices. I'll want to formalize this later. 

Our constraints are:
```
_C1: a_0_0_1 + a_0_1_0 == 1
_C2: a_0_0_1 >= 0
_C3: a_0_1_0 >= 0
_C4: b_0_0_1 + b_0_1_0 == 1
_C5: b_0_0_1 >= 0
_C6: b_1_0_1 >= 0
_C7: b_0_0_1 == b_1_0_1
_C8: b_0_0_1 == b_2_0_1
_C9: b_0_1_0 == b_1_1_0
_C10: b_0_1_0 == b_2_1_0
_C11: c_1_0_1 + c_1_1_0 == 1
_C12: c_1_0_1 >= 0
_C13: c_1_1_0 >= 0
_C14: d_2_0_1 + d_2_1_0 == 1
_C15: d_2_0_1 >= 0
_C16: d_2_1_0 >= 0
```

I've omitted all the constraints that are between the b_1's and b_2's because those are covered by the equalities. 
Let's try plugging this in. Since I'm writing the .lp file, I'm going to include the coef values as variables and add constraints for their values. 

```
Minimize
coef_0_1 * a_0_0_1 + coef_1_0 * a_0_1_0 + coef_0_1 * b_0_0_1 + coef_1_0 * b_0_1_0 + coef_1_0 * b_1_0_1 + coef_0_1 * b_1_1_0  + coef_0_1 * c_1_0_1  + coef_1_0 * c_1_1_0 + coef_1_0 * d_2_0_1 + coef_0_1 * d_2_1_0 + coef_1_0 * b_2_0_1 + coef_0_1 * b_2_1_0
Subject To
_C1: a_0_0_1 + a_0_1_0 == 1
_C2: a_0_0_1 >= 0
_C3: a_0_1_0 >= 0
_C4: b_0_0_1 + b_0_1_0 == 1
_C5: b_0_0_1 >= 0
_C6: b_1_0_1 >= 0
_C7: b_0_0_1 == b_1_0_1
_C8: b_0_0_1 == b_2_0_1
_C9: b_0_1_0 == b_1_1_0
_C10: b_0_1_0 == b_2_
_C11: c_1_0_1 + c_1_1_0 == 1
_C12: c_1_0_1 >= 0
_C13: c_1_1_0 >= 0
_C14: d_2_0_1 + d_2_1_0 == 1
_C15: d_2_0_1 >= 0
_C16: d_2_1_0 >= 0
_C17: coef_0_1 == 20613
_C18: coef_1_0 == 65409
Bounds
a_0_0_1 free
a_0_1_0 free
b_0_0_1 free
b_0_1_0 free
b_1_0_1 free
b_1_1_0 free
c_1_0_1 free
c_1_1_0 free
d_2_0_1 free
d_2_1_0 free
b_2_0_1 free
b_2_1_0 free
coef_0_1 free
coef_1_0 free
End
```

Turns out the library can't read in the .lp files, so I need to code it by hand.
We get a_0_0_1, b_0_1_0, c_1_0_1, and d_2_1_0, as expected.

# Take 3: Adding in Conversions

Now lets add in conversions. Let's look at the following two loops with a potential conversion.
```
for i0 in 0 to N0:
  for i1 in 0 to N1:
    a(i0,i1) = b(i0,i1)

CONVERT(a)
CONVERT(b)

for i1 in 0 to N1:
  for i0 in 0 to N0:
    a(i0, i1) = b(i0,i1)
```

Our decision variables are:
```
a_0_0_1
a_0_1_0
b_0_0_1
b_0_1_0
a_cin_0_1
a_cin_1_0
a_cout_0_1
a_cout_1_0
b_cin_0_1
b_cin_1_0
b_cout_0_1
b_cout_1_0
a_1_0_1
a_1_1_0
b_1_0_1
b_1_1_0
```
In this list we have our regular layout variables for a and b for the two loops. We also have in and out variables for the conversion steps.

Let's build up our constraints and objective functions bit by bit. Let's start with the basic constraints we already know. I'm omitting the >= 0 ones. 
```
a_0_0_1 + a_0_1_0 == 1
b_0_0_1 + b_0_1_0 == 1
a_1_0_1 + a_1_1_0 == 1
b_1_0_1 + b_1_1_0 == 1
```
These constraints are saying that each array only has one layout in any loop. Now lets add constraints saying that the conversion inputs and outputs must match.
```
#INPUTS
a_0_0_1 == a_cin_0_1
a_0_1_0 == a_cin_1_0
b_0_0_1 == b_cin_0_1
b_0_1_0 == b_cin_1_0
#OUTPUTS
a_1_0_1 == a_cout_0_1
a_1_1_0 == a_cout_1_0
b_1_0_1 == b_cout_0_1
b_1_1_0 == b_cout_1_0
```
Next lets add constraints that say we only have one rconversion input and one conversion output.
```
a_cin_0_1 + a_cin_1_0 == 1
a_cout_0_1 + a_cout_1_0 == 1
b_cin_0_1 + b_cin_1_0 == 1
b_cout_0_1 + b_cout_1_0 == 1
```

Now we need to develop the objective function. Starting with the access costs:
```
a_0_0_1 * coef_0_1
a_0_1_0 * coef_1_0
b_0_0_1 * coef_0_1
b_0_1_0 * coef_1_0
a_1_0_1 * coef_1_0
a_1_1_0 * coef_0_1
b_1_0_1 * coef_1_0
b_1_1_0 * coef_0_1
```
Next we need to add the conversion costs, which require new coefficients. We need to model the different conversions, so lets call it conv_inlayout_to_outlayout. So like:
```
conv_0_1_to_0_1
conv_0_1_to_1_0
conv_1_0_to_0_1
conv_1_0_to_1_0
```
The ones that stay the same have 0 cost. I'll write the code that evaluates the model cost later. Let's write the objective functions stuff first. We only include the cost if the conversion is happening. The conversion is only happening if the in and out far that conversion are true. So the conversion costs look like
```
conv_0_1_to_0_1 * a_cin_0_1 * a_cout_0_1
conv_0_1_to_1_0 * a_cin_0_1 * a_cout_1_0
conv_1_0_to_0_1 * a_cin_1_0 * a_cout_0_1
conv_1_0_to_1_0 * a_cin_1_0 * a_cout_1_0
conv_0_1_to_0_1 * b_cin_0_1 * b_cout_0_1
conv_0_1_to_1_0 * b_cin_0_1 * b_cout_1_0
conv_1_0_to_0_1 * b_cin_1_0 * b_cout_0_1
conv_1_0_to_1_0 * b_cin_1_0 * b_cout_1_0
```

So let's play around with the value of the conversion constants. We know that the "stay the same" conversions don't cost.
Let's see what it does if the other conversions are also free. We should expect a_1_1_0 and b_1_1_0. 

For this playing around, I'm setting the access coefficients to 1 and 3. This means that out of alignment accesses are 3 times more expensive. So, if the conversion cost is 4, we shouldn't see a conversion. 

So this formulation of the variables is a problem bc I think I can't multiply the decision variables together. So let's reformulate this with single variables for the conversions.
Variables:
```
a_0_0_1
a_0_1_0
b_0_0_1
b_0_1_0
a_conv_0_1_to_0_1
a_conv_0_1_to_1_0
a_conv_1_0_to_0_1
a_conv_1_0_to_1_0
b_conv_0_1_to_0_1
b_conv_0_1_to_1_0
b_conv_1_0_to_0_1
b_conv_1_0_to_1_0
a_1_0_1
a_1_1_0
b_1_0_1
b_1_1_0
```
Constraints:
```
a_0_0_1 + a_0_1_0 == 1
b_0_0_1 + b_0_1_0 == 1
a_1_0_1 + a_1_1_0 == 1
b_1_0_1 + b_1_1_0 == 1
a_conv_0_1_to_0_1 + a_conv_0_1_to_1_0 + a_conv_1_0_to_0_1 + a_conv_1_0_to_1_0 == 1
b_conv_0_1_to_0_1 + b_conv_0_1_to_1_0 + b_conv_1_0_to_0_1 + b_conv_1_0_to_1_0 == 1
a_0_0_1 == a_conv_0_1_to_0_1 + a_conv_0_1_to_1_0
a_0_1_0 == a_conv_1_0_to_0_1 + a_conv_1_0_to_1_0
a_1_0_1 == a_conv_0_1_to_0_1 + a_conv_1_0_to_0_1
a_1_1_0 == a_conv_0_1_to_1_0 + a_conv_1_0_to_1_0
b_0_0_1 == b_conv_0_1_to_0_1 + b_conv_0_1_to_1_0
b_0_1_0 == b_conv_1_0_to_0_1 + b_conv_1_0_to_1_0
b_1_0_1 == b_conv_0_1_to_0_1 + b_conv_1_0_to_0_1
b_1_1_0 == b_conv_0_1_to_1_0 + b_conv_1_0_to_1_0
```
Objective Function:
```
a_0_0_1 * coef_0_1
a_0_1_0 * coef_1_0
b_0_0_1 * coef_0_1
b_0_1_0 * coef_1_0
a_1_0_1 * coef_1_0
a_1_1_0 * coef_0_1
b_1_0_1 * coef_1_0
b_1_1_0 * coef_0_1
conv_0_1_to_0_1 * a_conv_0_1_to_0_1
conv_0_1_to_1_0 * a_conv_0_1_to_1_0
conv_1_0_to_0_1 * a_conv_1_0_to_0_1
conv_1_0_to_1_0 * a_conv_1_0_to_1_0
conv_0_1_to_0_1 * b_conv_0_1_to_0_1 
conv_0_1_to_1_0 * b_conv_0_1_to_1_0 
conv_1_0_to_0_1 * b_conv_1_0_to_0_1
conv_1_0_to_1_0 * b_conv_1_0_to_1_0
```

Okay, so when the conversions are free, we get a_0_0_1, a_1_1_0, and the same for b. When the conversions cost 4, we get a_0_0_1 and a_1_0_1, so the conversion is too expensive. What about when the conversion is  3? Still no conversion. What about 2? Interestingly, we get a_0_1_0 and a_1_1_0. so it still does'nt want to do the conversion, but wants us to start with the worse layout.


# Automating the Problem Setup

Now we want to automate the modeling setup. Automating will require some more vigorous definition of terms and stuff for the variable subscripting. Let's see what we can do. 

## Variable names

We have some different types of variables. First, we have the layout variables for the computations, second, we have the layout variables for the conversions. Conversions occur between any adjacent computations. So we number our computations, then we have conversions that basically assume the number of the preceeding computation.

So for computation i and data a with dimensionality n, the variable we introduce is 
a_i_nperm, based on the layout ordering for that variable. For the conversion following this computation, we have the variable conv_a_i_nperm1_to_nperm2.

So a good function for generating these variable names / declarations would take the computation number, the array name, and the dimensionality. It may be worthwhile to create variables for all arrays for all computations, even if the computation does'nt use the arary, because they won't show up in the objective function for the computations that don't use them. 


