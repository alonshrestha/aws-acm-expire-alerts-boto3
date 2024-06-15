# Author: Alon Shrestha
# Date: 2022-03-12
# Description: Python script to check AWS ACM certificates for expiration and send alerts.


from datetime import date
import config
import library

todayDay = date.today()


def mainHandler():
    """
    Main function to check AWS ACM certificates across multiple accounts and regions,
    and send email alerts based on their expiration dates.

    Returns:
    - None
    """
    for accountName in config.accountList:
        assumeRoleArn = config.accountConfig[accountName]['iamRole']
        regionsList = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']

        for region in regionsList:
            # Establish ACM client session for the account and region
            acmClient = library.getSession(assumeRoleArn, 'acm', 'client', region)
            print(f"Checking in Account: {accountName}, Region: {region}")

            # Retrieve list of issued certificates in ACM
            acmList = acmClient.list_certificates(CertificateStatuses=['ISSUED'], MaxItems=1000)
            for acmMetadata in acmList['CertificateSummaryList']:
                acmAge = str((acmMetadata['NotAfter'].date() - todayDay).days)
                print(acmMetadata['CertificateArn'], acmMetadata['DomainName'], acmMetadata['Type'],
                      acmMetadata['InUse'],
                      acmAge)

                # Send alert emails based on remaining days until expiration
                if int(acmAge) == 30:
                    subject = f"ALERT: Certificate {acmMetadata['DomainName']} Expiration |  {acmAge}  Days"
                    message = library.getTable(accountName, acmMetadata['CertificateArn'], acmMetadata['DomainName'],
                                               acmMetadata['Type'], acmMetadata['InUse'], acmAge, region)
                    library.sendEmail(subject, message)
                elif int(acmAge) == 20:
                    subject = f"ALERT: Certificate {acmMetadata['DomainName']} Expiration |  {acmAge}  Days"
                    message = library.getTable(accountName, acmMetadata['CertificateArn'], acmMetadata['DomainName'],
                                               acmMetadata['Type'], acmMetadata['InUse'], acmAge, region)
                    library.sendEmail(subject, message)
                elif int(acmAge) <= 10:
                    subject = f"ALERT: Certificate {acmMetadata['DomainName']} Expiration |  {acmAge}  Days"
                    message = library.getTable(accountName, acmMetadata['CertificateArn'], acmMetadata['DomainName'],
                                               acmMetadata['Type'], acmMetadata['InUse'], acmAge, region)
                    library.sendEmail(subject, message)


if __name__ == "__main__":
    mainHandler()
