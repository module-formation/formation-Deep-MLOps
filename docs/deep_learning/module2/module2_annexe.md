
# Relations entre convolution, convolution transposée et rétropropagation du gradient

## Représentation du produit de convolution comme un produit matriciel
Soit $F$ une feature map de taille $3 \times 3$, $k$ un noyau de convolution de taille $2 \times 2$ et $G$ la feature map obtenue comme le résultat de cette convolution, ie on a l'équation suivante.


\[
	G := F \odot k
\]

avec les matrices suivantes.

\[
	G := \begin{pmatrix}
		g_{0,0} & g_{0,1} \\
		g_{1,0} & g_{1,1}
	\end{pmatrix}
	\quad
	F :=
	\begin{pmatrix}
		f_{0,0} & f_{0,1} & f_{0,2} \\
		f_{1,0} & f_{1,1} & f_{1,2} \\
		f_{2,0} & f_{2,1} & f_{2,2}
		\\
	\end{pmatrix}
	\quad
	k := \begin{pmatrix}
		k_{0,0} & k_{0,1} \\
		k_{1,0} & k_{1,1}
	\end{pmatrix}
\]

On ne considère pour l'instant que le cas de la convolution dite "valide". Par définition du produit de convolution, on a les équation suivantes.

\[
\begin{equation}
	\begin{split}
		g_{0,0}  &:= f_{0,0}k_{0,0} + f_{0,1}k_{0,1} + f_{1,0}k_{1,0} + f_{1,1}k_{1,1} \\
		g_{0,1}  &:= f_{0,1}k_{0,0} + f_{0,2}k_{0,1} + f_{1,1}k_{1,0} + f_{1,2}k_{1,1} \\
		g_{1,0}  &:= f_{1,0}k_{0,0} + f_{1,1}k_{0,1} + f_{2,0}k_{1,0} + f_{2,1}k_{1,1} \\
		g_{1,1}  &:= f_{1,1}k_{0,0} + f_{1,2}k_{0,1} + f_{2,1}k_{1,0} + f_{2,2}k_{1,1}
	\end{split}
\end{equation}
\]

Réécrivons cela sous la forme d'un produit matriciel, en définissant sous la forme de vecteurs les matrices données plus haut.

\[
    F_{\mathrm{Vec}} := \begin{pmatrix}
		f_{0,0} & f_{0,1} & f_{0,2} & f_{1,0} & f_{1,1} & f_{1,2} & f_{2,0} & f_{2,1} & f_{2,2}
	\end{pmatrix}
\]

\[
	G_{\mathrm{Vec}} := \begin{pmatrix}
		g_{0,0} & g_{0,1} & g_{1,0} & g_{1,1}
	\end{pmatrix}
\]

On obtient la matrice suivant pour définir le noyau de convolution.

\[
	k_{\mathrm{Mat}} := \begin{pmatrix}
		k_{0,0} & k_{0,1} & 0       & k_{1,0} & k_{1,1} & 0       & 0       & 0       & 0       \\
		0       & k_{0,0} & k_{0,1} & 0       & k_{1,0} & k_{1,1} & 0       & 0       & 0       \\
		0       & 0       & 0       & k_{0,0} & k_{0,1} & 0       & k_{1,0} & k_{1,1} & 0       \\
		0       & 0       & 0       & 0       & k_{0,0} & k_{0,1} & 0       & k_{1,0} & k_{1,1}
	\end{pmatrix}
\]

Le produit de convolution se réécrit alors comme le produit matriciel suivant.

\[
	k_{\mathrm{Mat}} \cdot (F_{\mathrm{Vec}})^{T} = (G_{\mathrm{Vec}})^{T}
\]

La matrice $k$ définissant le produit de convolution est une matrice circulante double de Toeplitz

## Rétropropagation du gradient dans les CNN

On souhaite savoir comment se propage le gradient dans une couche convolutive.

Pour savoir cela on doit pouvoir calculer les deux dérivées partielles suivantes :$\frac{\partial \mathcal{L}}{\partial k}$ et $\frac{\partial \mathcal{L}}{\partial F}$.

1. La première étant nécessaire pour mettre à jour les poids du noyau de convolution,
2. La seconde pour continuer la rétro-propagation.

Pour les calculer, on utilise les deux propriétés suivantes :

1. La propriété des dérivations en chaînes :

\[
    \frac{\partial \mathcal{L}}{\partial k}  := \sum_{\ell} \frac{\partial \mathcal{L}}{\partial G_{\ell}} \cdot \frac{\partial G_{\ell}}{\partial k}
\]

\[
    \frac{\partial \mathcal{L}}{\partial F}  := \sum_{\ell} \frac{\partial \mathcal{L}}{\partial G_{\ell}} \cdot \frac{\partial G_{\ell}}{\partial F}
\]

