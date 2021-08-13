# Gradient Centralization: A New Optimization Technique for Deep Neural Networks

- [ArXiv](https://arxiv.org/abs/2004.01461)

## Abstract

Optimization techniques are of great importance to effectively and efficiently train a deep neural network (DNN). It has been shown that using the first and second order statistics (e.g., mean and variance) to perform Z-score standardization on network activations or weight vectors, such as batch normalization (BN) and weight standardization (WS), can improve the training performance. Different from these existing methods that mostly operate on activations or weights, we present a new optimization technique, namely gradient centralization (GC), which operates directly on gradients by centralizing the gradient vectors to have zero mean. GC can be viewed as a projected gradient descent method with a constrained loss function. We show that GC can regularize both the weight space and output feature space so that it can boost the generalization performance of DNNs. Moreover, GC improves the Lipschitzness of the loss function and its gradient so that the training process becomes more efficient and stable. GC is very simple to implement and can be easily embedded into existing gradient based DNN optimizers with only one line of code. It can also be directly used to fine-tune the pre-trained DNNs. Our experiments on various applications, including general image classification, fine-grained image classification, detection and segmentation, demonstrate that GC can consistently improve the performance of DNN learning. The code of GC can be found at [this https URL](https://github.com/Yonghongwei/Gradient-Centralization).

## Notes

La centralisation du gradient, est une nouvelle méthode d'optimisation des réseaux de neurones (plutôt une modification de celles déjà existantes), qui se concentre sur le gradient lui même afin de le centrer, i.e. étant donné le vecteur gradient $\overrightarrow{\mathrm{grad}}$ obtenu en différentiant la fonction de perte $\mathcal{L}_{\vartheta}$, on le centralise de façon à obtenir $\overrightarrow{\mathrm{grad}}_{CG}$ vérifiant l'églite suivante.

\[
    \mathbb{E}(\overrightarrow{\mathrm{grad}}_{CG}) =0
\]

!!! info "Remarque"

    On le verra par la suite, cette méthode peut être vu de façon géométrique comme une projection orthogonale du gradient sur un hyperplan contraignant la fonction de perte $\mathcal{L}_{\vartheta}$.

### Introduction

L'éfficacité de l'entraînement des réseaux de neurones dépend beaucoup des techniques d'optimization employées.

Le choix d'un optimiseur (Adam, RMSProp, Nesterov, etc) se fait généralement sur deux critères :

1. L'accélération de l'entraînement qui en résulte.
2. L'amélioration de la capacité de généralisation du réseau.

D'autres techniques d'optimisation existent :

- Les méthodes d'initialisation des poids (He, Xavierc etc),
- Le choix des fonctions d'activations (ReLU, mish),
- Le clipping du gradient,
- Mettre en place un taux d'apprentissage adaptatif.

Il existe aussi des techniques de normalisation et de standardisation des poids, **mais ces dernières ne sont pas applicables aux modèles pré-entrainés, dont les poids ne peuvent pas être centrés, normés** (sinon on perd l'intérêt du pré-entraînement).

L'article apporte deux contributions :

- Une nouvelle technique d'optimisation basée sur la centralisation du gradient, qui est facilement implémentable, [voir le tutoriel sur keras.io](https://keras.io/examples/vision/gradient_centralization/#implement-gradient-centralization).
- Les aspects théoriques de cette centralisation du gradient. L'article montre en particuliers que la centralisation du gradient :
    1. contraint la fonction de perte en ajoutant une nouvelle contrainte sur le vecteur de poids, ce qui permet de régulariser l'espace des poids ainsi de celui des features de sortie.
    2. Améliore les propriétés lipschitzienne de la fonction de perte.

!!! note "Définition"

    1. Une fonction $f$ entre deux espaces métriques $f \, : \, (X, d_{1}) \rightarrow (Y, d_{2})$ est lipschitz s'il existe une constante $C >0$ telle que :

    \[
        \forall x, y \in X, d_{2}(f(x), f(y)) \leq C d_{1}(x,y).
    \]

    En particulier, la fonction $f$ est continue.

    2. Une fonction différentiable $f$ entre deux espaces normés $f \, : \, (X, d_{1}) \rightarrow (Y, d_{2})$ est lipschitz lisse s'il existe une constante $C >0$ telle que :

    \[
        \forall x, y \in X, \| \nabla f(x) - \nabla f(y) \| \leq C \| x - y \|.
    \]

    ($C$-Lipschitz continuous gradient)

    3. La constante $C$ est appélée la constante de Lipschitz de $f$.

!!! info "A voir"

    - [Lipschitz Smoothness, Strong Convexity and the Hessian](https://math.stackexchange.com/questions/673898/lipschitz-smoothness-strong-convexity-and-the-hessian)
    - [Lipschitz continuous gradient](https://xingyuzhou.org/blog/notes/Lipschitz-gradient)

### Centralisation du gradient

On sait que la *Batch Normalization* permet de réduire la constante de Lipschitz de la fonction de perte $\mathcal{L}_{\vartheta}$ (TODO : Sources) et rend les gradients *plus lipschitz continus*.

Cependant, si la *batch size* est petite, la *Group Normalization* est plus appropriée, on perd alors les propriétés citées ci-dessus.

Peut-on directement opérer sur le gradient pour stabiliser l'entraînement ? Normaliser le gradient n'améliore pas la stabilité de l'entraînement, on va dire le centrer, ie le rendre d'espérance nulle.

### Notations et conventions

- Lorsque l'on parlera qu'une couche dense, on notera sa matrice de poids

    \[
    W_{fc} \in \mathbb{R}^{C_{in} \times C_{out}}.
    \]

- Lorsque l'on parlera d'une couche convolutive, on notera sa matrice de poids

    \[
        W_{conv} \in \mathbb{R}^{C_{in} \times C_{out} \times (k_{1}k_{2})},
    \]

    $k_{1}$ et $k_{2}$ étant les dimensions des noyaux de convolutions.

- Pour une couche quelconque, on utilisera la notation unifiée $W \in \mathbb{R}^{M \times N}$. Pour $W_{fc}$, $M = C_{in}$, et pour $W_{fc}$, $M = C_{in}k_{1}k_{2}$.

- Pour une couche $W \in \mathbb{R}^{M \times N}$, on notera $w_{i} \in \mathbb{R}^{M}, i = 1, \dots, N$ sa $i$-ième colonne.

!!! attention "Convention matricielle"

    pour un vecteur d'entrée $X$ de la couche $W$, les features en sortie de la couche sont alors données par la formule suivante.

    \[
        out_{W}(X) := W^{T} \cdot X \qquad W^{T} \in \mathbb{R}^{C_{out} \times C_{in}}
    \]

    Ce qui veut dire que par convention, les vecteurs considérés ici sont des **vecteurs colonnes**.

    \[
    out_{W}(X) =
    \left[
    \begin{array}{ccc}
        \rule[.5ex]{2.5ex}{0.5pt} & w^{T}_{1} & \rule[.5ex]{2.5ex}{0.5pt} \\
        \rule[.5ex]{2.5ex}{0.5pt} & w^{T}_{2} & \rule[.5ex]{2.5ex}{0.5pt}
    \end{array}
    \right]^{T}
    \cdot
    \begin{bmatrix}
            x_{1} \\
            x_{2}
    \end{bmatrix}
    \]

    \[
    W^{T} \cdot X =
    \left[
    \begin{array}{ccc}
        w_{1,1} & w_{1,2} & w_{1,3} \\
        w_{2,1} & w_{2,2} & w_{2,3}
    \end{array}
    \right]^{T}
    \cdot
    \begin{bmatrix}
            x_{1} \\
            x_{2}
    \end{bmatrix}
    \]

- Pour la fonction de perte $\mathcal{L}_{\vartheta}$, on notera son gradient $\nabla_{W}\mathcal{L}_{\vartheta}$ par rapport à la matrice de poids $W$, et $\nabla_{w_{i}}\mathcal{L}_{\vartheta}$ son gradient par rapport au vecteur de poids $w_{i}$.

- On note $\mathbf{e} := \frac{1}{\sqrt{M}}\cdot \mathbb{1}_{M}$, vecteur unitaire de $\mathbb{R}^{M}$.

### Formulation de la centralisation du gradient

Pour une couche dense ou convolutive, supposons que l'on a obtenu le gradient via rétropropagation.

Pour un vecteur de poids $w_{i}$, de gradient $\nabla_{w_{i}}\mathcal{L}_{\vartheta}$, l'opérateur de centralisation du gradient, noté $\Phi_{CG}$, est alors défini comme suit.

\[
    \Phi_{CG}(\nabla_{w_{i}}\mathcal{L}_{\vartheta}) := \nabla_{w_{i}}\mathcal{L}_{\vartheta} - \mathbb{E}(\nabla_{w_{i}}\mathcal{L}_{\vartheta})
\]

Où

\[
    \mathbb{E}(\nabla_{w_{i}}\mathcal{L}_{\vartheta}) := \frac{1}{M}\sum_{j=1}^{M}\nabla_{w_{i,j}}\mathcal{L}_{\vartheta}.
\]

En d'autres termes, pour une matrice de poids, on calcule la moyenne de chaque vecteur colonne de cette matrice et on retire cette moyenne à ses colonnes.

### Formulation matricielle et représentation géométrique

!!! note "Définition : Produit de Kronecker"

    Pour $x$ et $y$ deux vecteurs colonnes de dimensions $M$, respectivement $N$, le prodouit de Kronecker de $x$ et $y$, noté $x \cdot y^{T}$ ou $x \otimes y$ est alors défini de la façon suivante.

    \[
        x \cdot y^{T} := \left[ x_{i} \cdot y_{j}\right]
    \]

    Où $\left[ x_{i} \cdot y_{j}\right] \in \mathbb{R}^{M \times N}$ est la matrice dont les coefficients en les coordonnées $(i,j)$ sont données par le produit $x_{i} \cdot y_{j}$.

    Ce produit n'est pas commutatif. C'est un cas particulier de produit tensoriel, [voir ici](https://fr.wikipedia.org/wiki/Produit_matriciel#Produit_de_Kronecker).

Dans le cas qui nous intéresse ici, on applique le produit de Kronecker au vecteur suivant : $\mathbf{e}$.

\[
    \begin{align*}
    \mathbf{e} \otimes \mathbf{e} & := \frac{1}{\sqrt{M}}\cdot \mathbb{1} \otimes \frac{1}{\sqrt{M}}\cdot \mathbb{1} \\
                                  & = \frac{1}{M}\cdot \mathbb{1} \otimes \mathbb{1} \\
                                  & = \frac{1}{M}\cdot \mathbb{1} \otimes \mathbb{1} \\
                                  & = \frac{1}{M}\cdot\left[
                                        \begin{array}{ccc}
                                            1 & \cdots & 1 \\
                                            \vdots &  & \vdots \\
                                            1 & \cdots & 1
                                        \end{array}
                                        \right]
    \end{align*}
\]

Ici, $\mathbb{1} \otimes \mathbb{1}$ est donc une matrice carrée de taille $M \times M$ où tous les coefficients sont égaux à $1$.

Remarquons que dans l'autre sens, le produit scalaire $\mathbf{e}^{T} \cdot \mathbf{e}$ est égal à $1$, car $\mathbf{e}$ est par définition un vecteur unitaire.

Pour une matrice de poids $W$, de gradient $\nabla_{W}\mathcal{L}_{\vartheta}$, l'opérateur de centralisation du gradient, noté $\Phi_{CG}$, est alors défini comme suit.

\[
    \Phi_{CG}(\nabla_{W}\mathcal{L}_{\vartheta}) := \mathbf{P}(\nabla_{W}\mathcal{L}_{\vartheta})
\]

Où $\mathbf{P} := \mathbb{I}_{M} - \mathbf{e} \otimes \mathbf{e}$. $\mathbb{I}_{M}$ étant la matrice identité de taille $M$.

Avant de voir les propriétés de l'opérateur $\mathbf{P}$, vérifions que l'on obtient bien le même résultat avec cette définition que la précédente.

On a $\nabla_{W}\mathcal{L}_{\vartheta} := \left[ \nabla_{w_{1}}\mathcal{L}_{\vartheta} , \cdots, \nabla_{w_{N}}\mathcal{L}_{\vartheta} \right]$, d'où

\[
    \begin{align*}
    \Phi_{CG}(\nabla_{W}\mathcal{L}_{\vartheta}) & = \left(\mathbb{I}_{M} - \mathbf{e} \otimes \mathbf{e} \right)\cdot \left[ \nabla_{w_{1}}\mathcal{L}_{\vartheta} , \cdots, \nabla_{w_{N}}\mathcal{L}_{\vartheta} \right] \\
                                                 & = \left[ \nabla_{w_{1}}\mathcal{L}_{\vartheta} , \cdots, \nabla_{w_{N}}\mathcal{L}_{\vartheta} \right] - \frac{1}{M}\cdot \mathbb{1} \cdot \mathbb{1}^{T} \cdot \left[ \nabla_{w_{1}}\mathcal{L}_{\vartheta} , \cdots, \nabla_{w_{N}}\mathcal{L}_{\vartheta} \right].
    \end{align*}
\]

Par linéarité, il suffit de le vérifier sur chaque colonne.

\[
    \begin{align*}
    \nabla_{w_{i}}\mathcal{L}_{\vartheta} - \frac{1}{M}\cdot \mathbb{1} \cdot \mathbb{1}^{T} \cdot \nabla_{w_{i}}\mathcal{L}_{\vartheta} & = \nabla_{w_{i}}\mathcal{L}_{\vartheta} - \frac{1}{M}\cdot \mathbb{1} \cdot \left( \mathbb{1}^{T} \cdot \nabla_{w_{i}}\mathcal{L}_{\vartheta} \right) \\
    & = \nabla_{w_{i}}\mathcal{L}_{\vartheta} - \frac{1}{M}\cdot \mathbb{1} \cdot \left(\sum_{j=1}^{M}\nabla_{w_{i,j}}\mathcal{L}_{\vartheta}\right) \\
    & = \nabla_{w_{i}}\mathcal{L}_{\vartheta} - \mathbb{E}(\nabla_{w_{i}}\mathcal{L}_{\vartheta})
    \end{align*}
\]

On a donc bien le même résultat, peut importe la définition. Passons donc maintenant aux propriétés de l'opérateur $\mathbf{P}$.

!!! note "Théorème"

    L'opérateur $\mathbf{P}$ est idempotent et définie une projection sur l'hyperplan orthogonal au vecteur unitaire $\mathbf{e}^{T}$.

Montrons premièrement que c'est un opérateur idempotent. Pour cela il suffit de montrer que $P^{2} = P = P^{T}$. Tout d'abord, on a $P^{T} = (\mathbb{I}_{M} - \mathbf{e} \otimes \mathbf{e})^{T} = \mathbb{I}_{M}^{T} - (\mathbf{e} \cdot \mathbf{e}^{T})^{T} = \mathbb{I}_{M} - \mathbf{e} \cdot \mathbf{e}^{T} = P$.

D'où,

\[
    \begin{align*}
        P^{2} = P^{T}P & = (\mathbb{I}_{M} - \mathbf{e} \otimes \mathbf{e})^{T} \cdot (\mathbb{I}_{M} - \mathbf{e} \otimes \mathbf{e}) \\
                       & = \mathbb{I}_{M} - 2 \mathbf{e}\cdot \mathbf{e}^{T} + \mathbf{e}\cdot (\mathbf{e}^{T}\cdot \mathbf{e})\cdot \mathbf{e}^{T} \\
                       & = \mathbb{I}_{M} - 2 \mathbf{e}\cdot \mathbf{e}^{T} + \mathbf{e}\cdot\mathbf{e}^{T} \\
                       & = \mathbb{I}_{M} - \mathbf{e}\cdot \mathbf{e}^{T} \\
                       & = P.
    \end{align*}
\]

$P$ étant une application linéaire de $\mathbb{R}^{M} \rightarrow \mathbb{R}^{M}$, on a la somme directe

\[
    \mathbb{R}^{M} = \ker P \oplus \mathrm{im} \, P,
\]

avec

\[
    \mathrm{im}\,P = \ker(\mathbb{I}_{M}-P),
\]

or $\ker(\mathbb{I}_{M}-P) = \ker(\mathbb{I}_{M}-(\mathbb{I}_{M} - \mathbf{e} \otimes \mathbf{e})) = \ker (\mathbf{e} \otimes \mathbf{e})$.

\[
    \ker (\mathbf{e} \otimes \mathbf{e}) = \left\{ (x_{1}, \dots, x_{M}) \in \mathbb{R}^{M} \, : \, \sum_{i=1}^{M} x_{i} = 0 \right\}
\]

Cela définit bien un hyperplan, **l'hyperplan des vecteurs centrés**, ie de moyenne nulle. De plus, on a $\mathbf{e}^{T}\mathbf{P} = \mathbf{e}^{T}(\mathbb{I}_{M} - \mathbf{e} \otimes \mathbf{e}) = \mathbf{e}^{T} - (\mathbf{e}^{T} \cdot \mathbf{e}) \cdot \mathbf{e}^{T} = \mathbf{e}^{T} -  \mathbf{e}^{T} = 0$.

**Donc** $\mathbf{P}$ **est un opérateur de projection sur l'hyperplan orthogonal au vecteur unitaire** $\mathbf{e}^{T}$.

\[
    P \, : \, \mathbb{R}^{M\times N} \longrightarrow \mathbb{R}^{M\times N}
\]

\[
    \mathbb{R}^{M\times N} = \ker(\mathbf{e} \otimes \mathbf{e})^{M \times N} \oplus \left( \left\langle \mathbb{1}_{M} \right\rangle \oplus \cdots \oplus \left\langle \mathbb{1}_{M} \right\rangle \right)
\]

### Application à la descente du gradient

!!! attention "Attention"

    On rappelle ici que la couche dense ou convolutive sur laquelle on opère **est fixée**.

    Pour un réseau de neurones, **on a donc un opérateur de centralisation $\Phi_{CG}$, par couche dense et convolutive**.

Pour chaque couche de matrice de poids $W \in \mathbb{R}^{M \times N}$, on a donc :

- un vecteur unitaire $\mathbf{e}_{W} = \frac{1}{\sqrt{M}}\cdot \mathbb{1}_{W}$,
- et un opérateur de centralisation $\Phi_{CG}$ projetant sur $\ker (\mathbf{e}_{W} \otimes \mathbf{e}_{W})$ orthogonalement à $\mathbf{e}_{W}^{T}$.

![cg](./images/centralized_gradient.svg)

Notons $W^{t}$ la matrice des poids à l'itération $t$ pour une couche fixée. Une équation de l'hyperplan sur lequel projette $\Phi_{CG}$ est la suivante.

\[
    \mathcal{H} := \left\{ -w \in \mathbb{R}^{M} \, : \, \mathbf{e}_{W}^{T} \cdot w  = 0 \right\}
\]

