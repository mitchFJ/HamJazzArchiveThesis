FROM public.ecr.aws/lambda/python:3.12

ADD ./model ${LAMBDA_TASK_ROOT}/model/

COPY requirements.txt .

RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY app.py ${LAMBDA_TASK_ROOT}

COPY Data ${LAMBDA_TASK_ROOT}

CMD [ "app.lambda_handler" ]