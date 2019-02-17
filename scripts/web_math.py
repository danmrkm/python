import sys

import requests
import bs4
from bs4 import BeautifulSoup

class Solver(object):
    def __init__(self,url):
        self.url = url
        self.session = requests.Session()

    def solve(selsf):
        r = self.session.get(self.url)
        flag = ""

        while True:
            bs = BeautifulSoup(r.text, "html.parser")

            print "++Stage: ", bs.find(id="stage").string
            flag = bs.find(id="flag")
            if not flag.string == "Flag: -":
                break
            e = bs.select("#expression")[0].findChild('span')
            ans - self.evaluate_expression(e)
            r = self.session.post(self,url,data={'answer':ans})

        print "+Solved!"
        print flag.string

    def get_child_by_class(self,elem,classname):
        return elem.findChild(attr={'class': classname}, reccursive=False)

    def evaluate_expression(self,e):
        if isinstance(e,bs4.element.NavigableString):
            return int(e.string)

        elif isinstance(e,bs4.element.Tag):
            op_type = e['class'][0]
            op1_value = self.evaluate_expression(self.get_child_by_class(e,'op1').contents[0])
            op2_value = self.evaluate_expression(self.get_child_by_class(e,'op2').contents[0])

            if op_type == 'op_add':
                return op1_value + op2_value
            elif op_type == 'op_sub':
                return op1_value - op2_value
            elif op_type == 'op_mul':
                return op1_value * op2_value
            else:
                raise Exception('unknown op_type')

        else:
            raise Exception('unkown elem type')

if __name__ == '__main__':
    url = sys.argv[1]
    s = Solver(url)
    s.solve()