2. La linéarité de l'opérateur de dérivation :

\[
    \forall \,\, i,j \quad \left(\frac{\partial \mathcal{L}}{\partial k} \right)_{i,j}  := \sum_{\ell} \frac{\partial \mathcal{L}}{\partial G_{\ell}} \cdot \frac{\partial G_{\ell}}{\partial k_{i,j}}
\]

\[
    \forall \,\, i,j \quad \left(\frac{\partial \mathcal{L}}{\partial F}\right)_{i,j}  := \sum_{\ell} \frac{\partial \mathcal{L}}{\partial G_{\ell}} \cdot \frac{\partial G_{\ell}}{\partial F_{i,j}}
\]

On suppose connu $\frac{\partial \mathcal{L}}{\partial G_{\ell}}$. Ce que l'on doit calculer ce sont les deux gradients locaux $\frac{\partial G_{\ell}}{\partial k_{i,j}}$ et $\frac{\partial G_{\ell}}{\partial F_{i,j}}$ pour toute les valeurs de $(i,j,\ell)$.

### Première dérivée

On doit donc calculer les dérivées partielles suivantes.

\[
\begin{equation}
	\begin{split}
		\left(\frac{\partial \mathcal{L}}{\partial k} \right)_{0,0}  & := \sum_{\ell} \frac{\partial \mathcal{L}}{\partial G_{\ell}} \cdot \frac{\partial G_{\ell}}{\partial k_{0,0}} \\
		\left(\frac{\partial \mathcal{L}}{\partial k} \right)_{0,1}  & := \sum_{\ell} \frac{\partial \mathcal{L}}{\partial G_{\ell}} \cdot \frac{\partial G_{\ell}}{\partial k_{0,1}} \\
		\left(\frac{\partial \mathcal{L}}{\partial k} \right)_{1,0}  & := \sum_{\ell} \frac{\partial \mathcal{L}}{\partial G_{\ell}} \cdot \frac{\partial G_{\ell}}{\partial k_{1,0}} \\
		\left(\frac{\partial \mathcal{L}}{\partial k} \right)_{1,1}  & := \sum_{\ell} \frac{\partial \mathcal{L}}{\partial G_{\ell}} \cdot \frac{\partial G_{\ell}}{\partial k_{1,1}}
	\end{split}
\end{equation}
\]

Pour $G$, $G_{\ell}$ correspond aux 4 fonctions suivants : $g_{0,0}, g_{0,1}, g_{1,0}, g_{1,1}$. On a alors la formule suivante.

\[
\begin{equation*}
	\begin{split}
		\left(\frac{\partial \mathcal{L}}{\partial k} \right)_{i,j} & := \sum_{r,s} \frac{\partial \mathcal{L}}{\partial g_{r,s}} \cdot \frac{\partial g_{r,s}}{\partial k_{i,j}} \\
		& =\frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot \frac{\partial g_{0,0}}{\partial k_{i,j}} + \frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot \frac{\partial g_{0,1}}{\partial k_{i,j}} + \frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot \frac{\partial g_{1,0}}{\partial k_{i,j}} + \frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot \frac{\partial g_{1,1}}{\partial k_{i,j}}
	\end{split}
\end{equation*}
\]

$\frac{\partial \mathcal{L}}{\partial g_{r,s}}$ étant supposé connu, il nous reste à calculer les gradient locaux $\frac{\partial g_{r,s}}{\partial k_{i,j}}$ , ce que l'on sait faire facilement grâce aux formules de l'équation précédente. En appliquant la formule précédente pour tous les couples $(i,j)$, on obtient les résultats suivants.

\[
\begin{equation}
	\left(\frac{\partial \mathcal{L}}{\partial k} \right)_{0,0} = \frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot f_{0,0} + \frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot f_{0,1} + \frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot f_{1,0} + \frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot f_{1,1}
\end{equation}
\]

\[
\begin{equation}
	\left(\frac{\partial \mathcal{L}}{\partial k} \right)_{0,1}  = \frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot f_{0,1} + \frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot f_{0,2} + \frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot f_{1,1} + \frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot f_{1,2}
\end{equation}
\]

\[
\begin{equation}
	\left(\frac{\partial \mathcal{L}}{\partial k} \right)_{1,0} = \frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot f_{1,0} + \frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot f_{1,1} + \frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot f_{2,0} + \frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot f_{2,1}
\end{equation}
\]

\[
\begin{equation}
	\left(\frac{\partial \mathcal{L}}{\partial k} \right)_{1,1} = \frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot f_{1,1} + \frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot f_{1,2} + \frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot f_{2,1} + \frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot f_{2,2}
\end{equation}
\]

Si on remet tout cela sous forme matricielle, on obtient alors la matrice suivante.

