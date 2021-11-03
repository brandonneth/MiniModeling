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

## Constraints

Let's enumerate the types of constraints we're applying here
- one_layout_per_computation: each array can only have one layout per computation
- one_conversion_per_conversion: each array can only have one conversion per conversion
- computation_conversion_matching: each array layout for a computation matches the input layout for the following conversion
- conversion_computation_matching: the output layout for an array's conversion matches the layout for the subsequent computation
- nonnegative: all variables are greater than or equal to zero.

What info do we need to generate a one_layout_per_computation constraint? The computation number, the array name, and the dimensionality. The sum of all the generated variables should be 1.

Same for the one_conversion_per_conversion constraints.

Should be the same for computation_conversion_matching. THis one's a little more complicated. For each of the computation layouts, we want to generate the conversion variables that have that input layout. Similar thing for the conversion_computation_matching.

Nonnegative just takes all the names annd creates constraints for greater than 0. That ones easy.

The function that creates all the constraints takes the number of computations and the name dimension pairs like the all name functions. 

## Objective Function

This is the most complicated part because it requires access details. Looking back on the diagram of transformation regarding the data layout and execution policies, we need to determine the relatioonship between the decision variable names, the loop ordering and the accesses.

### A Detour to RAJA
One problem I've discovered about the examples I used above is that they're in C++ pseudocode and not in RAJA pseudocode. Let's take another look at an example to see if that helps the understanding.

Start with the kernel policies:
```
using KPOL_0_1 = KernelPolicy<
  For<0, seq_exec,
    For<1, seq_exec,
      Lambda<0>
    >
  >
>
using KPOL_1_0 = KernelPolicy<
  For<1, seq_exec,
    For<0, seq_exec,
      Lambda<0>
    >
  >
>
```

The numbering on the kernel policies in the example will help us remember the nesting order when we use them. Our loops are over two dimensions, the bounds of which we define next.

```
auto segments = make_tuple(RangeSegment(0,N0), RangeSegment(0,N1));
```

Now we can use the policies and segments.

```
auto kernel1 = kernel<KPOL_0_1>(segments, [=](auto i, auto j) {
  a(i0,i1) = b(i0,i1);
});

auto kernel2 = kernel<KPOL_1_0>(segments, [=](auto i, auto j) {
  a(i0,i1) = b(i0,i1);
});
```

These are the kernels from the third example above. Now lets continue with the analysis of the relationship between the nesting order, the accesses, and the decision variable names.

### Back to the Objective Function

Starting with just the first kernel, we have two accesses, `a(i0,i1)` and `b(i0,i1)`. We haven't chosen a layout for `a` or `b` yet, so we're thinking about these accesses in the "logical" space rather than the "concrete" space. Please take a look at the TransformationDiagram.pdf file for more information on these terms.

When we talk about the access `a(i0,i1)`, we're talking about LogicalAccessArguments, because we're looking at it in terms of the lambda arguments. However, both the kernel policy and the variables are in terms of the AccessIndicies, so we may choose to instead think of the access in those terms, because in our information gathering, we always use the same lambda arguments, so its always `i0, i1, i2, ...`. 

In the current model, the kernel policy is also not variable, so we know what nesting order transformation we're going to have. 

So we have a little more formal of an understanding of the elements we're dealing with. But what exactly are we trying to figure out? Here are the two questions
- What are the coefficients for each decision variable?
- How do we calculate the values of those coefficients?

### Coefficients

Let's take the terms of the objective function we developed for this example and try to understand their meaning more generally. Here are the terms:
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

Starting from the top, we have these two:
```
a_0_0_1 * coef_0_1
a_0_1_0 * coef_1_0
```
What do they represent? In simple terms, the cost of the accesses to `a(i0, i1)` in the first computation when the layout for `a` is either (0,1) or (1,0). Now, from this example, and from the next 2 terms from the access to `b(i0,i1)`, it may seem like we just match the coefficient indexing to the access indexing. The next examples complicate this idea.

For the second loop, we have the terms:
```
a_1_0_1 * coef_1_0
a_1_1_0 * coef_0_1
b_1_0_1 * coef_1_0
b_1_1_0 * coef_0_1
```
Notice that the coefficient indexing and the access indexing do not match here. This is related to the fact that the access index orders do not match the kernel policy order. 

So what's the procedure for selecting the right coefficient? 

