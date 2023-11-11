from lxml import etree
import re

# Parse the XML file
tree = etree.parse(file_path)

# Retrieve the namespaces from the XML file to find the OWL classes correctly
namespaces = tree.getroot().nsmap

# In some cases, the 'None' key is used for the default namespace. If present, it needs to be removed.
if None in namespaces:
    namespaces['default'] = namespaces.pop(None)

# Define a function to extract all OWL classes from the XML content
def extract_owl_classes(tree, namespaces):
    # List to store the names of the OWL classes
    owl_classes = []
    
    # Extract all OWL class elements
    for _, element in etree.iterwalk(tree, events=("end",), tag="{http://www.w3.org/2002/07/owl#}Class"):
        # Some classes may use rdf:about or rdf:ID for the class name
        class_name = element.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about")
        if not class_name:
            class_name = element.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}ID")
        
        # Extract the local name (i.e., without the namespace URI)
        if class_name:
            local_name = re.sub(r'^.*(#|/)', '', class_name)
            owl_classes.append(local_name)
    
    return owl_classes

# Extract OWL classes
owl_classes_list = extract_owl_classes(tree, namespaces)
owl_classes_list[:10]  # Display the first 10 classes for brevity


