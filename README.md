# lambda_cvxpy
sample of running cvxpy and Coin-or-CBC on AWS Lambda

lambda has some limitation on uploading code.
- 50MB for direct upload from console (with zip file)
- 262MB for upload via S3 (with zip file)
- 10GB for upload via ecr (with container image)

this sample shows how to upload codes via ecr.

first, create docker image.

second, push to aws ecr.

last, set lambda function (does not explain in this README).

it is important to start creating docker image from `coinor/cylp`, 

becayse starting from `public.ecr.aws/lambda/python:3.10` and

only executing line `RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"`

will fail installing Cbc.

## app.py, cvxpy_prj.py, lambda_cvxpy.ipynb
just for createing and testing code.

## cvxpy_prj

`cd` to this folder, and try below.

Build docker image.
```
docker build -t cvxpy_prj .   
```

Login to aws account (change `123456789101` to your aws accaount id).
```
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 123456789101.dkr.ecr.ap-northeast-1.amazonaws.com
```

Create repository on Amazon Elastic Container Repository (ECR)

```
aws ecr create-repository --region ap-northeast-1 --repository-name cvxpy_prj --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
```

Tag image with name same to repo.
```
docker tag  cvxpy_prj:latest 123456789101.dkr.ecr.ap-northeast-1.amazonaws.com/cvxpy_prj:latest
```

Push it to ECR.
```
docker push 123456789101.dkr.ecr.ap-northeast-1.amazonaws.com/cvxpy_prj:latest   
```

Now you can use the container image from lambda funcitons.

## encountered troubles

### ECR permission
`docker push` may fail when permission is not set correctly.

Craete user in IAM and put permissions like below.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:GetServiceBearerToken",
                "ecr:*"
            ],
            "Resource": "*"
        }
    ]
}
```

Create accesskey and secret access key on the user, and set them to `aws configure`.

aws cli: https://aws.amazon.com/jp/cli/

### lambda function arch.
check the docker's arch and set to the same one.
```
docker inspect cvxpy_prj | grep Architecture
```

### lambda function settings
try below when lambda function's test returns error.
- change time out value longer (inisial value is only 3s.)
- change memory value larger (initial value is 128MB.)

### links
- aws ecr(Elastic Container Registry) https://ap-northeast-1.console.aws.amazon.com/ecr/home?region=ap-northeast-1
- Amazon ECR リポジトリへのイメージのアップロード https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/images-create.html#images-upload
- coinor/cylp https://github.com/coin-or-tools/cylp-docker
- cvxpy sample code https://www.cvxpy.org/examples/basic/linear_program.html
- AWS提供でないベースイメージからLambdaを作る https://qiita.com/a_b_/items/337c4afee2e330efefe1
