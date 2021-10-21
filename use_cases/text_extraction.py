class TextExtraction:
    '''
    Extract metadata from documents using Apache Tika
    '''
    def __init__(self, tika_server: str) -> None:
        self.tika_client = tika_server