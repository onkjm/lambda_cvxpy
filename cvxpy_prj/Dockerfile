# FROM public.ecr.aws/lambda/python:3.10

# ubuntu:latest base
FROM coinor/cylp

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# AWS提供の言語ごとのRuntime Interface Client(RIC)を組み込む
# https://qiita.com/a_b_/items/337c4afee2e330efefe1
RUN mkdir /function && pip3 install --target /function awslambdaric
  
# Copy function code
COPY app.py /function/
COPY cvxpy_prj.py /function/

WORKDIR /function

ENTRYPOINT [ "/usr/bin/python3", "-m", "awslambdaric" ]

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ] 