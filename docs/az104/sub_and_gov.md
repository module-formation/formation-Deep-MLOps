# Souscription et Gouvernance

## Gérer les souscriptions

Pour pouvoir utiliser Azure une souscription est nécessaire. Les ressources déployées sur votre compte Azure sont donc liées à cette souscription.

Les souscriptions permettent aussi de configurer les environnements différemmment. Ainsi, on peut par exemple imaginer une souscription de développment, de production, de tests, chacune ayant des ressources et des paramètres différents.

Chaque souscription possède une id unique, référencée sous le nom `id` lorsque l'on utilise la commande `az account show` de l'az-cli.

```shell
❯ az account show
{
  "environmentName": "AzureCloud",
  "homeTenantId": "xxx-6490-xxxx-a448-xxxx",
  "id": "xxxxxx-0cde-xxxxx-9162-xxxxxx",
  "isDefault": true,
  "managedByTenants": [],
  "name": "Abonnement Azure 1",
  "state": "Enabled",
  "tenantId": "xxxxx-6490-xxx-a448-xxx",
  "user": {
    "name": "klimczak.mathieu@pm.me",
    "type": "user"
  }
}
```
Un compte peut avoir plusieurs souscription, et toute identité provenant de l'Azure AD ou d'un service cloud de Microsoft peut créer une souscription.

Les souscriptions peuvent aussi air comme périmètre pour la gestion des accès.

il existe 4 types de souscriptions différentes.

1. **Enterprise Agreements**. Recommandé pour les organisations de plus de 500 utilisateurs ou devices, offre les services cloud et les licences softwares à un prix réduit.
2. **Pay-as-you-go**. Idéal pour les petites organisations ou les individus, seuls les services utilisés sont payés au fur et à mesure.
3. **Cloud Solution Provider**. Obtenu via Microsoft Partners, idéal pour les organisations petites à medium. La facturation est gérée par le partenaire.
4. **Free Trial**. 200$ de crédits sur 30 jours et accès limité gratuit pendant 12 mois.
5. **Azure for students**. Les étudiants sont éligibles à un crédit de 100$ sur 12 mois après vérification.
6. **Visual Studio**. Souscription gérée par crédit à toute pesonne ayant souscrit à Visual Studio Professionnal ou Enterprise.


## Comprendre la hiérarchie

![screen](./../images/az104/hierarchy.svg)

* Les `management groups` offrent un niveau de vision au dessus des `resource groups`, ce qui permet de grouper ces derniers ensembles.
* Un `management group` racine est créé par défaut, et l'on peut avoir jusque 6 niveaux de `management group` en dehors du groupe racine.
* Chaque souscription peut contenir un ou plusieurs `resource groups` permettant de grouper logiquement les ressources telles que les machines virtuelles, les base de données, etc.
* Cette hiérarchie permet d'implémenter les politiques d'accès, de gérer les coûts, etc.

$$
\text{Resource} \subset \text {Resource Group} \subset \text {Subscription} \subset \text {Management Group}
$$

## Travailler avec le mode RBAC

RBAC : Role Based Access Control

Permet aux administrateurs des donner l'accès aux ressources Azure et de séparer les responsabilités dans l'équipe.

* **Qui** : N'importe quelle identité demandant un accès. Ca peut être un utilisateur, un groupe, un service principal ou une identité managée.
* **Quoi** : Définition du rôle, ensemble d'opérations que l'identité pourra effectuer. Ecrit au format JSON.
* **Où** : Définir les limites de l'accès.

Ces 3 points définissent un rôle, qui peut alors être assignée à l'identité.

On peut avoir au maximum jusque 2000 rôles par souscription.

**Principe du moindre privilège**.

## Built-in-roles et Custom Roles

## Gérer l'accès via Azure Portal

## Les tags Azure

## Blocage des ressources

## Analyse des coûts

## Politiques Azure
