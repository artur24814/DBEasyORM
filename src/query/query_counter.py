import time


class QueryCounter:
    __queries = []
    __start_registration = False

    @classmethod
    def start_registration(cls):
        cls.__start_registration = True

    @classmethod
    def end_registration(cls):
        cls.__start_registration = False

    @classmethod
    def register_query(cls, sql):
        if cls.__start_registration:
            cls.__queries.append(sql)

    @classmethod
    def clear_queries(cls):
        cls.__queries = []

    @classmethod
    def get_queries(cls):
        return cls.__queries

    @classmethod
    def get_query_count(cls):
        return len(cls.__queries)

    def __enter__(self):
        self.clear_queries()
        self.start_time = time.time()
        self.start_registration()
        print("Query logging started. Previous logs cleared.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_registration()
        elapsed_time = time.time() - self.start_time
        print(f"Query logging ended. Total queries: {self.get_query_count()}")
        print("Queries: ")
        [print(query) for query in self.get_queries()]
        print(f"Elapsed time: {elapsed_time:.2f} seconds.")
        if exc_type:
            print(f"Error occurred: {exc_value}")
