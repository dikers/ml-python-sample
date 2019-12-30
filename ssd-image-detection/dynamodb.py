# -*-coding:utf8-*-
"""
author:dikers
date: 2019-07-16
"""
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key

TABLE_NAME = "recommend"
ATTR_USER_ID = "userId"
ATTR_ITEM_ID = "itemId"
ATTR_NAME = "name"
ATTR_INFO = "info"


class DecimalEncoder(json.JSONEncoder):
    """
    json 中 整型变量转换
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return int(o)
        super(DecimalEncoder, self).default(o)


def delete_db():
    """
    删除表
    :return:
    """
    print("create db. ")
    client = boto3.client('dynamodb')

    try:
        response = client.delete_table(
            TableName=TABLE_NAME
        )
        print(response)
    except Exception:
        print("db ["+TABLE_NAME+"] is not exist!")
    else:
        print("delete db success!")


def create_db():
    """
    创建表
    :return:
    """
    print("create db. ")
    client = boto3.client('dynamodb')

    table = client.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': ATTR_USER_ID,
                'KeyType': 'HASH'
            },
            {
                'AttributeName': ATTR_ITEM_ID,
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': ATTR_USER_ID,
                'AttributeType': 'N'
            },
            {
                'AttributeName': ATTR_ITEM_ID,
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    # table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
    print(table)


def insert_item(item):
    """
    插入单条数据
    :param item:
    :return:
    """
    print("insert item: ", item)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=item)


def insert_batch_item(item_list):
    """
    批量插入数据
    :param item_list:
    :return:
    """

    print("insert batch item length: ", len(item_list))
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    with table.batch_writer() as batch:
        for item in item_list:
            batch.put_item(
                Item=item
            )


def update_table_capacity(read_capacity_units, write_capacity_units ):
    """
    调整写入容量
    :param read_capacity_units:
    :param write_capacity_units:
    :return:
    """
    print("update table capacity  ")
    client = boto3.client('dynamodb')
    response = client.update_table(

        TableName=TABLE_NAME,
        ProvisionedThroughput={
            'ReadCapacityUnits': read_capacity_units,
            'WriteCapacityUnits': write_capacity_units
        }
    )
    print(response)


def query_item(user_id):
    """
    单条数据
    :param user_id:
    :return:
    """

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    response = table.query(
        KeyConditionExpression=Key(ATTR_USER_ID).eq(user_id)
    )
    # print(response['Items'])
    return response['Items']

if __name__ == "__main__":
    # create_db()
    # insert_item()
    # get_item()

    # result = query_item(1)
    # json_str = ""
    # if result is None:
    #     print(" No results.")
    # else:
    #     print("data length: ", len(result))
    #     json_str = json.dumps(result, cls=DecimalEncoder)
    #
    # print(json_str)

    update_table_capacity(1, 1)