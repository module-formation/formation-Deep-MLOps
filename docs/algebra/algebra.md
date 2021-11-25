# Algèbre tensorielle

**Sources** :

* [Einstein summation for multi-dimensional arrays](http://www.nik.no/2000/Krister.Aahlander.pdf)
* [Einsum](https://www.drgoulu.com/2016/01/17/einsum/)
* [Einsum is All you Need - Einstein Summation in Deep Learning](https://rockt.github.io/2018/04/30/einsum)
* [Understanding einsum for Deep learning: implement a transformer with multi-head self-attention from scratch](https://theaisummer.com/einsum-attention/#the-einsum-and-einops-notation-basics)
* [einops](https://einops.rocks/)
* [Generalized Low Rank Models](https://stanford.edu/~boyd/papers/pdf/glrm.pdf)
* [Tensor Decompositions and Applications](https://www.kolda.net/publication/TensorReview.pdf)
* [Multilinear operators for higher-order decompositions](https://www.osti.gov/servlets/purl/923081)

## Introduction

Un tenseur est un "tableau multidimensionnel". L'ordre d'un tenseur est son nombre de dimensions :

* un tenseur d'ordre 1 est un vecteur,
* un tenseur d'ordre 2 est une matrice,
* de façon générale, un tenseur d'ordre $N$ est un élément du produit tensoriel de $N$ espaces vectoriels.

Pour un tenseur $\mathfrak{X}$ d'ordre $N$, ie $\mathfrak{X} \in \mathbb{R}^{I_{1} \times \cdots \times I_{N}}$, l'axe $k$ du tenseur correspond