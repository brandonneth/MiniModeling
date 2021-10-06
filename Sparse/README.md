This directory is going to do the same sort of modeling thing but for a sparse computation. With the dense stuff, I started with a single kernel, then did multiple kernels, then did conversions. I'll do the same here. The goal is to build to the computation that Wei used for her modeling work too. 

# 


# Single Kernel


Let's start with the inspector kernel for the dependences in the computation, which solves the equation Au=f without any parallelism or anything. A is lower triangular and f is a dense vector/forcing function. We're solving for u. Here is the CSR implementation, and I'm going to walk through an example on a whiteboard before deriving myself the CSC implementation. 

CSR:
```
for (i = 1; i < N; ++i)
    for (k = rowptr[i]; k < rowptr[i+1]-1; ++k)
        if (i > col[k])
            //insert (col[k], i) into dep_rel
```
Here's the A I'm rolling with on the whiteboard:
```
2 0 0 0 0
1 1 0 0 0
0 2 1 0 0
1 0 0 3 0
4 0 2 0 1
```
and the f:
```
10
12
3
8
24
```

From my work on the whiteboard, I derived the following code for the inspector using CSC:
```
for(i = 0; i < N; i++) {
    for (k = colptr[i]+1; k < colptr[i+1]; k++) {
        dep_rel.insert(i, row[k]);
    }
}
```
For the two implementations, the order that things are inserted is:
CSR:
```
(0,1)
(1,2)
(0,3)
(0,4)
(2,4)
```
CSC:
```
(0,1)
(0,3)
(0,4)
(1,2)
(2,4)
```

So we see that with CSR, the insert happen in monotonically increasing order for the second dimension, while for CSC it happens monotonically increasing for the first dimension. If we change the ordering of the dependence structure, we change which dimension the monotonically increasing order happens. 

One thing I don't get about the CSR implementation is why thereas a check for the column value being less than i. That is a feature that's encoded in the fact that we're working with a lower triangular matrix. So let me edit the CSR implementation to be:
```
for (i = 1; i < N; ++i) {
    for (k = rowptr[i]; k < rowptr[i+1]-1; ++k) {
        dep_rel.insert((col[k], i), 1);
    }
}
```

Furthermore, just like how the CSR implementation starts at i=1 bc the first row can only have 1 thing it due to triangularity, a similar feature is true of the last column in the CSC impleementation, so we can amend that implementation to:
```
for(i = 0; i < N-1; i++) {
    for (k = colptr[i]+1; k < colptr[i+1]; k++) {
        dep_rel.insert((i, row[k]), 1);
    }
}
```

There are a whole bunch of structural similarities between these two implementations. Almost like there's a symmetry of sorts across the "rotation" from CSR to CSC. We see the bounds for `i` reflected across the interval 0 to N. We see the bounds for `k` flip around in a similar way from rowptr to colptr, and we see the order of the inserted elements flipped as well. 

These implementation complexities are sort of scary from an automation perspective, so I'm going to pretend that's not something I have to deal with and instead assume I have the implementations handed to me already. 

For both implementations, the accesses to the compressed dimension and the uncompressed dimension both are monotonically increasing. We're actually doing stride 1 accessing through both arrays, so there's no performance difference to be found as far as I can tell. As Wei's experiment would imply, we see that the layout of the dep_rel array is the importance piece here. 

I guess lets try to come up with some modeling stuff at this point, bc I don't know how else to proceed.
- A_csr
- A_csc
- dep_rel_csr
- dep_rel_csc
Lets say that no matter what, for each insertion, its dep_rel.insert((src,tgt), 1). So we'd expect A_csr to match with dep_rel_csc and A_csc to match with dep_rel_csr. To be fair, I don't even really understand how the "insert" function would be implemented at all. 

To better understand how the insert works, I'm going to walk through the same example where the inserts are in the good order and build up the dependence relation array on the side.

So the ordered insert does something like this:
```
ordered_insert(new_row, new_col, new_val) {
    
    if (new_row == len(rowptr) - 1) {
        do_nothing()
    } else {
        rowptr.push(len(cols));
    }
    cols.push(new_col);
    vals.push(new_val);
}
```
We can just append the column value and the actual array value being inserted, and extend the rowptr only when the thing being inserted has a new row value. The cost of one insert is then pretty low, with 3 amortized constant inserts. So overall this is an O(1) operation, and we could try to estimate that constant if we wanted to but I don't.

