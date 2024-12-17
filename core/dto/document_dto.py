class DocumentDTO:
    def __init__(self, id, name, file_extension, type, content, info=None):
        self.id = id
        self.name = name
        self.file_extension = file_extension
        self.type = type
        self.content = content
        self.info = info

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "file_extension": self.file_extension,
            "type": self.type,
            "content": self.content,
            "info": self.info,
        }