We know from the offset the identity LambdaParameters transformation L, the KernelPolicy nesting order transformation for the compututation K, and the LogicalAccessArguments A. We want to find the coefficient for a particular data layout choice D. My claim is that we use the coefficient based on S=D(K(L(A))). Let's explore why.

#### Scoring Review

First, we review what this value S means by way of the example from Report 9.1.2021. Effectively, it is a way to "normalize" an access by stripping out the abstraction of the lambda arguments, the kernel policy nesting, and the data layout. This will let us better compare two different layouts or kernel policies.

For our example, the lambda for the kernel is
```
auto lam = [=](int nm, int d, int g, int z) {
  ... = ... psi(d,g,z);
}
```
the kernel policy is 
```
using KPOL = KernelPolicy<
  For<2, parallel_exec,
    For<1, parallel_exec,
      For<0, parallel_exec,
        For<3, seq_exec,
          Lambda<0>
        >      
      >
    >
  >
>;
```
and the data layout for our data `psi` is 
```
Layout(0,2,1);
```

- The LogicalAccessArguments are `A = (d,g,z)`. 
- The LambdaParameters transformation maps the parameters to their indices: `L = {nm -> 0, d -> 1, g -> 2, z -> 3}`. 
- The KernelPolicy transformation updates the indices to be the equivalent of the "normalized" order: `K = {2 -> 0, 1 -> 1, 0 -> 2, 3 -> 3}`.
- The DataLayout transformation permutes whatever list its given to normalize for the layout ordering. Where the input types/values of LambdaParameters and KernelPolicy matter, DataLayout is a general permutation on any list, reordering the contents without regard for what they are. The first element stays in place, while the second and third elements swap. `D = Permutation(0,2,1)`

So we start with our input `(d,g,z)`. Applying `L` gives `(1,2,3)`. Applying `K` gives `(1,0,3)`. Applying `D` gives `(1,3,0)`. This score means that with the given layout and nesting ordering, these accesses are in some sense equivalent to the accesses in this "normalized" loop nest:
```
for i0:
  for i1:
    for i2:
      for i3:
        a[i1][i3][i0]
```

Lets connect this to the coefficients for our decision variables. 

#### Normalizing Accesses

For our modeling, we want to estimate the cost of different choices of data layout. These costs are estimated using some collection of microbenchmarks. Thus, our objective is to create a set of microbenchmarks AND a mapping from choices to microbenchmarks. 

One possible choice would be to benchmark every possible combination of loop nest orderings, data layouts, and access orderings. Then our mapping from choice to benchmark is simple: pick the benchmark that uses the relevant ordering, layout, and access. The problem here is that this creates lots and lots of benchmarks to run. 

An better choice utilizes the concepts above to set the nesting and data layouts of our benchmarks constant and only change the access order. Then, we map the choice in data layout to the benchmark that is its normalized variant as described above. For the example above, the decision variable `psi_0_0_2_1`, which represents choosing the layout `(0,2,1)`, would have a coefficient determined by the microbenchmark that executes the normalized loop nest we created above. The decision variable `psi_0_0_1_2` which represents a different choice in layout, `(0,1,2)`, would have a different coefficient based on the normalized loop nest it leads to. 

#### Coefficient Naming

This approach of mapping decisions to their equivalent normalized loop nests is my selected approach. So far, we've been using coefficient names based on the access index order within the normalized nest, but this is insufficient. To see why, consider the following two normalized loop nests:
```
for i0:
  for i1:
    a[i0][i1]
for i0:
  for i1:
    for i2:
      a[i0][i1]
```
Both of these nests would be given the name `coef_0_1`. So the coefficient also needs to name its nest depth. These two loops would become `coef_d2_0_1` and `coef_d3_0_1` to denote they are depths 2 and 3, respectively. 

For nesting depth `depth` and array dimensionality `num_dims`, what are the possible coefficient names? All of them will start with "coef_d", followed by the value of `depth` and then an underscore. For the end of the coefficients, we enumerate the possible choices of `num_dims` numbers from 0 to `depth-1`, inclusive, with repetition. This allows for accesses like `a[i0][i0]`.

The function `all_coefficient_names` in `automating.py` generates all possible coefficient names for given maximum depth and dimensionality.

#### Coefficient Values

