# Name: Bar Olivkovis 
# Linkdin: https://www.linkedin.com/in/bar-olivkovis-35a6561bb/
# Beta version stay tuned ;]

import json
import subprocess

#List of regions
regions = {
    1: "us-east-1",
    2: "us-east-2",
    3: "us-west-1",
    4: "us-west-2",
    5: "ca-central-1",
    6: "eu-west-1",
    7: "eu-central-1",
    8: "eu-west-2",
    9: "eu-west-3",
    10: "eu-north-1",
    11: "ap-northeast-1",
    12: "ap-northeast-2",
    13: "ap-southeast-1",
    14: "ap-southeast-2",
    15: "ap-south-1",
    16: "sa-east-1",
    17: "us-gov-west-1",
    18: "us-gov-east-1"
}

# List of OS
OS_FREE = {
    1: "Amazon Linux 2023 AMI 2023.0.20230614.0 x86_64 HVM kernel-6.1",
    2: "Amazon Linux 2 Kernel 5.10 AMI 2.0.20230612.0 x86_64 HVM gp2",
    3: ".NET Core 6, Mono 6.12, PowerShell 7, and MATE DE pre-installed to run your .NET applications on Amazon Linux 2 with Long Term Support (LTS).",
    4: "Canonical, Ubuntu, 22.04 LTS, amd64 jammy image build on 2023-05-16",
    5: "Canonical, Ubuntu, 20.04 LTS, amd64 focal image build on 2023-05-17",
    6: "Microsoft Windows Server 2022 Full Locale English AMI provided by Amazon",
    7: "Provided by Red Hat, Inc.",
    8: "Input your search",
}

# colors
Colors = {
    'Red': '\033[91m',
    'Pink': '\033[95m',
    'Green': '\033[92m',
    'Yellow': '\033[93m',
    'RESET': '\033[0m',
    'Red': '\033[91m'
}


# GET os and Region from the aws cli command and filter the result
def get_ami_id(os, region, Colors):
    if os == "Input your search":
        os = input("Enter your OS: ")

# Command of the AWS CLI 
    command = [
        "aws",
        "ec2",
        "describe-images",
        "--filters",
        f"Name=description,Values={os}",
        "--region",
        region,
        "--query",
        "Images[].[Architecture,CreationDate,ImageLocation,ImageId,PlatformDetails]",
        "--output",
        "json",
    ]
    # Print the input Command 
    print(f"{Colors['Green']}Command:\n{Colors['Yellow']}{' '.join(command)}{Colors['RESET']}")
    result = subprocess.check_output(command, text=True)


    # Print the result of the command
    print(f"\n{Colors['Green']}Command output:{Colors['RESET']}")

    
    # change the output of ami_info and print it as pink 
    ami_info = process_output(result)
    if ami_info:
        print(f"{Colors['Pink']}{ami_info['Architecture']}{Colors['RESET']}")
        print(f"{Colors['Pink']}{ami_info['CreationDate']}{Colors['RESET']}")
        print(f"{Colors['Pink']}{ami_info['ImageLocation']}{Colors['RESET']}")
        print(f"{Colors['Pink']}{ami_info['ImageId']}{Colors['RESET']}")
        print(f"{Colors['Pink']}{ami_info['PlatformDetails']}{Colors['RESET']}")  
 
            
# Process the command output 
def process_output(output):
    try:
        images = json.loads(output)
        if images:
            image_info = images[0]
            ami_info = {
                "Architecture": f'Architecture: "{image_info[0]}"',
                "CreationDate": f'CreationDate: "{image_info[1]}"',
                "ImageLocation": f'ImageLocation: "{image_info[2]}"',
                "ImageId": f'ImageId: "{image_info[3]}"',
                "PlatformDetails": f'PlatformDetails: "{image_info[4]}"',
            }
            return ami_info
        # when No AMI found will print No AMI with red color 
        else:
            raise IndexError
    except IndexError:
        print(f"{Colors['Red']}{'No AMI information Found!'}{Colors['RESET']}")
        
# User InterFace
def main():
    print("Available OS:")
    for num, os_option in OS_FREE.items():
        print(f"{num}. {os_option}")

    os_num = int(input("Enter the OS number: "))

    if os_num in OS_FREE:
        os = OS_FREE[os_num]
    else:
        print("Invalid OS number.")
        return

    print("Available regions:")
    for num, region in regions.items():
        print(f"{num}. {region}")

    region_num = int(input("Enter the region number: "))

# if the number in region is correct it will run if not will print Invalid
    if region_num in regions:
        region = regions[region_num]
        ami_id = get_ami_id(os, region, Colors)
    else:
        print("Invalid region number.")

# executed when the script run directly 
if __name__ == "__main__":
     main()
