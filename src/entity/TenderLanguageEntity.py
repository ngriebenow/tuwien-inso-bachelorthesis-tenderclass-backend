class TenderLanguageEntity:
    """
    This class holds the title and description of one tender for a certain language.
    """

    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link
