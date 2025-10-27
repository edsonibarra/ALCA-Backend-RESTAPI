def extract_values(df, logger):
    for index, series in df.iterrows():
        # Initialize all keys with empty strings
        row_dict = {
            "departamento": "",
            "ubicacion": "",
            "precio": "",
            "propietario": "",
            "id": "",
            "estatus": "",
            "telefono": "",
            "calle": "",
            "colonia": "",
            "numero": "",
            "ciudad": "",
            "cp": "",
            "cochera": "",
            "baños": "",
            "petfredly": "",
            "patio": "",
            "recamaras": "",
            "centro_de_lavado": "",
            "minisplit": "",
            "caracteristicas": "",
            "servicios_incluidos": "",
            "precio_renta": "",
            "comentarios": "",
            "no_servicio_cfe": "",
            "no_servicio_simas": ""
        }

        logger.info(f'Reading row={index}.')

        try:
            # Copy values from the DataFrame series to the dictionary
            row_dict["departamento"] = series["DEPARTAMENTO"]
            row_dict["ubicacion"] = series["UBICACIÓN"]
            row_dict["precio"] = series["PRECIO"]
            row_dict["propietario"] = series["PROPIETARIO"]
            row_dict["id"] = series["ID"]
            row_dict["estatus"] = series["ESTATUS"]
            row_dict["telefono"] = series["TELEFONO"]
            row_dict["calle"] = series["CALLE"]
            row_dict["colonia"] = series["COLONIA"]
            row_dict["numero"] = series["NUMERO"]
            row_dict["ciudad"] = series["CIUDAD"]
            row_dict["cp"] = series["CP"]
            row_dict["cochera"] = series["COCHERA"]
            row_dict["baños"] = series["BAÑOS"]
            row_dict["petfredly"] = series["PETFREDLY"]
            row_dict["patio"] = series["PATIO"]
            row_dict["recamaras"] = series["RECAMARAS"]
            row_dict["centro_de_lavado"] = series["CENTRO DE LAVADO"]
            row_dict["minisplit"] = series["MINISPLIT"]
            row_dict["caracteristicas"] = series["CARACTERISTICAS"]
            row_dict["servicios_incluidos"] = series["SERVICIOS INCLUIDOS"]
            row_dict["precio_renta"] = series["PRECIO RENTA"]
            row_dict["comentarios"] = series["COMENTARIOS"]
            row_dict["no_servicio_cfe"] = series["NO. SERVICIO CFE"]
            row_dict["no_servicio_simas"] = series["NO. SERVICIO SIMAS"]

            # Yield the dictionary
            yield row_dict

        except Exception as e:
            logger.error(f'There was an error {e}. In line {index}.')