For each coefficient, we need the function that evaluates its value.
The structure of the function should be something like:
```
template <typename VIEW>
void coefficient_evaluation_d{NESTING_DEPTH}_{ACCESS_ORDER} (VIEW a, {BOUNDS_DECLARATIONS}) {
  auto start = std::clock();
  {FOR_LOOP_NESTING_START}
  a({ACCESS_ARGUMENTS})= 0;
  {FOR_LOOP_NESTING_STOP}
  auto stop = std::clock();
  auto t = stop - start;
  std::cout << "coef_d{NESTING_DEPTH}_{ACCESS_ORDER} = " << t << std::endl ; 
}
```
The invocation will look something like:
```
double * _a_d{NESTING_DEPTH}_{ACCESS_ORDER} = new double [{SIZE
_COMPUTATION}];
VIEW{NUMDIMS} a_d{NESTING_DEPTH}_{ACCESS_ORDER} (_a_d{NESTING_DEPTH}_{ACCESS_ORDER}, {DIM_SIZES});

coefficient_evaluation_d{NESTING_DEPTH}_{ACCESS_ORDER}(a_d{NESTING_DEPTH}_{ACCESS_ORDER}, {NEST_SIZES})

free(_a_d{NESTING_DEPTH}_{ACCESS_ORDER})
```

Functions to automate the generation of both of these things are found in automating.py, as well as one to generate the whole .cpp file.

THis is only for the ocmputation coefficients.

### Objective Function Computation Terms

Now that we can evaluate the coefficients and map our decision variables to those coefficients, we're ready to start building up our objective function.

Lets break them into computation terms and conversion terms. We are yet to dive into the conversion coefficients, so lets just put those aside for now.

We're handed, for each computation, a kernel policy nesting order and some number of accesses which each contain the arguments used to access the view and the identifier for the view. It also gives us the layout in use but we're choosing ourselves so we can disregard that for now.

For each access, start by calculating the partial score by applying the identity LambdaParameter function and then the reordering defined by the computation's kernel policy. Call this partial score S. 

Next, for each of the decision variables V for that view in that computation, extract the data layout permutation D. Apply D to S. Call the result T. Let n be the depth of the computation's nest. The coefficient for V is `coef_d$n_$T`.

Sum the terms generated this way for all accesses in the entire program. That is the computation component of the objective function. 

### Objective Function Conversion Terms

We return now to the conversion portion of the objective function. The set of conversion coefficients is based on the product of permutations of each size. Conversion decision variables are mapped to coefficients directly by matching their layout inputs and outputs. 

Evaluating the conversion coefficients is more complicated. It could be as easy as just evaluating the naive copy, as if it were juts any other function. But this would not be performance optimal. Instead, it may be that we try all possible execution policies for each and then pick the best policy. Alternatively, there may be existing capabilities, hardware or otherwise, for re-laying out the data in memory. For example, Tom mentioned something about GPU transfers doing it. 

So this creates a sort of multistep process. First, for each of the possible conversions, we figure out the best layout. Then, we use that cost as the coeficcient for the objective function. So we need a function that generates the function for the conversion call.

Its going to be similar to the computation functions. But instead, we'll have two view arguments for the function. These views will have the same normalized layout because we've normalized out the layout and the nesting order. 

So really this is boiling down to a similar kind of problem where instead of determining the best data layout for a fixed access order and nesting order, we want to determine the best nesting order for a fixed access order and data layout. So lets start our generating functions there. We have the input data layout and the output data layout. These are different from the access order. Lets start even lower with an example. We want to calculate the coefficient `conv_0_1_2_to_2_1_0`, which is the conversion coefficient for changing from the normal layout to the reverse of the normal layout `(0,1,2) to (2,1,0). One loop nest that does this conversion is:
```
for i0:
  for i1:
    for i2:
      out(i2,i1,i0) = in(i0,i1,i2)
