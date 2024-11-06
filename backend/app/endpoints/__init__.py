from .healhCheck import apiRouter as healhCheck
from .lab1 import apiRouter as lab1
from .lab2 import apiRouter as lab2
from .lab3 import apiRouter as lab3
from .lab3_search import apiRouter as lab3_search
from .lab4 import apiRouter as lab4
from .lab5 import apiRouter as lab5
from .test_mongo import apiRouter as test_mongo

listOfRoutes = [
    healhCheck,
    lab1,
    lab2,
    lab3,
    lab3_search,
    lab4,
    lab5,
    test_mongo,
]

__all__ = [
    "listOfRoutes",
]
