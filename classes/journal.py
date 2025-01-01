class Journal:
    def __init__(self, name, text, feeling_score, date):
        self.name = name
        self.text = text
        self.feeling_score = feeling_score
        self.date = date
    
    def save(self):
        with open("data/output.txt", "a") as file:
            # Write the variables to the file
            file.write(f"Name: {self.name};")
            file.write(f"Text: {self.text};")
            file.write(f"Feeling Score: {self.feeling_score};")
            file.write(f"Date: {self.date}\n")