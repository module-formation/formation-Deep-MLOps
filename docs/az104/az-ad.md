# AZ-104: Microsoft Azure Administrator - Managing Azure Active Directory

On se concentre ici sur le concept d'identité. Comment Azure Active Directory sécurise votre identité. Comment les utilisateurs et les groupes sont implémentés dans Azure AD.

## Introduction à Azure AD

Azure AD est le service de gestion des identités et des répertoires basé sur le cloud qui permet l'accès aux services Azure et à d'autres solutions SaaS comme Microsoft 365, DropBox, Concur, Salesforce, etc.

Il offre également des options de self-service, notamment la réinitialisation des mots de passe, l'authentification, la gestion des appareils, les identités hybrides et l'authentification unique (SSO).

### Concepts

#### Identité

Un objet qui peut être authentifié est considéré comme une identité. Ca peut être :

* un utilisateur,
* un groupe,
* une identité managée (corresponf à une identité d'une ressource Azure),
* un service principal.

#### Compte

Lorsque nous associons des attributs à une identité, cela devient un compte.

!!! example "Exemple"

    * Un utilisateur aura plusieurs attributs comme sa localisation, son département, son manager, son numéro de téléphones, etc. On obtient un **compte d'utilisateur**.

    * Un groupe aura comme attributs ses membres, une description, une adresse email. On obtient un **compte de groupe**.

#### Compte Azure AD

Tout compte qui est créé dans Azure AD ou par un autre service cloud de Microsoft est connu comme un **compte Azure AD**.

#### Azure AD Tenant ou directory

C'est un instance dédiée de Azure AD qui est créée durant la création de n'importe quelle souscription à un service Microsoft cloud. **Tenant** et **Directory** siginifient la même chose et sont interchangeables.

C'est via ce Tenant que l'on peut gérer les utilisateurs, groupes attenants à la souscription.

Une organisation peut avoir un voire plusieurs Azure AD tenants suivant ses besoins.

### Azure AD vs Active Directory Domain Services (ADDS)

!!! attention "Attention"

    Ce sont deux services complètement différents



|                                                               Azure AD                                                                |                                                  ADDS                                                   |
| :-----------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------: |
|                                                       Requêtage via HTTP/HTTPS                                                        |                                           Requêtage via LDAP                                            |
| Les protôcoles utilisés pour l'authentification incluent SAML, WS-Federation, OpenID connect. OAuth est utilisé pour l'authorisation. |                         Kerberos est utilisé pour l'authentification dans ADDS                          |
|                           La fédération peut être mise en place avec des fournisseurs tiers comme Facebook.                           | La fédération est possible uniquement avec d'autres domaines. Les services tiers en sont pas supportés. |
|                                                    Azure AD est une offre managée.                                                    |                             ADDS tourne sur une VM ou un serverus physique.                             |


### Les différentes éditions d'Azure AD

On a 4 versions différentes d'azure AD :

* Premium P2,
* Premium P1,
* M365 Apps,
* Free.

Premium P2 possède le plus grand nombre de features, tandis que l'édition free en a le moins.

|            | No object directory limit |   SSO & Core IAM   | B2B collaboration  | O365 Identity and access |  Hybrid identity   | Conditional access | Identity protection | Identity governance |
| :--------: | :-----------------------: | :----------------: | :----------------: | :----------------------: | :----------------: | :----------------: | :-----------------: | :-----------------: |
| Premium P2 |    :heavy_check_mark:     | :heavy_check_mark: | :heavy_check_mark: |    :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:  | :heavy_check_mark:  |
| Premium P1 |    :heavy_check_mark:     | :heavy_check_mark: | :heavy_check_mark: |    :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark: |                     |                     |
| M365 Apps  |    :heavy_check_mark:     | :heavy_check_mark: | :heavy_check_mark: |    :heavy_check_mark:    |                    |                    |                     |                     |
|    Free    |  Limité à 50 000 objets  | :heavy_check_mark: | :heavy_check_mark: |                          |                    |                    |                     |                     |

### Les comptes d'utilisateurs

Les comptes utilisateurs sont utilisés pour l'authentification et l'authorisation. Tous les utilisateurs doivent avoir un compte.

Chaque compte peux avoir plusieurs propriétés facultatives, comme l'adresse, le département (dans l'entreprise, l'organisation).

Il est possble d'obtenir la liste complète des utilisateurs via le chemin Azure Active Directory > Users > All Users (pourvu que votre compte ait le droit d'y accéder).

