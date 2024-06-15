### AWS ACM Expiration Alert Automation Scripts Using Python Boto3

### Description:
This Python script automates the monitoring of AWS ACM (Amazon Certificate Manager) certificates across multiple AWS accounts. It checks the expiration dates of ACM certificates and sends email alerts when certificates are nearing expiration (less than 30 days) using AWS SES. The script uses AWS IAM roles with STS (Security Token Service) AssumeRole for cross-account access, ensuring security and isolation between AWS accounts.

### Features:
- **Multi-Account Support:** Monitor ACM certificates across multiple AWS accounts.
- **Automated Alerts:** Send email alerts using AWS SES when ACM certificates are 30, 20, and 10 days away from expiration.
- **Security:** Uses STS AssumeRole for secure access to AWS resources across accounts.
- **Customizable:** Easily configurable through `config.py` to specify AWS account name and IAM Roles and SES (Simple Email Service) email through `library.py` recipients.
- **MIT License:** Open-source under the MIT License, allowing for modification and distribution.

### Python Version:
Compatible with Python 3.12

### Installation:
1. Clone the repository:
   ```
   git clone https://github.com/alonshrestha/aws-acm-expire-alerts-boto3.git
   ```
2. Install dependencies:
   ```
   pip install boto3  # If not already installed
   ```

### Configuration:
- Edit `config.py` to specify:
  - `accountList`: List of AWS account names to monitor.
  - `accountConfig`: Dictionary mapping AWS account names to their respective IAM role ARNs.
- Ensure the AWS IAM roles used for AssumeRole have appropriate permissions:
  - **ACM Access:** Read-only access.
  - **SES Access:** Ensure the AWS account where the script runs has SES access to send emails.

### Usage:
- Run `main.py` to initiate ACM certificate checks and email alerts:
  ```
  python main.py
  ```

### Example `config.py`:
```python
# List of AWS account names
accountList = ['AWS-Account1', 'AWS-Account2']

# Configuration dictionary mapping account names to their respective IAM role ARNs
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
```

### License:
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

### Author:
- **Alon Shrestha**
- GitHub: [Profile Link](https://github.com/alonshrestha)

## Usage Disclaimer and Considerations

- This application is a basic example and may require modifications based on specific use cases or security considerations.
- Refer to the [boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for more information.
- **Important**: Thoroughly test before deploying in a production environment to ensure it meets specific requirements without unintended consequences.

---