\[
	\frac{\partial \mathcal{L}}{\partial k}  =
	\begin{pmatrix}
		\left(\frac{\partial \mathcal{L}}{\partial k} \right)_{0,0} & \left(\frac{\partial \mathcal{L}}{\partial k} \right)_{0,1} \\
		\left(\frac{\partial \mathcal{L}}{\partial k} \right)_{1,0} & \left(\frac{\partial \mathcal{L}}{\partial k} \right)_{1,1}
	\end{pmatrix}
\]

La matrice $\frac{\partial \mathcal{L}}{\partial k}$ peut s'écrire comme le produit de convolution suivant.

\[
	\frac{\partial \mathcal{L}}{\partial k}
	=
	\begin{pmatrix}
		f_{0,0} & f_{0,1} & f_{0,2} \\
		f_{1,0} & f_{1,1} & f_{1,2} \\
		f_{2,0} & f_{2,1} & f_{2,2}
	\end{pmatrix} \odot \begin{pmatrix}
		\frac{\partial \mathcal{L}}{\partial g_{0,0}} & \frac{\partial \mathcal{L}}{\partial g_{0,1}} \\
		\frac{\partial \mathcal{L}}{\partial g_{1,0}} & \frac{\partial \mathcal{L}}{\partial g_{1,1}}
	\end{pmatrix}
\]

### Deuxième dérivée

On doit donc calculer les dérivées partielles suivantes.

\[
\begin{equation}
	\left(\frac{\partial \mathcal{L}}{\partial F} \right)_{i,j}  := \sum_{\ell} \frac{\partial \mathcal{L}}{\partial G_{\ell}} \cdot \frac{\partial G_{\ell}}{\partial F_{i,j}}
\end{equation}
\]

Pour $G$, $G_{\ell}$ correspond aux 4 fonctions suivants : $g_{0,0}, g_{0,1}, g_{1,0}, g_{1,1}$, et pour $F$, $F_{i,j}$ correspond à $f_{i,j}$. De la même façon que pour le calcul précédent, on a la formule suivante.

\[
\begin{equation*}
	\begin{split}
		\left(\frac{\partial \mathcal{L}}{\partial F} \right)_{i,j} & := \sum_{r,s} \frac{\partial \mathcal{L}}{\partial g_{r,s}} \cdot \frac{\partial g_{r,s}}{\partial f_{i,j}} \\
		& =\frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot \frac{\partial g_{0,0}}{\partial f_{i,j}} + \frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot \frac{\partial g_{0,1}}{\partial f_{i,j}} + \frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot \frac{\partial g_{1,0}}{\partial f_{i,j}} + \frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot \frac{\partial g_{1,1}}{\partial f_{i,j}}
	\end{split}
\end{equation*}
\]

En appliquant cette formule, on peut calculer les gradient locaux $\frac{\partial g_{r,s}}{\partial f_{i,j}}$ grâce aux formules de l'équation

\[
\begin{align*}
	\left(\frac{\partial \mathcal{L}}{\partial F} \right)_{0,0} & =
	\frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot k_{0,0}     \\
	\left(\frac{\partial \mathcal{L}}{\partial F} \right)_{0,1} & =
	\frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot k_{0,1} +
	\frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot k_{0,0}     \\
	\left(\frac{\partial \mathcal{L}}{\partial F} \right)_{0,2} & =
	\frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot k_{0,1}     \\
	\left(\frac{\partial \mathcal{L}}{\partial F} \right)_{1,0} & =
	\frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot k_{1,0} +
	\frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot k_{0,0}     \\
	\left(\frac{\partial \mathcal{L}}{\partial F} \right)_{1,1} & =
	\frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot k_{1,1} +
	\frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot k_{1,0} +
	\frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot k_{0,1} +
	\frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot k_{0,0}     \\
	\left(\frac{\partial \mathcal{L}}{\partial F} \right)_{1,2} & =
	\frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot k_{1,1} +
	\frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot k_{0,1}     \\
	\left(\frac{\partial \mathcal{L}}{\partial F} \right)_{2,0} & =
	\frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot k_{1,0}     \\
	\left(\frac{\partial \mathcal{L}}{\partial F} \right)_{2,1} & =
	\frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot k_{1,1} +
	\frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot k_{1,0}     \\
	\left(\frac{\partial \mathcal{L}}{\partial F} \right)_{2,2} & =
	\frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot k_{1,1}
\end{align*}
\]

Si on remet tout cela sous forme matricielle, on obtient alors la matrice suivante.