Il est possible d'appliquer des opérations en masse sur les utilisateurs.

Il existe 3 types de comptes différents :

1. Les identités cloud. Ce sont des utilisateurs qui existent uniquement dans l'AD Azure, peuent aussi provenir d'un AD Azure externe.
2. Les comptes invités. Ce sont des utilisateurs qui existent en dehors de l'Ad Azure et qui ont été invités à le rejoindre, par exemple des comptes Microsoft, Lives, etc.
3. Des comptes synchronisés. Ce sont des comptes qui proviennent d'un AD Windows onprem, ils sont impossible à créer et ne peuvent être que synchronisés.

Si un utilisateur est supprimé de l'AD Azure, il sera gardé en mémoire pendant 30 jours.

### Opérations on masse (bulk operations)

Plutôt que d'inviter, supprimer ou créer des utilisateurs un par un, il est possible de faire ces mêmes opérations en masse via la commande **Bulk operations**, qui permet de télécharger un csv pour :

1. créer des utilisateurs en masse,
2. inviter des utilisateurs en masse,
3. supprimer des des utilisateurs en masse.

### Les comptes de groupes

Tout comme pour les utilisateurs, il est possible de créer des groupes. Il en existe deux types :

1. Les groupes de sécurité, qui permettent des gérer les autorisations d'accès.
2. Les groupes M365, qui permettent la collaboration et l'accès aux ressources de Microsoft 365.

Types d'assignations à un groupe :

1. Les utilisateurs peuvent êtres assignés (`Assigned`) par un administrateur à un groupe et ils ne peuvent pas quitter per eux mêmes, seul l'administrateur peut les révoquer.
2. On peut avoir des assignations dynamiques (`Dynamic user`) où l'assignation se fait via attributs, l'AD assignera ou supprimera un utilisateur de façon dynamique d'un groupe suivant ses attributs.
3. On peut avoir des assignations dynamiques pour les devices (`Dynamic device`), **uniquement pour les groupes de sécurité**, les devices seront assignés ou supprimés de façon dynamique en fonction de leur OS, de leur version, etc.

### Azure AD Join

Azure AD join permet de gérer les différents devices pour être sur qu'ils suivent les règles standards de sécurité éditées dans l'entreprise.

Azure AD join permet aussi d'avoir accès à ces différents services.

1. Single Sign-On : autorise le SSO pour vos applications, services, SaaS solutions.
2. Accès à Microsoft Store for Business : permet de publier vos applications internes sur le store  pour un usage interne.
3. Roaming d'entreprise : pour synchroniser vos paramètres et configurations entre vos différents devices.
4. Windows Hello : support pour windows Hello, pour de la reconnaissance biométrique.
5. Gestion des devices : pour gérer et si nécessaire restreindre l'accès aux applications.
6. Accès onprem :accès aux ressources et applications onprem.

### SSPR : Self Service Password Reset

Permet à l'utilisateur de modifier son mot de passe sans passer par l'IT, plusieurs méthodes peuvent êtres proposées (via mail, sms, mobile app code  etc.). Il est possible d'en configurer 2 maximums.

C'est une feature qui n'est accessible qu'avec une licence Premium P2. Le SSPR peut être mis en place au niveau des groupes directement. il est activé par défaut pour les comptes admins.

### Environnements multi tenant
