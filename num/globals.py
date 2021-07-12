
# globals
# -------------------------------------------------------------------------------------------------------------------------------


def get_env_config(var, file):
    '''
    El formato para el archivo por cada linea debe ser
    CONSTANTE = "Variable"
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
        return -1, print(f'Unexpected error')
