# iam_cicd.tf

This file creates the IAM policy needed for GitHub Actions to deploy to ECS.

## Why This Exists

The CD pipeline needs to:
1. Push images to ECR (already covered by the ECR policy you attached earlier)
2. Trigger ECS deployments (this new policy)

Without this policy, the `aws ecs update-service` command in the CD pipeline will fail with an access denied error.

## Code Breakdown

### ECS Deployment Policy

```hcl
resource "aws_iam_policy" "github_actions_ecs" {
  name        = "${var.project_name}-${var.environment}-github-actions-ecs"
  description = "Allows GitHub Actions to deploy to ECS"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ECSDeployment"
        Effect = "Allow"
        Action = [
          "ecs:UpdateService",
          "ecs:DescribeServices",
          "ecs:DescribeTasks",
          "ecs:ListTasks"
        ]
        Resource = [...]
      }
    ]
  })
}
```

**Permissions explained:**

| Permission | Purpose |
|------------|---------|
| `ecs:UpdateService` | Trigger new deployments with `--force-new-deployment` |
| `ecs:DescribeServices` | Check service status, wait for stability |
| `ecs:DescribeTasks` | Get task health/status during deployment |
| `ecs:ListTasks` | List running tasks in the service |
| `ecs:DescribeClusters` | Validate cluster exists |

## After Running Terraform Apply

The policy is created but not attached to any user. You need to attach it to your `github-actions` IAM user:

### Option 1: AWS Console
1. Go to IAM → Users → github-actions
2. Click "Add permissions" → "Attach policies directly"
3. Search for `insightxi-dev-github-actions-ecs`
4. Select and attach

### Option 2: AWS CLI
```bash
aws iam attach-user-policy \
  --user-name github-actions \
  --policy-arn $(terraform output -raw github_actions_ecs_policy_arn)
```

## Security Notes

- The policy is scoped to only the ECS cluster and services created by this Terraform
- It cannot affect other ECS clusters in your account
- Consider using OIDC for GitHub Actions instead of long-lived access keys (more secure)
