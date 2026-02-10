# IAM Policy for GitHub Actions CI/CD
# Attach this policy to your github-actions IAM user

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
        Resource = [
          "arn:aws:ecs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:service/${aws_ecs_cluster.main.name}/*",
          "arn:aws:ecs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:task/${aws_ecs_cluster.main.name}/*"
        ]
      },
      {
        Sid    = "ECSDescribeCluster"
        Effect = "Allow"
        Action = [
          "ecs:DescribeClusters"
        ]
        Resource = aws_ecs_cluster.main.arn
      }
    ]
  })
}

# Output the policy ARN so you can attach it to your IAM user
output "github_actions_ecs_policy_arn" {
  description = "ARN of the IAM policy for GitHub Actions ECS deployment"
  value       = aws_iam_policy.github_actions_ecs.arn
}
