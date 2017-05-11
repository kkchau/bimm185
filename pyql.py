"""
    Store PyMySql executions as functions for ease of use
    Requires the PyMySql package
    @author     Kevin Chau
    @date       9 May 2017
    @notes      TODO need to test sqlSelect
                TODO better exception handling
"""

import pymysql
import getpass


def sqlConnect(hst, usr, database, cur_class=pymysql.cursors.DictCursor):
    """
        Instantiate a connection object to connect to the specified database
    """

    print("Connecting to {} as {}...".format(hst, usr))
    if database:
        print("Using database {}".format(database))

    passwd = getpass.getpass("Input password: ")

    try:
        # create connection to database
        sqlconnection = pymysql.connect(host=hst,
                                        user=usr,
                                        password=str(passwd),
                                        db=database,
                                        cursorclass=cur_class)

    except Exception as e:
        print("CONNECTION ERROR")
        print(e)
        return 1

    return sqlconnection


def sqlInsert(sql_connection, table, col_list, values):
    """
        Execute INSERT command to the given SQL connection.
    """

    try:
        with sql_connection.cursor() as cursor:
            sub_set = ','.join(['%s' for _ in range(len(values))])
            command = ("INSERT INTO "
                       + table
                       + "("
                       + ','.join(col_list)
                       + ") VALUES ("
                       + sub_set + ");")
            cursor.execute(command, values)

        sql_connection.commit()

    except Exception as e:
        print("INSERT ERROR")
        print(e)
        print(command)
        return 1        # error code 1

    return 0            # return code success


def sqlSelect(sql_connection, table, fields=None, where=None, limit=None):
    """
        Execute SELECT command to the given SQL connection with optional
            "where" and "limit" parameters
    """

    # format arguments and command
    f = ','.join(fields) if fields else '*'
    command = "SELECT {} from {}".format(f, table)
    if where:
        command += " WHERE {}".format(where)
    if limit:
        command += " LIMIT {}".format(str(limit))
    command += ";"

    # format result
    result = []

    try:
        with sql_connection.cursor() as cursor:
            cursor.execute(command)

        all_rows = cursor.fetchall()
        if not all_rows:
            return fields, None
        all_fields = list(all_rows[0].keys())

        if fields:
            for row in all_rows:
                result.append([row[field] for field in fields])
        else:
            for row in all_rows:
                result.append([row[field] for field in all_fields])

    except Exception as e:
        print("SELECTION ERROR")
        print(e)
        print(command)
        return 1

    return all_fields, result
