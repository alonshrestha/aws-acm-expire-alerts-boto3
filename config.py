# List of AWS account names
accountList = ['AWS-Account1', 'AWS-Account2']

# Configuration dictionary mapping account names to their respective IDs
accountConfig = {
    "AWS-Account1":
        {
            "iamRole": "arn:aws:iam::12345678910:role/role_acm_expire_alerts"
        },
    "AWS-Account2":
        {
            "iamRole": "arn:aws:iam::10987654321:role/role_acm_expire_alerts"
        }
}
