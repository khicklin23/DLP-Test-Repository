# SYNTHETIC TEST DATA. All credentials/hosts below are fake and inert.
# Generated for Netskope One DLP testing of Infrastructure-as-Code files
# with embedded cloud credentials (a very common accidental-commit pattern —
# .tfvars files are often gitignored inconsistently across a team).

aws_access_key_id     = "AKIAJ2XZ7Y6EXAMPLE0"
aws_secret_access_key = "4pQZ9k2vLtR8mNcW1sYbXdEoFgHjKlEXAMPLEKEY"
aws_account_id        = "000000000000"

rds_master_username = "wayfinder_admin"
rds_master_password = "Wf$AdminRDS2026!Prod"
rds_instance_class   = "db.r6g.xlarge"

kms_key_arn = "arn:aws:kms:us-east-2:000000000000:key/0000-0000-0000-0000-000000000000"

vpc_id             = "vpc-0a1b2c3d4e5f6EXMP"
private_subnet_ids = ["subnet-0f1e2d3c4b5a6EXMP", "subnet-0f1e2d3c4b5a7EXMP"]

datadog_api_key = "00000000000000000000000000EXAMPLE"
pagerduty_integration_key = "00000000000000000000000000EXMP"

github_deploy_token = "ghp_9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2aEXMP"

# Synthetic fixture — DLP testing only. Real .tfvars files with secrets
# like this should never be committed; use a remote state backend + a
# secrets manager (AWS Secrets Manager / Vault) instead.
