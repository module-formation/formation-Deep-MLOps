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

## Travailler avec le mode RBAC

## Built-in-roles et Custom Roles

## Gérer l'accès via Azure Portal

## Les tags Azure

## Blocage des ressources

## Analyse des coûts

## Politiques Azure
