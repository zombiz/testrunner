import io
import random
import string
import sys
import requests
import datetime
import collections
import constants

class ValueGenerator(object):

    def rand_bool(self):
        return random.choice([True, False])

    def rand_null(self):
        return random.choice(["NULL", "null", "Null", None])

    def rand_reserved(self):
        return random.choice(constants.niql_reserved_keywords)

    def rand_string(self, len_min=0, len_max=10):
        self.len_min = int(len_min)
        self.len_max = int(len_max)
        return ''.join(random.choice(
            string.ascii_letters * 40 + \
            string.digits * 10 + \
            string.whitespace * 40 + \
            string.punctuation * 10) for _ in xrange(random.randint(self.len_min, self.len_max)))

    def rand_int(self, negative=False):
        if bool(negative):
            return -1 * random.randint(1, sys.maxsize)
        else:
            return random.randint(0, sys.maxsize)

    def rand_float(self, negative=False):
        if bool(negative):
            return -1 * random.uniform(sys.float_info.min, sys.float_info.max)
        else:
            return random.uniform(sys.float_info.min, sys.float_info.max)

    def array_strings(self, len_min=0, len_max=10, num_min=0, num_max=10):
        ret = []
        self.num_min = int(num_min)
        self.num_max = int(num_max)
        while self.num_min < self.num_max:
            ret.append(self.rand_string(len_min=len_min, len_max=len_max))
            self.num_min += 1
        return ret

    def array_numbers(self, num_min=0, num_max=10):
        ret = []
        self.num_min = int(num_min)
        self.num_max = int(num_max)
        while self.num_min < self.num_max:
            ret.append(random.choice([self.rand_int(),
                                      self.rand_float(),
                                      self.rand_int(negative=True),
                                      self.rand_int(negative=True),
                                      ]))
            self.num_min += 1
        return ret

    def date_time(self):
        return str(datetime.datetime.now())[:random.randint(10, 19)]

    def sub_doc(self, max_nesting=10, max_items=20):
        try:
            items = random.randint(1, int(max_items))
            sub_doc_dict = collections.defaultdict(dict)
            func_list = [func for func in dir(self) if
                         callable(getattr(self, func)) and not func.startswith("__")]
            # and not func == "sub_doc"]
            while items > 0:
                nesting = random.randint(0, int(max_nesting))
                val = getattr(globals()['ValueGenerator'](), random.choice(func_list))()
                sub_doc_dict[items][nesting] = val
                items -= 1
            return sub_doc_dict
        except:
            # Insurance against maximum recursion depth exceeded exception
            return {{{}}}

    def empty(self, type="string"):
        return constants.empty[type]

    def tabs(self, len_min=1, len_max=10):
        return "\t" * random.randint(int(len_min), int(len_max))

    def string_num(self, len_min=1, len_max=10):
        self.len_min = int(len_min)
        self.len_max = int(len_max)
        return ''.join(random.choice(
            string.digits
           ) for _ in xrange(random.randint(self.len_min, self.len_max)))

    # def rand_name(self):
    #     name = requests.get('http://uinames.com/api')
    #     if not name:
    #         return "Chuck Norris"
    #     return name.json()