```
Note that here, both arrays have the same layout permuttaion (identity), even though they have different layouts.

So for each of the permutations of the loop nests, ie, each of the possible nesting orders, we have the body `out({OUTLAYOUT}) = in({INLAYOUT})`.

It does need to be said here that the conversion loops need not use only the first n dimensions. It could be a view with dimension N2xN3xN5 or something. I think a potential here would be to just have the extents be global variables. I'm going to do this. 

I Also don't think its strictly necessary that I go back and update the other functions since i can pass teh global values as parameters. 

Anyway, on to the invocation of the function. With the layouts and nesting order defined, I need to allocate the memory for the two arrays, create the two views, call the function, and free the memory. 

Back to the topic of the N2xN3xN5 thing, thats actually not a problem bc its equivalent to having it be N0 N1 N2 and different values for the Ns. 

## Back to the Objective Function

So now that we've got the coefficient values and the constraints, lets create the objcetive function once and for all. But we still need to bring in the code for the kernel, layout, and lambda transformations. Let's also break out the coefficient calculation code from the constraint generation code. So we're going to break up the files.

Next we're going to add in the access analysis code, which is going to give us the tools for applying the kernel policies and stuff. I'm going to add in a function that gives us the normalized access by applying the lambda, the kernel policy, and the data layout. 

I need a taste of what the model data function outputs. Let's check that out for the following kernel
```
using KPOL = KernelPolicy<
  statement::For<0, loop_exec,
    statement::For<1>, loop_exec,
      statement::For<2>, loop_exec,
        statement::Lambda<0>
    >
  >
>;

auto knl1 = make_kernel<KPOL>(make_tuple(RangeSegment(0,N0), RangeSegment(0,N1)), [=] (auto i, auto j, auto k) {
  a(i,k) += b(i,j) * c(j,k);
});

knl1.model_data();
```
Here's the output:
```
{
 "NestingOrder" : [0,1,2],
"LambdaParameters" : [0,1,2],
"AccessArguments" : [[0x2000019a0010,i1,i2],[0x200000980010,i0,i2],[0x200001190010,i0,i1],[0x2000019a0010,i1,i2],[0x200001190010,i0,i1],[0x200000980010,i0,i2]],
"DataLayouts" : {
0x200000980010: [0,1],
0x200001190010: [0,1],
0x2000019a0010: [0,1]}}
```
Let's clean this up
```
{
  "NestingOrder" : [0,1,2],
  "LambdaParameters" : [0,1,2],
  "AccessArguments" : [[0x2000019a0010,i1,i2],[0x200000980010,i0,i2],[0x200001190010,i0,i1],[0x2000019a0010,i1,i2],[0x200001190010,i0,i1],[0x200000980010,i0,i2]],
  "DataLayouts" : {
    0x200000980010: [0,1],
    0x200001190010: [0,1],
    0x2000019a0010: [0,1]
  }
}
```
The LambdaParameters aren't quite right, bceause they need the i. Also, the view names are a mess, so maybe we use the mapping function that we've got as well here. Furthermore, it looks like we're seeing duplicates in the accesses. I think I've fixed this problem elsewhere? 
Now we get 
```
{
 "NestingOrder" : [0,1,2],
"LambdaParameters" : [i0,i1,i2],
"AccessArguments" : [["arr0",i1,i2],["arr1",i0,i2],["arr2",i0,i1]],
"DataLayouts" : {
"arr0": [0,1],
"arr1": [0,1],
"arr2": [0,1]}}
```

# Demo

We'll be demonstrating the process using the code in demo_comp.cpp, which is a matrix multiply with the nesting order (2,0,1). We start by compiling and running the demo_comp, which prints the access data.
```
clang++ -I $HOME/libs/include/RAJA -std=c++17 -fopenmp -o demo_comp.exe demo_comp.cpp $HOME/libs/lib/libRAJA.a
./demo_comp.exe > demo_comp.info
cat demo_comp.info
python3 demo_comp.py

clang++ -I $HOME/libs/include/RAJA -std=c++17 -fopenmp -o coef_eval_demo_comp.exe coef_eval_demo_comp.cpp $HOME/libs/lib/libRAJA.a
./coef_eval_demo_comp.exe > demo_comp.coefs



```

Based on the output, we have `arr1(i0,i2) += arr2(i0, i1) * arr0(i1, i2)`

For nesting order (2,0,1), arr1_0_0_1 should be matched to the coefficient (1,0).
arr2_0_0_1 should be coefficient for (1,2) and arr2_0_1_0 should be (2,1).
arr0_0_0_1 should be (2,0) and arr0_0_1_0 should be (0,2). This is what comes out.






# 10.28.2021

Now working on the creation of the interface for automatic layout manipulation for the user. The basic use looks like
```
auto computation = manipulate_layouts(knl1, knl2, knl3);
```
The execution function should be straightforward, just execute knl1, then conversion, then knl2, then conversion, then knl3.

The hard part is figuring out what the conversion should be when constructing the computation. Let's run with an example to make this more concrete, as usual. 

```
using KPOL = KernelPolicy<
  statement::For<0, loop_exec,
    statement::For<1, loop_exec,
      statement::For<2, loop_exec,
        Lambda<0>
      >
    >
  >
