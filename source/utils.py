from transformers import BertModel, BertTokenizer
import xml.etree.ElementTree as ET
import numpy as np
from models  import *

device = torch.device('cpu')

bert = BertModel.from_pretrained('rubert-base-cased-sentence')
tokenizer = BertTokenizer.from_pretrained('rubert-base-cased-sentence')

multiclass = BERT_based(bert)
multiclass.load_state_dict(torch.load("pretrained/multiclass.pt"))
multiclass.to(device)
multiclass.eval()

oneclass = Autoencoder(768)
oneclass.load_state_dict(torch.load("pretrained/oneclass.pt"))
oneclass.to(device)
oneclass.eval()

def tokenize(text):
    tokenized = tokenizer.batch_encode_plus(text, max_length=15, padding='max_length', truncation=True,return_tensors="pt")
    return tokenized

def get_embedding(text):
    inputs = tokenizer(text, max_length=15, padding='max_length', truncation=True,return_tensors="pt")
    with torch.no_grad():
        outputs = bert(**inputs)
    last_hidden_state = outputs.last_hidden_state
    sentence_embedding = last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    return sentence_embedding

def detect_anomalies(model, data, threshold=0.1266):
    with torch.no_grad():
        reconstructed = model(data)
        reconstructed = reconstructed.squeeze(0) 
        loss = torch.mean((reconstructed - data) ** 2, dim=1)
    return (loss > threshold).cpu().numpy()
    
def multipred(text):
    text = [text]
    tokens = tokenize(text)
    input_id = tokens["input_ids"].to(device)
    attention_mask = tokens["attention_mask"].to(device)
    
    with torch.no_grad():
        pred = multiclass(input_id, attention_mask)

    pred = pred.cpu().numpy()
    result = np.argmax(pred, axis=1)+1
    return result
    
def onepred(text):
    embed = get_embedding(text)
    tensor = torch.tensor(embed, dtype=torch.float32).reshape(1, 768)
    #print(f"DEBUG!!! {tensor.size()}")
    anomalies = detect_anomalies(oneclass, tensor)
    #print(f"DEBUG!!! {anomalies[0]}")
    return anomalies[0]
    
def classify_text(text):
    
    bool = onepred(text)
    
    if bool == 0:
        return multipred(text)
    else:
        return 0
    
def get_answer(index):
    
    with open('answer_data.xml', 'r', encoding='utf-8') as file:
        data = file.read()

    root = ET.fromstring(data)
    
    for answer in root.findall('answer'):
        if int(answer.attrib['id']) == index:
            return answer.text.strip()   