# Terraform 101

## Infrastructure as Code : IaC

Pour provisionner des ressources chez AWS, GCP, Azure, etc il est possible de passer par l'interface d'administration. Lorsque l'on a beaucoup de ressources à créer cela est loin d'être optimal.

L'idée est alors de coder tout cela, par exemple en passantt par du shell et l'interface en ligne de commande fournie pour rendre tout cela plus modulaire.


!!! example "Exemple d'IaC"

    ```shell title="Creation de 2 AZML workspace dans 2 resource groups"
    #!/bin/bash
    BLUE='\033[1;34m'
    GREEN='\033[1;32m'
    RED='\033[1;31m'
    NC='\033[0m' # No Color

    create_shared_resources(){

        resourceGroup1=${1:-"RG-EU-TEST-MLOPS1"}
        resourceGroup2=${2:-"RG-EU-TEST-MLOPS2"}
        workspace1=${3:-"workspace-mlops-1"}
        workspace2=${4:-"workspace-mlops-2"}
        location=${5:-"westeurope"}

        echo -e "${BLUE}resourceGroup1${NC}  : ${GREEN}$resourceGroup1${NC}"
        echo -e "${BLUE}resourceGroup2${NC}  : ${GREEN}$resourceGroup2${NC}"
        echo -e "${BLUE}workspace1${NC}      : ${GREEN}$workspace1${NC} "
        echo -e "${BLUE}workspace2${NC}      : ${GREEN}$workspace2${NC}"
        echo -e "${BLUE}location${NC}        : ${GREEN}$location${NC}"


        if ! az --version > /dev/null 2>&1;
            then
                echo -e "${RED}Failure: az cli is not installed. Please install it first.${NC}" >&2
                exit 1
            else
                echo -e "${GREEN}Success: az cli is installed, processing.${NC}"
        fi

        echo -e "${BLUE}Logging into your azure.${NC}"
        az login --tenant XXXXXXX.onmicrosoft.com

        echo -e "${BLUE}Create first resource group${NC}"
        az group create -l "$location" -n "$resourceGroup1"

        echo -e "${BLUE}Create second resource group${NC}"
        az group create -l "$location" -n "$resourceGroup2"

        echo -e "${BLUE}Create third resource group containing storage account${NC}"
        az group create -l "$location" -n "XXXXXXX"

        echo -e "${BLUE}Create storage account${NC}"
        az storage account create --name "storagemlops" --resource-group "XXXXXXX"

        echo -e "${BLUE}Get storage account resrouce id storage account${NC}"
        storage_id=$(az storage account show \
        --name storagemlops \
        --resource-group XXXXXXX \
        --query id \
        --output tsv)

        echo -e "${BLUE}Create workspace 1${NC}"
        az ml workspace create --file workspace1.yaml --resource-group "$resourceGroup1"

        echo -e "${BLUE}Create workspace 2${NC}"
        az ml workspace create --file workspace2.yaml --resource-group "$resourceGroup2"
    }


    create_shared_resources "$2" "$2" "$3" "$4" "$5"
    ```

Le code ci dessus, bien que fonctionnel, demande de savoir programmer en shell, et n'est pas réutilisable pour autre chose que ce pour quoi il est prévu. D'où le développement de solutions comme **Terraform** et **Ansible**.

En solution d'IaC, on peut par exemple citer :

* Docker,
* Ansible,
* Terraform,
* CloudFormation,
* Vagrant,
* Packer,
* Saltstack,
* Puppet.

Les solutions d'IaC se rangent généralement en 3 grandes sous-familles.

| Configuration Management | Server Templating | Provisionnement |
| :----------------------: | :---------------: | :-------------: |
|         Ansible          |      Docker       |    Terraform    |
|          Puppet          |      Packer       | CloudFormation  |
|        Saltstack         |      Vagrant      |                 |
|           Chef           |                   |                 |


### Configuration Management

Fait pour:

* Installer et gérer les softwares
* Maintenir une structure standard
* Le contrôle de version
* Etre idempotent

### Server Templating


* Fait pour déployer des softwares et dépendances pré-installées
* Les exemples les plus courants de tels templates sont des VM ou des images Docker.
* Ce genre d'infrastructure est immutable. Si on veut la changer, il faut changer le template.

### Provisionnement

Premet de déployer des ressources d'infrastructure immutable, comme des serveurs, des bases de données, des composantes réseaux, etc.

La plupart de ses solutions sont multi-fournisseurs (AWS, GCP, Azure, etc)

## Terraform

[Installation](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

### Langage HCL

Les fichier terraform sont des fichiers avec l'extension `.tf` et sont écrits en **HashiCorp Configuration Language** (HCL).

Un fichier terraform écrit en HCL est composé d'une suite d'instructions ayant la syntaxe suivante.

```terraform
<resource> <paramêtres> {
  clé1 = valeur1
  clé2 = valeur2
}
```

Par exemple, si l'on souhaite écrire un fichier local grâce à terraform, on le fait de la manière suivante.


```terraform
resource "local_file" "hello" {
  filename = "hello.txt"
  content  = "hello from tf !"
}
```


```terraform
block_name "resource_type" "resource_name" {
    # arguments specifics to the resource type
    filename = "hello.txt"
    content  = "hello from tf !"
}
```

### TF Workflow

1. Rédaction du fichier `.tf`.
2. Initialisation via `terraform init`.
3. Review via `terraform plan`.
4. Application via `terraform apply`.

```sh
❯ terraform init

Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/local...
- Installing hashicorp/local v2.2.3...
- Installed hashicorp/local v2.2.3 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
❯ terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # local_file.hello will be created
  + resource "local_file" "hello" {
      + content              = "hello from tf !"
      + directory_permission = "0777"
      + file_permission      = "0777"
      + filename             = "hello.txt"
      + id                   = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
❯ terraform plan -out local.tfplan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # local_file.hello will be created
  + resource "local_file" "hello" {
      + content              = "hello from tf !"
      + directory_permission = "0777"
      + file_permission      = "0777"
      + filename             = "hello.txt"
      + id                   = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Saved the plan to: local.tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "local.tfplan"
❯ terraform apply "local.tfplan"
local_file.hello: Creating...
local_file.hello: Creation complete after 0s [id=9e87d6c4005d4f68dee4a2ab989e243fd56f7a5f]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
❯ terraform show
# local_file.hello:
resource "local_file" "hello" {
    content              = "hello from tf !"
    directory_permission = "0777"
    file_permission      = "0777"
    filename             = "hello.txt"
    id                   = "9e87d6c4005d4f68dee4a2ab989e243fd56f7a5f"
}
```
