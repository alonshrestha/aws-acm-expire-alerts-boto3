import boto3
from datetime import date

todayDate = date.today()

sts_client = boto3.client('sts')  # Creating an STS client for AWS AssumeRole functionality


def getTable(accountName, acmArn, domainName, acmType, inUse, acmAge, region):
    """
    Constructs an HTML table with AWS ACM certificate details.

    Args:
    - accountName (str): AWS account name.
    - acmArn (str): ACM certificate ARN.
    - domainName (str): Domain name associated with the certificate.
    - acmType (str): Type of ACM certificate.
    - inUse (bool): Whether the certificate is in use.
    - acmAge (str): Age of the certificate in days.
    - region (str): AWS region where the certificate is located.

    Returns:
    - message (str): HTML formatted table with certificate details.
    """
    acmTable = ['<html>'
                '<head><style>table {font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;border-collapse: '
                'collapse; }'
                'td,th{'
                'border:1px solid #ddd;'
                'padding:8px;'
                'width:1%;'
                '}'
                '</style>''</head>', '<table>'
                                     '<tr>'
                                     '<td style="border:5px solid white;" colspan="8"> </td>'
                                     '</tr>'
                                     '<tr>'
                                     '<th style="background-color:#FFBB33" colspan="8">'"Certificate Details"'</th>'
                                     '</tr>'
                                     '<tr>'
                                     '<td> <strong> AWS Account </strong> </td>'
                                     '<td> <strong> Certificate Arn </strong> </td>'
                                     '<td> <strong> Domain Name </strong> </td>'
                                     '<td> <strong> Type </strong> </td>'
                                     '<td> <strong> In Use </strong> </td>'
                                     '<td> <strong> Age </strong> </td>'
                                     '<td> <strong> Region </strong> </td>'
                                     '</tr>',
                                     '<tr>'
                                     '<td>' + accountName + '</td>'
                                     '<td>' + acmArn + '</td>'
                                     '<td>' + str(domainName) + '</td>'
                                     '<td>' + acmType + '</td>'
                                     '<td>' + str(inUse) + '</td>'
                                     '<td>' + acmAge + '</td>'
                                     '<td>' + region + '</td>'
                                     '</tr>'
                                     '</table>']

    acmTable.append('<h4> <i>Automated &#128640; </i></h4>')
    message = (''.join(acmTable))
    return message


def sendEmail(subject, message):
    """
    Sends an email using AWS SES service.

    Args:
    - subject (str): Subject line of the email.
    - message (str): HTML formatted content of the email.

    Returns:
    - None
    """
    toEmail = ['dev@example.com']
    try:
        destination = {
            'ToAddresses': toEmail,
        }
        print(f"Email: '{subject}' Initiated To: {toEmail}")
        ses = boto3.client('ses')
        response = ses.send_email(
            Source='IP Admin <admin@example.com>',
            Destination=destination,
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Html': {
                        'Data': message,
                        'Charset': 'UTF-8',

                    }

                }

            }
        )
        print("Email Success!!")
    except Exception as e:
        print(f"Email Failed!! Error: {e}")


def getSession(iamRoleArn, service, serviceType, region):
    """
    Creates and returns an AWS boto3 session for the specified service and region using AssumeRole.

    Args:
    - iamRoleArn (str): AWS IAM Role Arn.
    - service (str): AWS service name (e.g., 'acm', 'ses').
    - serviceType (str): Type of AWS service ('client' or 'resource').
    - region (str): AWS region where the service session is required.

    Returns:
    - session: Boto3 session object for the specified service and region.
    """
    session = ""
    sts_response = sts_client.assume_role(
        RoleArn=iamRoleArn,
        RoleSessionName='sts-acm-expire-alerts',
    )
    if serviceType == 'client':
        # Creating boto3 client session with temporary credentials
        session = boto3.client(service, aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
                               aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
                               aws_session_token=sts_response['Credentials'][
                                   'SessionToken'],
                               region_name=region,
                               )
    elif serviceType == 'resource':
        # Creating boto3 resource session with temporary credentials
        session = boto3.resource(service, aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
                                 aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
                                 aws_session_token=sts_response['Credentials'][
                                     'SessionToken'],
                                 region_name=region,
                                 )
    return session  # Returning boto3 session object for the specified service and region
