
# globals
# -------------------------------------------------------------------------------------------------------------------------------


def get_env_config(var, file):
    '''
    El formato para el archivo por cada linea debe ser
    CONSTANTE1 = "Variable1"
    CONSTANTE2 = "Variable2"
    '''
    try:
        archivo = open(file)
        if archivo:
            for line in archivo:
                if str(line[0:len(var)]) == str(var):
                    response = line.split("\"")
                    return response[1]
                else:
                    response = f'Can\'t find {var}'
            return -1, response
        archivo.close()
    except FileNotFoundError:
        return -1, print(f'{FileNotFoundError} Can\'t open {file}')
    except:
        return -1, print(f'Unexpected error from get_env_config()')


def make_sql_querry(connectionName, sql, data=None, fetchType=None):
    """

    Definir fetchType como "one" o "all" para lograr retorno

    """
    # Falta manejo de errores
    try:
        cursor = connectionName.connection.cursor()
        if data is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, data)

        if fetchType == "all":
            toReturn = cursor.fetchall()
            connectionName.connection.commit()
            cursor.close()
            return toReturn
        elif fetchType == "one":
            toReturn = cursor.fetchone()
            connectionName.connection.commit()
            cursor.close()
            return toReturn
        connectionName.connection.commit()
        cursor.close()
    except TypeError:
        return print('TypeError')
    except:
        return print(f'error en make_sql_querry con sql:{sql}{data}')
