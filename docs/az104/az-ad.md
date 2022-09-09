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
|    Free    |  Limmité à 50 000 objets  | :heavy_check_mark: | :heavy_check_mark: |                          |                    |                    |                     |                     |

### Les comptes d'utilisateurs
