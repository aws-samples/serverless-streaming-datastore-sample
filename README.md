## serverless-streaming-datastore-sample
This project is a demonstration that allows you to utilize the following blog post:

[Build an end-to-end serverless streaming pipeline with Apache Kafka on Amazon MSK using Python](https://aws.amazon.com/blogs/big-data/build-an-end-to-end-serverless-streaming-pipeline-with-apache-kafka-on-amazon-msk-using-python/)

It has been adapted to make the concepts from the blog post readily available as a demo.

## How It Works

Integration between MSK and DynamoDB uses a Lambda function to consume records from MSK and write them to DynamoDB. 

Lambda internally polls for new messages from MSK and then synchronously invokes the target Lambda function.

The Lambda function’s event payload contains batches of messages from MSK. For the integration between MSK and DynamoDB, the Lambda function writes these messages to DynamoDB. 

Example Integration

The steps below show how to set up a sample integration between MSK and Amazon DynamoDB. 

The example represents data generated by IoT devices and ingested into MSK. As data is ingested into Amazon MSK, 

it can be integrated with analytics services or third-party tools compatible with Apache Kafka, enabling various analytics use cases.

Integrating DynamoDB as well provides key value lookup of individual device records.

As an example, a Python script writes IoT sensor data to MSK. Subsequently, a Lambda function writes items with the partition key "deviceid" to DynamoDB.

The provided CloudFormation template will create the following resources: An Amazon S3 bucket, a Amazon VPC, a MSK cluster, and an AWS CloudShellfor testing data operations.

To generate test data, create an MSK topic, and create a DynamoDB table, you can use Session Manager from the management console to log into the CloudShell's operating system and execute Python scripts.

After running the CloudFormation template, you can finish building this architecture by performing the following operations:

### Step 1. 

Run the CloudFormation template “S3bucket.yaml” to create an S3 bucket. For any subsequent scripts or operations, please execute them in the same region.

Enter "ForMSKTestS3" as the CloudFormation stack name.

After completion, note down the S3 bucket name output under "Outputs". You will need it in Step 3. 
 
### Step 2. 

Upload the downloaded ZIP file “fromMSK.zip” to the S3 bucket you just created.
 
### Step 3.  

Run the CloudFormation template “VPC.yaml” to create a VPC, MSK cluster, and Lambda function.

On the parameter input screen, enter the S3 bucket name you created in Step 1 where it asks for the S3 bucket.

Set the CloudFormation stack name to "ForMSKTestVPC".
 
### Step 4. 

Prepare the environment for running Python scripts on the CloudShell.

You can use CloudShell on the AWS Management Console. If you need more information on using CloudShell, please refer to this document. After starting CloudShell, create a CloudShell that belongs 

to the VPC you have just created in order to connect to the MSK Cluster. At this time, CloudShell should be created on a Private subnet.

Name can be set to any name. An example is MSK-VPC.

For VPC, select MSKTest.

For Subnet, select MSKTest Private Subnet (AZ1)

For SecurityGroup select ForMSKSecurityGroup






 
 


Once the CloudShell belonging to the Private Subnet has started, execute the following commandspip install boto3 kafka-python aws-msk-iam-sasl-signer-python

Step 5. Download Python scripts from the S3 bucket.
aws s3 cp s3://[YOUR-BUCKET-NAME]/pythonScripts.zip ./.
unzip pythonScripts.zip.


Step 6. Set the environment variables for the broker URL and region value in the Python scripts.
Check the MSK cluster broker endpoint in the management console.
 

 
Set the environment variables on the CloudShell.
If you are using the Oregon region (us-west-2):
export AWS_REGION="us-west-2".
export MSK_BROKER="boot-YOURMSKCLUSTER.c3.kafka-serverless.ap-southeast-1.amazonaws.com:9098".
Run the Python scripts.
Create an MSK topic:
python ./createTopic.py.
Create a DynamoDB table:
python ./createTable.py.
Write test data to the MSK topic:
python ./kafkaDataGen.py.

Step 7. Check the CloudWatch metrics for the created MSK, Lambda, and DynamoDB resources, and verify the data stored in the device_status table using the DynamoDB Data Explorer to ensure all processes executed correctly. If each process is executed without error, the test data written from CloudShell to MSK is also written to DynamoDB and can be checked.
 

Step 8. When you're done with the sample, delete the resources created in this tutorial.
Delete the two CloudFormation stacks: "ForMSKTestS3" and "ForMSKTestVPC". If the stack deletion completes successfully, all resources will be deleted.

Next Steps

If you created resources while following along with this sample, please remember to clean them up to avoid any unexpected charges.


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

