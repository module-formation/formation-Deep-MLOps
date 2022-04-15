# Annex : Automatic HTTPS with Azure Container Instances (ACI)

https://itnext.io/automatic-https-with-azure-container-instances-aci-4c4c8b03e8c9

Automatic HTTPS with Azure Container Instances (ACI)

Let’s assume you want to deploy a simple containerized application or service to the Azure cloud. Additionally, your service needs to be reachable publicly via HTTPS. This technical article shows you how to achieve this goal.
Azure Container Instances

According to the architecture guide Choosing an Azure compute service you’ve got several options to deploy your containerized service, one of them is Azure Container Instances (ACI):

    Container Instances: The fastest and simplest way to run a container in Azure, without having to provision any virtual machines and without having to adopt a higher-level service.

Simple also means that you don’t get all the options and features of a full-blown orchestration solution, such as Azure Kubernetes Service (AKS). ACI provides features like sidecars and persistent volumes. With ACI, however, you have to live with a downtime when upgrading your deployment.

And you have to set up TLS manually. There is a guide, Enable TLS with a sidecar container, which tells you how to set up HTTPS with Nginx and a self-signed certificate. Ugh. The guide also mentions Caddy as an alternate TLS provider but doesn’t provide more details.
Caddy

    Caddy 2 is a powerful, enterprise-ready, open source web server with automatic HTTPS written in Go.

Ok, sounds nice! Automatic HTTPS sounds really intriguing. What does it mean? “Caddy obtains and renews TLS certificates for your sites automatically. It even staples OCSP responses.” Wow! But how is this done?

“Caddy serves public DNS names over HTTPS using certificates from a public ACME CA such as Let’s Encrypt”. This means, you just need a public DNS record and Caddy needs to be reachable via ports 80 and 443. Nice!
Setup Instructions

So let’s combine ACI and Caddy to achieve our goal. I’ll use Terraform to set up the infrastructure in Azure. We’ll start with a new Terraform file and configure it with the Azure Provider (azurerm) and a local value for the Azure region:

```HCL
terraform {
  required_version = ">= 0.14, < 0.15"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.0"
    }
  }
}

provider "azurerm" {
  features {}
}

locals {
  location = "West Europe"
}
```

Next, we are going to define three resources so that we can provide persistent storage for Caddy:

```tf
resource "azurerm_resource_group" "aci_caddy" {
  name     = "aci_caddy"
  location = local.location
}

resource "azurerm_storage_account" "aci_caddy" {
  name                      = "acicaddy"
  resource_group_name       = azurerm_resource_group.aci_caddy.name
  location                  = azurerm_resource_group.aci_caddy.location
  account_tier              = "Standard"
  account_replication_type  = "LRS"
  enable_https_traffic_only = true
}

resource "azurerm_storage_share" "aci_caddy" {
  name                 = "aci-caddy-data"
  storage_account_name = azurerm_storage_account.aci_caddy.name
}
```

This is needed so that the certificate from Let’s Encrypt is not lost between deployments. If you deploy frequently and Caddy can’t remember the previous certificate, you will probably run into a rate limit of Let’s Encrypt which means you won’t be able to get any new certificate for your domain for some time.

Now we’re ready to define our main resource, the container instance (called container group in Terraform):

```
resource "azurerm_container_group" "aci_caddy" {
  resource_group_name = "aci_caddy"
  location            = local.location
  name                = "aci_caddy"
  os_type             = "Linux"
  dns_name_label      = "aci-caddy"
  ip_address_type     = "public"

  container {
    name   = "app"
    image  = "nginxinc/nginx-unprivileged"
    cpu    = "0.5"
    memory = "0.5"
  }

  container {
    name   = "caddy"
    image  = "caddy"
    cpu    = "0.5"
    memory = "0.5"

    ports {
      port     = 443
      protocol = "TCP"
    }

    ports {
      port     = 80
      protocol = "TCP"
    }

    volume {
      name                 = "aci-caddy-data"
      mount_path           = "/data"
      storage_account_name = azurerm_storage_account.aci_caddy.name
      storage_account_key  = azurerm_storage_account.aci_caddy.primary_access_key
      share_name           = azurerm_storage_share.aci_caddy.name
    }

    commands = ["caddy", "reverse-proxy", "--from", "aci-caddy.westeurope.azurecontainer.io", "--to", "localhost:8080"]
  }
}

output "url" {
  value = "https://${azurerm_container_group.aci_caddy.fqdn}"
  description = "URL"
}
```

Note that we define two containers. On line 9, we use an Nginx unprivileged image which serves as a surrogate for our real service and listens on port 8080.

On line 16, we define another container (sidecar) which contains our Caddy server. As mentioned previously, Caddy needs ports 80 and 443, so we assign those ports. Also, note that we are using a public IP (line 7) and we define a DNS subdomain (line 6).

Lines 32–38 contain the configuration for the shared volume which reference the storage resources we defined before. Caddy stores its data in the /data directory.

Line 40 contains all the magic to start Caddy. We tell it to act as a reverse proxy for our main service, the address to listen to (from parameter), and the forwarding address for our main service (to parameter), which is localhost:8080. That’s it. Caddy can be started with a one-liner and requires almost no configuration! (This is a concept I call zero config which I will treat in a future article.)

Finally, we print the address of our new service which should be accessible via HTTPS with a valid certificate from Let’s Encrypt.

Let’s log in with the Azure CLI (az), and let’s initialize and apply our new Terraform config:

```Shell
❯ az login -o none
The default web browser has been opened at https://login.microsoftonline.com/common/oauth2/authorize. Please continue the login in the web browser. If no web browser is available or if the web browser fails to open, use device code flow with `az login --use-device-code`.
You have logged in. Now let us find all the subscriptions to which you have access...

❯ terraform init

Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/azurerm versions matching "~> 2.0"...
- Installing hashicorp/azurerm v2.45.1...
- Installed hashicorp/azurerm v2.45.1 (signed by HashiCorp)

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

❯ terraform apply

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # azurerm_container_group.aci_caddy will be created
  (...)

  # azurerm_resource_group.aci_caddy will be created
  (...)

  # azurerm_storage_account.aci_caddy will be created
  (...)

  # azurerm_storage_share.aci_caddy will be created
  (...)

Plan: 4 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + url = (known after apply)

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

(...)

Apply complete! Resources: 4 added, 0 changed, 0 destroyed.

Outputs:

url = "https://aci-caddy.westeurope.azurecontainer.io"
```

Nice work! Let’s test our service in a browser by invoking the URL provided in the output. If the page displays “Welcome to nginx!” and the browser doesn’t complain about invalid certificates then we achieved our goal.

There are some restrictions you need to be aware of: First, for each service you have to spin up a separate Caddy service. This consumes extra resources. Second, you also have to make sure that your service doesn’t listen on ports 80 and 443 as those are reserved for Caddy. Third, Caddy requires a public IP.
Conclusion

In this technical guide, I demonstrated how you can overcome one of the shortcomings of ACI when it comes to managing TLS certificates for an HTTPS connection.