What about the random insert? Let's build up the insertion with the bad order. So this one has 2 things that I think are potentially expensive.
1. Figuring out where in the col array the value needs to go and inserting the value there
2. Updating rowptr

Let's break these down. To figure out what the index of the value will be after being inserted, we need to do something like:
```
col_index(new_row, new_col, new_val) {
    if (new_row >= len(rowptr)) { // we haven't put something in with this high a row number yet
        return len(cols);
    } else {
        start_of_row_index = rowptr[new_row];
        end_of_row_index = row_ptr[new_row+1];
        insert_index = -1;
        for(i = start_of_row_index; i < end_of_row_index; i++) {
            if (new_col > cols[i]) {
                insert_index = i+1;
            }
        }
        return insert_index;
    }
}
```
This is assuming that each element of the array only is written once. Next we need to do the insert, which for a fixed size array, since we're not inserting at the end, is O(len(array)), so O(nnz). 

Last we have to update the rowptr, which involves "+= 1"ing the indices of rowptr greater than the row_index, which is O(len(rowptr)), which is O(N).


So we have O(nnz) + O(nnz) + O(N) for the random insert. How does this compare to Wei's evaluation?

Wei says that the random insert is #dep * #dep, which in this case is the same as nnz (each dependence is 1 nonzero), and we do #dep inserts, so I agree.

So what about the other kernels? Let's look at the next kernel, which consumes the dependence relation to create the wavefront relation. 

## Kernel 2: Wavefront Relation

This kernel is being done as a sparse thing for some reason and honestly I don't get it. But let's roll with it, and start with CSR  wave_rel being ordered (wavefront, iteration).
So we start with wave_rel as:
```
rowptr: 0         5 5 5 5 
   col: 0 1 2 3 4
   val: 0 0 0 0 0  
```
I'm spacing out the rowptr to show the matrix more clearly. Also, I'm going to have the val array match the wavefront rather than just being 1. This is why I don't understand why we don't just use a 1D array or something, since iteration values are dense. Anyway, let's process (0,1). We see that their wavefront values are both 0, so we need to remove and reinsert the (1,1) value. After removal:
```
rowptr: 0       4 4 4 4 
   col: 0 2 3 4
   val: 0 0 0 0  
```
After reinsertion
```
rowptr: 0       4 5 5 5
   col: 0 2 3 4 1
   val: 0 0 0 0 1
```
Now we do the same for (0,3) and (0,4) and we have
```
rowptr: 0   2     5 5 5
   col: 0 2 1 3 4
   val: 0 0 1 1 1
```
Next we do (1,2)
```
rowptr: 0 1     4 5 5
   col: 0 1 3 4 2
   val: 0 1 1 1 2
```
And finally (2,4)
```
rowptr: 0 1   3 4 5
   col: 0 1 3 2 4
   val: 0 1 1 2 3
```
This is our final wave_rel. What if we did the same process, but made it (iteration, wavefront)? We start with
```
rowptr: 0 1 2 3 4 5
   col: 0 0 0 0 0 
   val: 0 0 0 0 0
```
For the dependence (0,1), we get the wavefront 0 and 0, so we need to remove (1,0) and insert (1,1). Remove:
```
rowptr: 0 1 1 2 3 4
   col: 0   0 0 0 
   val: 0   0 0 0
```
Insert:
```
rowptr: 0 1 2 3 4 5
   col: 0 1 0 0 0 
   val: 0 1 0 0 0
```
Next we do dependence (0,3)
Remove (3,0):
```
rowptr: 0 1 2 3 3 4
   col: 0 1 0   0 
   val: 0 1 0   0
```
Insert (3,1):
```
rowptr: 0 1 2 3 4 5
   col: 0 1 0 1 0 
   val: 0 1 0 1 0
```

Next is dep (0,4), giving us:
```
rowptr: 0 1 2 3 4 5
   col: 0 1 0 1 1 
   val: 0 1 0 1 1
```

Next is dep (1,2), so delete (2,0) insert (2,2)
```
rowptr: 0 1 2 3 4 5
   col: 0 1 2 1 1 
   val: 0 1 2 1 1
```

Next is dep (2,4) delete (4,1) insert (4,3)
```
rowptr: 0 1 2 3 4 5
   col: 0 1 2 1 3 
   val: 0 1 2 1 3
```

So I still think this a weird way to do it, but maybe thats not the point, and the point is just to compare the different ways. 