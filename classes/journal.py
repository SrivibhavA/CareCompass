class Journal:
    def __init__(self, text, feeling_score):
        self.text = text
        self.feeling_score = feeling_score
    
    def save(self):
        with open("output.txt", "a") as file:
            # Write the variables to the file
            file.write(f"Text: {self.text}; ")
            file.write(f"Feeling Score: {self.feeling_score}\n")