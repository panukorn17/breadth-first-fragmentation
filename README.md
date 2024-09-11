# breadth-first-fragmentation


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## Usage

### Installation

Install latest from the GitHub
[repository](https://github.com/panukorn17/breadth-first-fragmentation):

``` sh
$ pip install git+https://github.com/panukorn17/breadth-first-fragmentation.git
```

or from
[conda](https://anaconda.org/ptaleo17/breadth-first-fragmentation)

``` sh
$ conda install ptaleo17::breadth-first-fragmentation
```

or from [pypi](https://pypi.org/project/breadth-first-fragmentation/)

``` sh
$ pip install breadth_first_fragmentation
```

### Documentation

Documentation can be found hosted on this GitHub
[repository](https://github.com/panukorn17/breadth-first-fragmentation)’s
[pages](https://panukorn17.github.io/breadth-first-fragmentation/).
Additionally you can find package manager specific guidelines on
[conda](https://anaconda.org/ptaleo17/breadth-first-fragmentation) and
[pypi](https://pypi.org/project/breadth-first-fragmentation/)
respectively.

## How to use

``` python
from breadth_first_fragmentation.fragmentation import break_into_fragments_defragmo
```

``` python
smi = 'CCCN(CCc1cccc(-c2ccccc2)c1)C(=O)C1OC(C(=O)O)=CC(N)C1NC(C)=O'
break_into_fragments_defragmo(smi, min_length=0, verbose=1)
```

    Head fragment:  *CCC
    Recurse tail:  N(*)(CCc1cccc(-c2ccccc2)c1)C(=O)C1OC(C(=O)O)=CC(N)C1NC(C)=O
    Tail:  *CCc1cccc(-c2ccccc2)c1
    Recurse Head:  N(*)(*)C(=O)C1OC(C(=O)O)=CC(N)C1NC(C)=O
    Head fragment:  *N(*)*
    Recurse tail:  C(*)(=O)C1OC(C(=O)O)=CC(N)C1NC(C)=O
    Head fragment:  *C(*)=O
    Recurse tail:  C1(*)OC(C(=O)O)=CC(N)C1NC(C)=O
    Head fragment:  *NC1C(N)C=C(C(=O)O)OC1*
    Recurse tail:  C(*)(C)=O
    Final Fragment:  C(*)(C)=O

    ('CCCN(CCc1cccc(-c2ccccc2)c1)C(=O)C1OC(C(=O)O)=CC(N)C1NC(C)=O',
     '*CCC *CCc1cccc(-c2ccccc2)c1 *N(*)* *C(*)=O *NC1C(N)C=C(C(=O)O)OC1* C(*)(C)=O',
     6)

Visual representation of the breadth-first-fragmentation algorithm:
</br>
<img src="images/breadth-first-fragmentation.png" alt="breadth-first-fragmentation" style="width: 450px;"/>

``` python
smi = 'CCCN(CCc1cccc(-c2ccccc2)c1)C(=O)C1OC(C(=O)O)=CC(N)C1NC(C)=O'
break_into_fragments_defragmo(smi, min_length=3, verbose=1)
```

    Head fragment:  *CCC
    Recurse tail:  N(*)(CCc1cccc(-c2ccccc2)c1)C(=O)C1OC(C(=O)O)=CC(N)C1NC(C)=O
    Tail:  *CCc1cccc(-c2ccccc2)c1
    Recurse Head:  N(*)(*)C(=O)C1OC(C(=O)O)=CC(N)C1NC(C)=O
    Head fragment:  *C(=O)N(*)*
    Recurse tail:  C1(*)OC(C(=O)O)=CC(N)C1NC(C)=O
    Head fragment:  *NC1C(N)C=C(C(=O)O)OC1*
    Recurse tail:  C(*)(C)=O
    Final Fragment:  C(*)(C)=O

    ('CCCN(CCc1cccc(-c2ccccc2)c1)C(=O)C1OC(C(=O)O)=CC(N)C1NC(C)=O',
     '*CCC *CCc1cccc(-c2ccccc2)c1 *C(=O)N(*)* *NC1C(N)C=C(C(=O)O)OC1* C(*)(C)=O',
     5)
