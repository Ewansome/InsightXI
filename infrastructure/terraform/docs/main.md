# main.tf

This file configures the Terraform provider and sets up the foundation for all other resources.

## Code Breakdown

```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

**What:** Declares the required Terraform version and AWS provider.

**Why:**
- `required_version = ">= 1.0"` ensures anyone running this code has Terraform 1.0 or higher, preventing compatibility issues with older syntax
- `source = "hashicorp/aws"` tells Terraform to download the official AWS provider from the Terraform Registry
- `version = "~> 5.0"` means "any version >= 5.0 but < 6.0" - this allows patch updates but prevents breaking changes from major versions

---

```hcl
provider "aws" {
  region = var.aws_region
}
```

**What:** Configures the AWS provider with the region from variables.

**Why:**
- Using a variable instead of hardcoding makes the infrastructure reusable across regions
- The provider block tells Terraform how to authenticate with AWS (it uses your AWS CLI credentials by default)

---

```hcl
data "aws_caller_identity" "current" {}
```

**What:** A data source that fetches information about the currently authenticated AWS account.

**Why:**
- This gives us access to the AWS account ID without hardcoding it
- Useful for constructing ARNs (Amazon Resource Names) that include the account ID
- Helps verify you're deploying to the correct account