>;

VIEW2 a(_a, N, N);
VIEW2 b(_b, N, N);
VIEW2 c(_c, N, N);
VIEW2 d(_d, N, N);
VIEW2 e(_e, N, N);

auto lambda1 = [=](auto i0, auto i1, auto i2) {
  c(i0,i2) += a(i0,i1) * b(i1, i2);
};

auto lambda2 = [=](auto i0, auto i1, auto i2) {
  e(i1,i0) += d(i0,i2) * c(i2,i0);
};

auto iterspace = make_tuple(RangeSegment(0,N), RangeSegment(0,N), RangeSegment(0,N));

auto knl1 = make_kernel<KPOL>(iterspace, lambda1);

auto knl2 = make_kernel<KPOL>(iterspace, lambda2);

auto computation = manipulate_layout(knl1, knl2);

computation();

```

So in this situation, we'd generally expect `c` to get a new layout. So what form does all the stuff take? 
Important to note here that the structure of the final kernel thing needs to be teh same each time. So when passing in 2 kernels to `manipulate`, the same number of kernels needs to be in the outputted sequence. This indicates that we'll have to do all the conversions in a single kernel between each computation. So if we were manipulating both c and d, we would need to do both simultaneously. Furthermore, the kernel that we generate needs to be the same dimensionality each time, regardless of the dimension of the arrays we're manipulating. Thus, we'll probably want a forall that does a single iteration that makes a call to a function that does the transformation or transformations. Alternatively, we could have the user pass in the views they want considered for transformation as part of the function call. So for example, manipulate_layouts would be like
```
auto computation = manipulate_layouts(make_tuple(a,b,c,d,e), knl1, knl2);
```
This says they want us to consider all the views for possible layout changes. I think this method is probably more feasible, so we'll go with it now.

```
auto manipulate_layouts(auto views_to_consider, auto knl1, auto knl2) {

  auto permutations = modelling_magic(views_to_consider, knl1, knl2);

  auto conversion_knls = permute_views(views_to_consider, permutations);

  auto all_kernels = tuple_cat(make_tuple(knl1), conversion_knls, make_tuple(knl2));
  return chain(all_kernels);
}
```

I'll leave the modelling magic for later. One thing I think I can tackle now is the permute_views. Or i guess, permute_view. Regardless of whether they are passed into the function or extracted from the view being changed or calculated using the other two pieces, we'll need to have 3 pieces of information: the current layout, the permutation to apply, and the final layout. WAIT. I can do it with just the output layout. The performance might suffer, but the conversion function is just:
```
auto permute_view(VIEW2 v, Layout2 l) {

  auto converter = [=](auto unused) {
    VIEW2 v2(...,l);
    kernel<POL2D>(v.get_bounds(), [=](auto i, auto j) {
      v2(i,j) = v(i,j);
    });
    auto tofree = v.get_data();
    v.set_data(v2.get_data());
    v.set_layout(l);
    free(tofree);
  }

  return converter;
}
```
And we'd call it with rangesegment of 0 to 1. 

Then permute_views looks something like
```
template <typename... ViewTypes, typename... LayoutTypes, camp::idx_t...Is>
auto permute_views(camp::tuple<ViewTypes...> views, camp::tuple<LayoutTypes...> layouts, camp::idx_seq<Is...>) {
  return make_tuple(permute_view(camp::get<Is>(views), camp::get<Is>(layouts))...);
}

template <typename... ViewTypes, typename... LayoutTypes>
auto permute_views(camp::tuple<ViewTypes...> views, camp::tuple<LayoutTypes...> layouts) {
  auto seq = idx_seq_for<ViewTypes...>{};
  return permute_views(views, layouts, seq);
}
```

# 11.3.2021

Thinking about the evaluation portion now. Given a computation, we need a way of generating the different possible implementations of that computation and timing them. 

The procedure for a first pass at evaluation would look like this.

Assumptions:
- 2 kernels only with one conversion stage

Procedure:
1. (User) Specify the two kernels and which Views to consider changing
2. (User) Pass those to function which generates the different possible implementations and names those implementations using a standard schema
3. (User) Specify kernels and views to modeling tool 
4. (User) Implement model-selected variant
5. Compare performance of model-selected variant against the ordered series of all possible implementations 





