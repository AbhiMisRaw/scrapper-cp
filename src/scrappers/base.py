from abc import abstractmethod

class BaseScrapper():

    @abstractmethod
    def fetch_jobs():
        pass