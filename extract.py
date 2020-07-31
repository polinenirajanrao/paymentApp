import boto3
docName = 'Two_Column_Two_Para.PNG'
with open(docName, 'rb') as file :
    imageBytes = bytearray(file.read())
textract = boto3.client(service_name = 'textract', region_name = 'us-east-1')
### Calling Amazon Textract
response = textract.detect_document_text(Document = {'Bytes' : imageBytes})
### Printing text
for term in response["Blocks"]:
    if term["BlockType"] == "LINE":
        print(term["Text"])
## Detecting columns and printing lines
columns = []
lines = []

for term in response["Blocks"]:
    if term["BlockType"] == "LINE":
        column_found = False
        for index, column in enumerate(columns):
            bbox_left = term["Geometry"]["BoundingBox"]["Left"]
            bbox_right = term["Geometry"]["BoundingBox"]["Left"] + term["Geometry"]["BoundingBox"]["Width"]
            bbox_centre = term["Geometry"]["BoundingBox"]["Left"] + term["Geometry"]["BoundingBox"]["Width"]/2
            column_centre = column["left"] + column['right']/2
            
            if (bbox_centre > column['left'] and bbox_centre < column['right']) or \
            (column_centre > bbox_left and column_centre < bbox_right):
                lines.append([index, term["Text"]])
                column_found = True
                break
        if not column_found:
            columns.append({'left' : term["Geometry"]["BoundingBox"]["Left"], 
                           'right' : term["Geometry"]["BoundingBox"]["Left"] + term["Geometry"]["BoundingBox"]["Width"]})
            lines.append([len(columns)-1, term["Text"]])
lines.sort(key=lambda x : x[0])
for line in lines:
    print(line[1])