\[
    \frac{\partial \mathcal{L}}{\partial F}  =
	\begin{pmatrix}
    \frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot k_{0,0} &
    \frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot k_{0,1} +
    \frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot k_{0,0} &
    \frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot k_{0,1}   \\
    \\
    \frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot k_{1,0} +
    \frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot k_{0,0} &
    \frac{\partial \mathcal{L}}{\partial g_{0,0}} \cdot k_{1,1} +
    \frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot k_{1,0} +
    \frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot k_{0,1} +
    \frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot k_{0,0} &
    \frac{\partial \mathcal{L}}{\partial g_{0,1}} \cdot k_{1,1} +
    \frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot k_{0,1}
    \\
    \\
    \frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot k_{1,0} &
    \frac{\partial \mathcal{L}}{\partial g_{1,0}} \cdot k_{1,1} +
    \frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot k_{1,0} &
    \frac{\partial \mathcal{L}}{\partial g_{1,1}} \cdot k_{1,1}
    \end{pmatrix}
\]

Cette matrice provient en fait du produit de convolution complet suivant.

\[
	\frac{\partial \mathcal{L}}{\partial F}  =
	\begin{pmatrix}
		0 & 0                                             & 0                                             & 0 \\
		0 & \frac{\partial \mathcal{L}}{\partial g_{0,0}} & \frac{\partial \mathcal{L}}{\partial g_{0,1}} & 0 \\
		0 & \frac{\partial \mathcal{L}}{\partial g_{1,0}} & \frac{\partial \mathcal{L}}{\partial g_{1,1}} & 0 \\
		0 & 0                                             & 0                                             & 0 \\
	\end{pmatrix}
	\odot
	\begin{pmatrix}
		k_{1,1} & k_{1,0} \\
		k_{0,1} & k_{0,0}
	\end{pmatrix}
\]

### Lien avec la convolution initiale

Si on met le produit de convolution précédent sous la forme d'un produit matriciel, on obtient le résultat suivant.

\[
\begin{equation}
	\begin{split}
		\frac{\partial \mathcal{L}}{\partial F}  =
		\begin{pmatrix}
			k_{0,0} & 0       & 0       & 0       \\
			k_{0,1} & k_{0,0} & 0       & 0       \\
			0       & k_{0,1} & 0       & 0       \\
			k_{1,0} & 0       & k_{0,0} & 0       \\
			k_{1,1} & k_{1,0} & k_{0,1} & k_{0,0} \\
			0       & k_{1,1} & 0       & k_{0,1} \\
			0       & 0       & k_{1,0} & 0       \\
			0       & 0       & k_{1,1} & k_{1,0} \\
			0       & 0       & 0       & k_{1,1} \\
		\end{pmatrix}
		\cdot
		\begin{pmatrix}
			\frac{\partial \mathcal{L}}{\partial g_{0,0}} \\
			\frac{\partial \mathcal{L}}{\partial g_{0,1}} \\
			\frac{\partial \mathcal{L}}{\partial g_{1,0}} \\
			\frac{\partial \mathcal{L}}{\partial g_{1,1}} \\
		\end{pmatrix}
	\end{split}
\end{equation}
\]

Remarquez que le fait d'avoir fait une convolution complète n'apparaît pas dans le produit matriciel (ie on a pas rajouté plus de zéros), cette matrice là est la transposée de celle de l'équation.

\[
	\begin{pmatrix}
		k_{0,0} & 0       & 0       & 0       \\
		k_{0,1} & k_{0,0} & 0       & 0       \\
		0       & k_{0,1} & 0       & 0       \\
		k_{1,0} & 0       & k_{0,0} & 0       \\
		k_{1,1} & k_{1,0} & k_{0,1} & k_{0,0} \\
		0       & k_{1,1} & 0       & k_{0,1} \\
		0       & 0       & k_{1,0} & 0       \\
		0       & 0       & k_{1,1} & k_{1,0} \\
		0       & 0       & 0       & k_{1,1} \\
	\end{pmatrix}
	=
	\begin{pmatrix}
		k_{0,0} & k_{0,1} & 0       & k_{1,0} & k_{1,1} & 0       & 0       & 0       & 0       \\
		0       & k_{0,0} & k_{0,1} & 0       & k_{1,0} & k_{1,1} & 0       & 0       & 0       \\
		0       & 0       & 0       & k_{0,0} & k_{0,1} & 0       & k_{1,0} & k_{1,1} & 0       \\
		0       & 0       & 0       & 0       & k_{0,0} & k_{0,1} & 0       & k_{1,0} & k_{1,1}
	\end{pmatrix}^{T} = k_{\mathrm{Mat}}^{T}
\]


!!! note "Théorème"
	La transposée de la matrice définissant le noyau de convolution détermine comment se propage le gradient dans les couches en amont.

	En d'autres termes, l'erreur $\frac{\partial \mathcal{L}}{\partial G}$ est rétro-propagée en la multipliant par $k_{\mathrm{Mat}}^{T}$.
