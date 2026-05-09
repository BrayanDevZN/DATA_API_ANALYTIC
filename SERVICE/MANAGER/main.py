import pandas as pd
import numpy as np

from SERVICE.PIPELINE.carts import Data_Carts
from SERVICE.PIPELINE.products import Data_Product
from SERVICE.PIPELINE.users import Data_Users


class Main_Data:

    @staticmethod
    def _response(result):

        if isinstance(result, pd.DataFrame):

            result = result.replace({np.nan: None})

            return (
                result
                .astype(object)
                .where(pd.notnull(result), None)
                .to_dict(orient="records")
            )

        if isinstance(result, dict):

            return {
                key: Main_Data._response(value)
                for key, value in result.items()
            }

        if isinstance(result, list):

            return [
                Main_Data._response(item)
                for item in result
            ]

        if isinstance(result, np.integer):
            return int(result)

        if isinstance(result, np.floating):
            return float(result)

        if isinstance(result, np.ndarray):
            return result.tolist()

        return result

    @staticmethod
    def Carts(search=None):

        if search is not None:
            result = Data_Carts().search(search)

        else:
            result = Data_Carts().execute()

        return Main_Data._response(result)

    @staticmethod
    def Product(search=None):

        if search is not None:
            result = Data_Product().search(search)

        else:
            result = Data_Product().execute()

        return Main_Data._response(result)

    @staticmethod
    def Users(search=None):

        if search is not None:
            result = Data_Users().search(search)

        else:
            result = Data_Users().execute()

        return Main_Data._response(result)